#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import rclpy
from rclpy.node import Node
from a2rl_bs_msgs.msg import ControllerStatus, ControllerDebug, Localization, EgoState, VectornavIns, FlyeagleEyePlannerReport
from eav24_bsu_msgs.msg import Wheels_Speed_01, HL_Msg_01, HL_Msg_02, HL_Msg_03, ICE_Status_01, ICE_Status_02, PSA_Status_01, Tyre_Surface_Temp_Front, Tyre_Surface_Temp_Rear, Brake_Disk_Temp 
from sensor_msgs.msg import PointCloud2, Image
from std_msgs.msg import Float32MultiArray, Float32, Bool
from cv_bridge import CvBridge
import time
import os
import yaml
import json
import threading
import numpy as np
import ros2_numpy
import cv2
from spirems import Publisher, Subscriber, def_msg, cvimg2sms
import psutil


"""
依赖项安装：
pip install spirems ros2-numpy psutil pynvjpeg
"""

DEFAULT_IP = "47.91.111.225"


# 从 rpy 计算旋转矩阵
def rpy_to_rotation_matrix(roll, pitch, yaw):
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    R_y = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    R_z = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])
    return R_z @ R_y @ R_x

# 转换点云
def transform_points(points, rotation_matrix, translation_vector):
    # 点云坐标变换: P' = R * P + t
    return (rotation_matrix @ points.T).T + translation_vector

# 定义 Lidar 的参数
lidar_params = {
    "lidar_front": {"xyz": [2.199, 0.053, 0.744], "rpy": [-0.144, -1.550, -2.993]},
    "lidar_left": {"xyz": [1.691, 0.2969, 0.80634], "rpy": [-0.420, -1.553, -0.622]},
    "lidar_right": {"xyz": [1.691, -0.1969, 0.755093], "rpy": [0.625635, -1.5428, 0.424122]}
}


t_front = np.array(lidar_params["lidar_front"]["xyz"])
rpy_front = lidar_params["lidar_front"]["rpy"]
R_front = rpy_to_rotation_matrix(*rpy_front)

t_left = np.array(lidar_params["lidar_left"]["xyz"])
rpy_left = lidar_params["lidar_left"]["rpy"]
R_left = rpy_to_rotation_matrix(*rpy_left)

t_right = np.array(lidar_params["lidar_right"]["xyz"])
rpy_right = lidar_params["lidar_right"]["rpy"]
R_right = rpy_to_rotation_matrix(*rpy_right)


def cpu_monit(sms_msg):
    cpu_cnt = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    sms_msg['cpu'] = cpu_percent
    # cpu_freq = psutil.cpu_freq(percpu=False)

    virtual_memory = psutil.virtual_memory()
    sms_msg['mem'] = virtual_memory.used / 1024 / 1024 / 1024

    disk_usage = psutil.disk_usage('/')
    sms_msg['disk'] = disk_usage.used / 1024 / 1024 / 1024 / 1024

    sensors_temperatures = psutil.sensors_temperatures()
    if 'coretemp' in sensors_temperatures:
        sms_msg['cpu_temp'] = sensors_temperatures['coretemp'][0].current
    elif 'k10temp' in sensors_temperatures:
        sms_msg['cpu_temp'] = sensors_temperatures['k10temp'][0].current

    return sms_msg


# ==============================================================================
#                                                                   SCALE_TO_255
# ==============================================================================
def scale_to_255(a, min, max, dtype=np.uint8):
    """ Scales an array of values from specified min, max range to 0-255
        Optionally specify the data type of the output (default is uint8)
    """
    return (((a - min) / float(max - min)) * 255).astype(dtype)


# ==============================================================================
#                                                         POINT_CLOUD_2_BIRDSEYE
# ==============================================================================
def point_cloud_2_birdseye(points,
                           res=0.2,
                           side_range=(-40., 40.),  # left-most to right-most
                           fwd_range=(-30., 30.), # back-most to forward-most
                           height_range=(-2., 2.),  # bottom-most to upper-most
                           ):
    """ Creates an 2D birds eye view representation of the point cloud data.

    Args:
        points:     (numpy array)
                    N rows of points data
                    Each point should be specified by at least 3 elements x,y,z
        res:        (float)
                    Desired resolution in metres to use. Each output pixel will
                    represent an square region res x res in size.
        side_range: (tuple of two floats)
                    (-left, right) in metres
                    left and right limits of rectangle to look at.
        fwd_range:  (tuple of two floats)
                    (-behind, front) in metres
                    back and front limits of rectangle to look at.
        height_range: (tuple of two floats)
                    (min, max) heights (in metres) relative to the origin.
                    All height values will be clipped to this min and max value,
                    such that anything below min will be truncated to min, and
                    the same for values above max.
    Returns:
        2D numpy array representing an image of the birds eye view.
    """
    # EXTRACT THE POINTS FOR EACH AXIS
    x_points = points[:, 0]
    y_points = points[:, 1]
    z_points = points[:, 2]

    # FILTER - To return only indices of points within desired cube
    # Three filters for: Front-to-back, side-to-side, and height ranges
    # Note left side is positive y axis in LIDAR coordinates
    f_filt = np.logical_and((x_points > fwd_range[0]), (x_points < fwd_range[1]))
    s_filt = np.logical_and((y_points > -side_range[1]), (y_points < -side_range[0]))
    filter = np.logical_and(f_filt, s_filt)
    indices = np.argwhere(filter).flatten()

    # KEEPERS
    x_points = x_points[indices]
    y_points = y_points[indices]
    z_points = z_points[indices]

    # CONVERT TO PIXEL POSITION VALUES - Based on resolution
    x_img = (-y_points / res).astype(np.int32)  # x axis is -y in LIDAR
    y_img = (-x_points / res).astype(np.int32)  # y axis is -x in LIDAR

    # SHIFT PIXELS TO HAVE MINIMUM BE (0,0)
    # floor & ceil used to prevent anything being rounded to below 0 after shift
    x_img -= int(np.floor(side_range[0] / res))
    y_img += int(np.ceil(fwd_range[1] / res))

    # CLIP HEIGHT VALUES - to between min and max heights
    pixel_values = np.clip(a=z_points,
                           a_min=height_range[0],
                           a_max=height_range[1])

    # RESCALE THE HEIGHT VALUES - to be between the range 0-255
    pixel_values = scale_to_255(pixel_values,
                                min=height_range[0],
                                max=height_range[1])

    # INITIALIZE EMPTY ARRAY - of the dimensions we want
    x_max = 1 + int((side_range[1] - side_range[0]) / res)
    y_max = 1 + int((fwd_range[1] - fwd_range[0]) / res)
    # im = np.zeros([y_max, x_max, 3], dtype=np.uint8)
    im = np.zeros([y_max, x_max], dtype=np.uint8)

    # FILL PIXEL VALUES IN IMAGE ARRAY
    # im[y_img, x_img, 1] = pixel_values
    # im[y_img, x_img, 2] = pixel_values
    im[y_img, x_img] = pixel_values

    return im


class A2RLTeamFlyEagleMonitNode(Node, threading.Thread):
    def __init__(self):
        Node.__init__(self, 'A2RLTeamFlyEagleMonitNode')
        threading.Thread.__init__(self)

        self.latest_camera_fl_msg = None
        self.latest_camera_fl_lock = threading.Lock()
        self.latest_camera_fr_msg = None
        self.latest_camera_fr_lock = threading.Lock()
        self.latest_camera_cl_msg = None
        self.latest_camera_cl_lock = threading.Lock()
        self.latest_camera_cr_msg = None
        self.latest_camera_cr_lock = threading.Lock()
        self.latest_camera_rl_msg = None
        self.latest_camera_rl_lock = threading.Lock()
        self.latest_camera_rr_msg = None
        self.latest_camera_rr_lock = threading.Lock()
        self.latest_camera_r_msg = None
        self.latest_camera_r_lock = threading.Lock()

        self.latest_kistler_status_msg = None
        self.latest_kistler_status_lock = threading.Lock()
        self.latest_observer_ego_loc_msg = None
        self.latest_observer_ego_loc_lock = threading.Lock()
        self.latest_observer_ego_state_msg = None
        self.latest_observer_ego_state_lock = threading.Lock()
        self.latest_a2rl_vn_ins_msg = None
        self.latest_a2rl_vn_ins_lock = threading.Lock()
        self.latest_sensor_lidar_front_msg = None
        self.latest_sensor_lidar_front_lock = threading.Lock()
        self.latest_sensor_lidar_left_msg = None
        self.latest_sensor_lidar_left_lock = threading.Lock()
        self.latest_sensor_lidar_right_msg = None
        self.latest_sensor_lidar_right_lock = threading.Lock()
        self.latest_controller_debug_msg = None
        self.latest_controller_debug_lock = threading.Lock()
        self.latest_controller_status_msg = None
        self.latest_controller_status_lock = threading.Lock()
        self.latest_ego_loc_msg = None
        self.latest_ego_loc_lock = threading.Lock()
        self.latest_ego_state_msg = None
        self.latest_ego_state_lock = threading.Lock()
        self.latest_hlmsg_01_msg = None
        self.latest_hlmsg_01_lock = threading.Lock()
        self.latest_hlmsg_02_msg = None
        self.latest_hlmsg_02_lock = threading.Lock()
        self.latest_hlmsg_03_msg = None
        self.latest_hlmsg_03_lock = threading.Lock()
        self.latest_ice_status_01_msg = None
        self.latest_ice_status_01_lock = threading.Lock()
        self.latest_ice_status_02_msg = None
        self.latest_ice_status_02_lock = threading.Lock()
        self.latest_psa_status_01_msg = None
        self.latest_psa_status_01_lock = threading.Lock()
        self.latest_tyre_surface_temp_front_msg = None
        self.latest_tyre_surface_temp_front_lock = threading.Lock()
        self.latest_tyre_surface_temp_rear_msg = None
        self.latest_tyre_surface_temp_rear_lock = threading.Lock()

        self.latest_planner_reference_s_distance_msg = None
        self.latest_planner_reference_s_distance_lock = threading.Lock()
        self.latest_planner_real_perc_msg = None
        self.latest_planner_real_perc_lock = threading.Lock()
        self.latest_lap_times_msg = None
        self.latest_lap_times_lock = threading.Lock()

        self.latest_brake_disk_temp_msg = None
        self.latest_brake_disk_temp_lock = threading.Lock()

        self.camera_fl_sub = self.create_subscription(
            Image, "/sensor/camera/camera_fl/sxcam_raw", self.camera_fl_callback, 10
        )
        self.camera_fr_sub = self.create_subscription(
            Image, "/sensor/camera/camera_fr/sxcam_raw", self.camera_fr_callback, 10
        )
        self.camera_cl_sub = self.create_subscription(
            Image, "/sensor/camera/camera_cl/sxcam_raw", self.camera_cl_callback, 10
        )
        self.camera_cr_sub = self.create_subscription(
            Image, "/sensor/camera/camera_cr/sxcam_raw", self.camera_cr_callback, 10
        )
        self.camera_rl_sub = self.create_subscription(
            Image, "/sensor/camera/camera_rl/sxcam_raw", self.camera_rl_callback, 10
        )
        self.camera_rr_sub = self.create_subscription(
            Image, "/sensor/camera/camera_rr/sxcam_raw", self.camera_rr_callback, 10
        )
        self.camera_r_sub = self.create_subscription(
            Image, "/sensor/camera/camera_r/sxcam_raw", self.camera_r_callback, 10
        )

        self.kistler_status_sub = self.create_subscription(
            Bool,
            "/localization/kistler_status",
            self.kistler_status_callback,
            10
        )
        self.observer_ego_loc_sub = self.create_subscription(
            Localization,
            "/a2rl/observer/ego_loc",
            self.observer_ego_loc_callback,
            10
        )
        self.observer_ego_state_sub = self.create_subscription(
            EgoState,
            "/a2rl/observer/ego_state",
            self.observer_ego_state_callback,
            10
        )

        self.planner_reference_s_distance_sub = self.create_subscription(
            Float32MultiArray,
            "/a2rl/planner/reference_s_distance",
            self.planner_reference_s_distance_callback,
            10
        )
        self.planner_real_perc_sub = self.create_subscription(
            Float32,
            "/a2rl/planner/real_perc",
            self.planner_real_perc_callback,
            10
        )
        self.lap_times_sub = self.create_subscription(
            Float32MultiArray,
            "/lap_times",
            self.lap_times_callback,
            10
        )

        self.a2rl_vn_ins_sub = self.create_subscription(
            VectornavIns,
            "/a2rl/vn/ins",
            self.a2rl_vn_ins_callback,
            10
        )
        self.sensor_lidar_front_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_front/points",
            self.sensor_lidar_front_callback,
            10
        )
        self.sensor_lidar_left_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_left/points",
            self.sensor_lidar_left_callback,
            10
        )
        self.sensor_lidar_right_sub = self.create_subscription(
            PointCloud2,
            "/sensor/lidar_right/points",
            self.sensor_lidar_right_callback,
            10
        )
        self.controller_debug_sub = self.create_subscription(
            ControllerDebug,
            "/a2rl/controller/debug",
            self.controller_debug_callback,
            10
        )
        self.controller_status_sub = self.create_subscription(
            ControllerStatus,
            "/a2rl/controller/status",
            self.controller_status_callback,
            10
        )
        self.ego_loc_sub = self.create_subscription(
            Localization,
            "/a2rl/observer/ego_loc/low_freq",
            self.ego_loc_callback,
            10
        )
        self.ego_state_sub = self.create_subscription(
            EgoState,
            "/a2rl/observer/ego_state/low_freq",
            self.ego_state_callback,
            10
        )
        self.hlmsg_01_sub = self.create_subscription(
            HL_Msg_01,
            "/a2rl/eav24_bsu/hl_msg_01",
            self.hlmsg_01_callback,
            10
        )
        self.hlmsg_02_sub = self.create_subscription(
            HL_Msg_02,
            "/a2rl/eav24_bsu/hl_msg_02",
            self.hlmsg_02_callback,
            10
        )
        self.hlmsg_03_sub = self.create_subscription(
            HL_Msg_03,
            "/a2rl/eav24_bsu/hl_msg_03",
            self.hlmsg_03_callback,
            10
        )
        self.ice_status_01_sub = self.create_subscription(
            ICE_Status_01,
            "/a2rl/eav24_bsu/ice_status_01",
            self.ice_status_01_callback,
            10
        )
        self.ice_status_02_sub = self.create_subscription(
            ICE_Status_02,
            "/a2rl/eav24_bsu/ice_status_02",
            self.ice_status_02_callback,
            10
        )
        self.psa_status_01_sub = self.create_subscription(
            PSA_Status_01,
            "/a2rl/eav24_bsu/psa_status_01",
            self.psa_status_01_callback,
            10
        )
        self.tyre_surface_temp_front_sub = self.create_subscription(
            Tyre_Surface_Temp_Front,
            "/a2rl/eav24_bsu/tyre_surface_temp_front",
            self.tyre_surface_temp_front_callback,
            10
        )
        self.tyre_surface_temp_rear_sub = self.create_subscription(
            Tyre_Surface_Temp_Rear,
            "/a2rl/eav24_bsu/tyre_surface_temp_rear",
            self.tyre_surface_temp_rear_callback,
            10
        )

        self.brake_disk_temp_sub = self.create_subscription(
            Brake_Disk_Temp,
            "/a2rl/eav24_bsu/brake_disk_temp",
            self.brake_disk_temp_callback,
            10
        )
        self.init_sms_msg()
        self.sms_msg_pub = Publisher("/flyeagle/status", "std_msgs::Null", ip=DEFAULT_IP)
        self.sms_lidar_pub = Publisher("/flyeagle/lidar_map", "sensor_msgs::CompressedImage", ip=DEFAULT_IP)
        self.sms_sub = Subscriber("/flyeagle/live_switch", "std_msgs::Number", self.live_switch_callback, ip=DEFAULT_IP)
        self.live_key = 0
        self.bridge = CvBridge()
        self.start()

    def live_switch_callback(self, msg):
        self.live_key = msg['data']

    def camera_fl_callback(self, msg):
        with self.latest_camera_fl_lock:
            self.latest_camera_fl_msg = msg

    def camera_fr_callback(self, msg):
        with self.latest_camera_fr_lock:
            self.latest_camera_fr_msg = msg

    def camera_cl_callback(self, msg):
        with self.latest_camera_cl_lock:
            self.latest_camera_cl_msg = msg

    def camera_cr_callback(self, msg):
        with self.latest_camera_cr_lock:
            self.latest_camera_cr_msg = msg

    def camera_rl_callback(self, msg):
        with self.latest_camera_rl_lock:
            self.latest_camera_rl_msg = msg

    def camera_rr_callback(self, msg):
        with self.latest_camera_rr_lock:
            self.latest_camera_rr_msg = msg

    def camera_r_callback(self, msg):
        with self.latest_camera_r_lock:
            self.latest_camera_r_msg = msg

    def kistler_status_callback(self, msg):
        with self.latest_kistler_status_lock:
            self.latest_kistler_status_msg = msg

    def observer_ego_loc_callback(self, msg):
        with self.latest_observer_ego_loc_lock:
            self.latest_observer_ego_loc_msg = msg

    def observer_ego_state_callback(self, msg):
        with self.latest_observer_ego_state_lock:
            self.latest_observer_ego_state_msg = msg

    def planner_reference_s_distance_callback(self, msg):
        with self.latest_planner_reference_s_distance_lock:
            self.latest_planner_reference_s_distance_msg = msg
    
    def planner_real_perc_callback(self, msg):
        with self.latest_planner_real_perc_lock:
            self.latest_planner_real_perc_msg = msg
    
    def lap_times_callback(self, msg):
        with self.latest_lap_times_lock:
            self.latest_lap_times_msg = msg

    def a2rl_vn_ins_callback(self, msg):
        with self.latest_a2rl_vn_ins_lock:
            self.latest_a2rl_vn_ins_msg = msg
    
    def sensor_lidar_front_callback(self, msg):
        with self.latest_sensor_lidar_front_lock:
            self.latest_sensor_lidar_front_msg = msg
    
    def sensor_lidar_left_callback(self, msg):
        with self.latest_sensor_lidar_left_lock:
            self.latest_sensor_lidar_left_msg = msg
    
    def sensor_lidar_right_callback(self, msg):
        with self.latest_sensor_lidar_right_lock:
            self.latest_sensor_lidar_right_msg = msg
    
    def controller_debug_callback(self, msg):
        with self.latest_controller_debug_lock:
            self.latest_controller_debug_msg = msg
    
    def controller_status_callback(self, msg):
        with self.latest_controller_status_lock:
            self.latest_controller_status_msg = msg

    def ego_loc_callback(self, msg):
        self.latest_ego_loc_msg = msg

    def ego_state_callback(self, msg):
        self.latest_ego_state_msg = msg

    def hlmsg_01_callback(self, msg):
        self.latest_hlmsg_01_msg = msg

    def hlmsg_02_callback(self, msg):
        self.latest_hlmsg_02_msg = msg

    def hlmsg_03_callback(self, msg):
        self.latest_hlmsg_03_msg = msg

    def ice_status_01_callback(self, msg):
        with self.latest_ice_status_01_lock:
            self.latest_ice_status_01_msg = msg

    def ice_status_02_callback(self, msg):
        with self.latest_ice_status_02_lock:
            self.latest_ice_status_02_msg = msg

    def psa_status_01_callback(self, msg):
        with self.latest_psa_status_01_lock:
            self.latest_psa_status_01_msg = msg
    
    def tyre_surface_temp_front_callback(self, msg):
        with self.latest_tyre_surface_temp_front_lock:
            self.latest_tyre_surface_temp_front_msg = msg
    
    def tyre_surface_temp_rear_callback(self, msg):
        with self.latest_tyre_surface_temp_rear_lock:
            self.latest_tyre_surface_temp_rear_msg = msg
    
    def brake_disk_temp_callback(self, msg):
        with self.latest_brake_disk_temp_lock:
            self.latest_brake_disk_temp_msg = msg
    
    def init_sms_msg(self):
        self.sms_msg = def_msg('std_msgs::Null')
        self.sms_msg['ego_position'] = [0, 0, 0]
        self.sms_msg['ego_orientation_ypr'] = [0, 0, 0]
        self.sms_msg['ego_velocity'] = [0, 0, 0]
        self.sms_msg['ego_acceleration'] = [0, 0, 0]
        self.sms_msg['position_enu_ins'] = [0, 0, 0]
        self.sms_msg['velocity_body_ins'] = [0, 0, 0]
        self.sms_msg['acceleration_ins'] = [0, 0, 0]
        self.sms_msg['orientation_ypr'] = [0, 0, 0]
        self.sms_msg['ice_actual_gear'] = 1
        self.sms_msg['ice_actual_throttle'] = 0.0
        self.sms_msg['ice_engine_speed_rpm'] = 0.0
        self.sms_msg['ice_water_temp_deg_c'] = 0.0
        self.sms_msg['ice_oil_temp_deg_c'] = 0.0
        self.sms_msg['lateral_error'] = 0.0
        self.sms_msg['yaw_error'] = 0.0
        self.sms_msg['speed_error'] = 0.0
        self.sms_msg['front_brake'] = 0.0
        self.sms_msg['rear_brake'] = 0.0
        self.sms_msg['slip_f'] = 0.0
        self.sms_msg['slip_r'] = 0.0
        self.sms_msg['safe_stop_mode'] = 0
        self.sms_msg['reason_for_safestop'] = ''
        self.sms_msg['psa_actual_pos_rad'] = 0.0
        self.sms_msg['tyre_temp_fl'] = [0, 0, 0]
        self.sms_msg['tyre_temp_fr'] = [0, 0, 0]
        self.sms_msg['tyre_temp_rl'] = [0, 0, 0]
        self.sms_msg['tyre_temp_rr'] = [0, 0, 0]
        self.sms_msg['brake_disk_temp_fl'] = 0.0
        self.sms_msg['brake_disk_temp_fr'] = 0.0
        self.sms_msg['brake_disk_temp_rl'] = 0.0
        self.sms_msg['brake_disk_temp_rr'] = 0.0
        self.sms_msg['s_flag'] = 0.0
        self.sms_msg['s_distance'] = 0.0
        self.sms_msg['s_cure'] = 100.0
        self.sms_msg['real_perc'] = 0.0
        self.sms_msg['lap_count'] = 0
        self.sms_msg['kistler_status'] = 0

    def run(self):
        lidar1_on = False
        lidar2_on = False
        lidar3_on = False
        while True:
            t1 = time.time()
            with self.latest_observer_ego_loc_lock:
                if self.latest_observer_ego_loc_msg is not None:
                    msg = self.latest_observer_ego_loc_msg
                    self.sms_msg['ego_position'] = [msg.position.x, msg.position.y, msg.position.z]
                    self.sms_msg['ego_orientation_ypr'] = [msg.orientation_ypr.x, msg.orientation_ypr.y, msg.orientation_ypr.z]
            with self.latest_observer_ego_state_lock:
                if self.latest_observer_ego_state_msg is not None:
                    msg = self.latest_observer_ego_state_msg
                    self.sms_msg['ego_velocity'] = [msg.velocity.x, msg.velocity.y, msg.velocity.z]
                    self.sms_msg['ego_acceleration'] = [msg.acceleration.x, msg.acceleration.y, msg.acceleration.z]
            with self.latest_a2rl_vn_ins_lock:
                if self.latest_a2rl_vn_ins_msg is not None:
                    msg = self.latest_a2rl_vn_ins_msg
                    self.sms_msg['position_enu_ins'] = [msg.position_enu_ins.x, msg.position_enu_ins.y, msg.position_enu_ins.z]
                    self.sms_msg['velocity_body_ins'] = [msg.velocity_body_ins.x, msg.velocity_body_ins.y, msg.velocity_body_ins.z]
                    self.sms_msg['acceleration_ins'] = [msg.acceleration_ins.x, msg.acceleration_ins.y, msg.acceleration_ins.z]
                    self.sms_msg['orientation_ypr'] = [msg.orientation_ypr.x, msg.orientation_ypr.y, msg.orientation_ypr.z]
            with self.latest_sensor_lidar_front_lock:
                if self.latest_sensor_lidar_front_msg is not None:
                    msg = self.latest_sensor_lidar_front_msg
                    pcd_front = ros2_numpy.numpify(msg)['xyz']
                    lidar1_on = True
            with self.latest_sensor_lidar_left_lock:
                if self.latest_sensor_lidar_left_msg is not None:
                    msg = self.latest_sensor_lidar_left_msg
                    pcd_left = ros2_numpy.numpify(msg)['xyz']
                    lidar2_on = True
            with self.latest_sensor_lidar_right_lock:
                if self.latest_sensor_lidar_right_msg is not None:
                    msg = self.latest_sensor_lidar_right_msg
                    pcd_right = ros2_numpy.numpify(msg)['xyz']
                    lidar3_on = True
            with self.latest_ice_status_01_lock:
                if self.latest_ice_status_01_msg is not None:
                    msg = self.latest_ice_status_01_msg
                    self.sms_msg['ice_actual_gear'] = msg.ice_actual_gear
                    self.sms_msg['ice_actual_throttle'] = msg.ice_actual_throttle
            with self.latest_ice_status_02_lock:
                if self.latest_ice_status_02_msg is not None:
                    msg = self.latest_ice_status_02_msg
                    self.sms_msg['ice_engine_speed_rpm'] = msg.ice_engine_speed_rpm
                    self.sms_msg['ice_water_temp_deg_c'] = msg.ice_water_temp_deg_c
                    self.sms_msg['ice_oil_temp_deg_c'] = msg.ice_oil_temp_deg_c
            with self.latest_controller_debug_lock:
                if self.latest_controller_debug_msg is not None:
                    msg = self.latest_controller_debug_msg
                    self.sms_msg['lateral_error'] = msg.lateral_error
                    self.sms_msg['yaw_error'] = msg.yaw_error
                    self.sms_msg['speed_error'] = msg.speed_error
            with self.latest_controller_status_lock:
                if self.latest_controller_status_msg is not None:
                    msg = self.latest_controller_status_msg
                    self.sms_msg['front_brake'] = msg.front_brake
                    self.sms_msg['rear_brake'] = msg.rear_brake
                    self.sms_msg['slip_f'] = msg.slip_f
                    self.sms_msg['slip_r'] = msg.slip_r
                    self.sms_msg['safe_stop_mode'] = msg.safe_stop_mode
                    self.sms_msg['reason_for_safestop'] = msg.reason_for_safestop
            with self.latest_tyre_surface_temp_front_lock:
                if self.latest_tyre_surface_temp_front_msg is not None:
                    msg = self.latest_tyre_surface_temp_front_msg
                    self.sms_msg['tyre_temp_fl'] = [msg.outer_fl, msg.center_fl, msg.inner_fl]
                    self.sms_msg['tyre_temp_fr'] = [msg.outer_fr, msg.center_fr, msg.inner_fr]
            with self.latest_tyre_surface_temp_rear_lock:
                if self.latest_tyre_surface_temp_rear_msg is not None:
                    msg = self.latest_tyre_surface_temp_rear_msg
                    self.sms_msg['tyre_temp_rl'] = [msg.outer_rl, msg.center_rl, msg.inner_rl]
                    self.sms_msg['tyre_temp_rr'] = [msg.outer_rr, msg.center_rr, msg.inner_rr]
            with self.latest_psa_status_01_lock:
                if self.latest_psa_status_01_msg is not None:
                    msg = self.latest_psa_status_01_msg
                    self.sms_msg['psa_actual_pos_rad'] = msg.psa_actual_pos_rad            
            with self.latest_brake_disk_temp_lock:
                if self.latest_brake_disk_temp_msg is not None:
                    msg = self.latest_brake_disk_temp_msg
                    self.sms_msg['brake_disk_temp_fl'] = msg.brake_disk_temp_fl
                    self.sms_msg['brake_disk_temp_fr'] = msg.brake_disk_temp_fr
                    self.sms_msg['brake_disk_temp_rl'] = msg.brake_disk_temp_rl
                    self.sms_msg['brake_disk_temp_rr'] = msg.brake_disk_temp_rr

            with self.latest_planner_reference_s_distance_lock:
                if self.latest_planner_reference_s_distance_msg is not None:
                    msg = self.latest_planner_reference_s_distance_msg
                    self.sms_msg['s_flag'] = msg.data[0]
                    self.sms_msg['s_distance'] = msg.data[1]
                    self.sms_msg['s_cure'] = msg.data[2]
            with self.latest_planner_real_perc_lock:
                if self.latest_planner_real_perc_msg is not None:
                    msg = self.latest_planner_real_perc_msg
                    self.sms_msg['real_perc'] = msg.data
            with self.latest_lap_times_lock:
                if self.latest_lap_times_msg is not None:
                    msg = self.latest_lap_times_msg
                    self.sms_msg['lap_count'] = len(msg.data)
            with self.latest_kistler_status_lock:
                if self.latest_kistler_status_msg is not None:
                    msg = self.latest_kistler_status_msg
                    self.sms_msg['kistler_status'] = 1 if msg.data else 0

            if self.live_key > 0:
                cv_image = None
                if self.live_key == 1:
                    with self.latest_camera_fl_lock:
                        if self.latest_camera_fl_msg is not None:
                            msg = self.latest_camera_fl_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 2:
                    with self.latest_camera_fr_lock:
                        if self.latest_camera_fr_msg is not None:
                            msg = self.latest_camera_fr_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 3:
                    with self.latest_camera_cl_lock:
                        if self.latest_camera_cl_msg is not None:
                            msg = self.latest_camera_cl_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 4:
                    with self.latest_camera_cr_lock:
                        if self.latest_camera_cr_msg is not None:
                            msg = self.latest_camera_cr_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 5:
                    with self.latest_camera_rl_lock:
                        if self.latest_camera_rl_msg is not None:
                            msg = self.latest_camera_rl_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 6:
                    with self.latest_camera_rr_lock:
                        if self.latest_camera_rr_msg is not None:
                            msg = self.latest_camera_rr_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                elif self.live_key == 7:
                    with self.latest_camera_r_lock:
                        if self.latest_camera_r_msg is not None:
                            msg = self.latest_camera_r_msg
                            try:
                                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                            except Exception as e:
                                print(e)
                if cv_image is not None:
                    sms_img = cvimg2sms(cv_image)
                    self.sms_lidar_pub.publish(sms_img)

            if self.live_key == 0 and lidar1_on and lidar2_on and lidar3_on:
                pcd_front = transform_points(pcd_front[::4], R_front, t_front)
                pcd_left = transform_points(pcd_left[::4], R_left, t_left)
                pcd_right = transform_points(pcd_right[::4], R_right, t_right)

                pcd = np.concatenate((pcd_front, pcd_left, pcd_right), axis=0)
                img = point_cloud_2_birdseye(pcd)
                sms_img = cvimg2sms(img)
                self.sms_lidar_pub.publish(sms_img)
                # cv2.imshow('img', img)
                # cv2.waitKey(5)
            
            self.sms_msg = cpu_monit(self.sms_msg)
            self.sms_msg["timestamp"] = time.time()
            self.sms_msg_pub.publish(self.sms_msg)
            # print(json.dumps(self.sms_msg, indent=4))


def main(args=None):
    rclpy.init(args=args)
    node = A2RLTeamFlyEagleMonitNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
