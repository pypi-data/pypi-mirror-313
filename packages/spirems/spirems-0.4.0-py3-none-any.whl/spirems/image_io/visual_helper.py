#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import cv2
import os
from PIL import ImageFont, ImageDraw, Image
import csv
from datetime import datetime


font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/fradmcn.ttf')
font_path_big = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/msyh_boot.ttf')
font_size = 17
font_color = (255, 255, 255)
font = ImageFont.truetype(font_path, font_size)
font_s = ImageFont.truetype(font_path, 10)
font_big = ImageFont.truetype(font_path_big, 60)
font_50 = ImageFont.truetype(font_path_big, 50)
font_20 = ImageFont.truetype(font_path_big, 20)
font_15 = ImageFont.truetype(font_path_big, 15)
accel_list = []
full_map_mask = None
colors_g2r = [
    (53, 143, 10),
    (32, 143, 10),
    (10, 143, 10),
    (10, 143, 37),
    (10, 143, 66),
    (15, 204, 120),  # 5
    (27, 238, 224),
    (27, 184, 238),
    (12, 69, 233),
    (29, 16, 244),
    (29, 16, 244)
]


def load_a2rl_logo() -> np.ndarray:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/racecar.jpg')
    default_img = cv2.imread(img_path)
    return default_img


def draw_charts(img: np.ndarray, visual_msg: dict) -> np.ndarray:
    if len(img.shape) == 3 and img.shape[0] == 720 and img.shape[1] == 1280:
        img_show_ = img.copy()
        show_h, show_w = 120, 1280
        menu_img = img_show_[-show_h:, :show_w]
        menu_mask = np.zeros_like(menu_img, dtype=np.uint8)
        menu_img = cv2.addWeighted(menu_img, 0.5, menu_mask, 0.5, 0)
        if 'bar_chart_items' in visual_msg:
            for item in visual_msg['bar_chart_items']:  # chart
                posx = item['posx']
                val = item['val']
                val_min = item['val_min']
                val_max = item['val_max']
                if val < val_min:
                    val = val_min
                if val > val_max:
                    val = val_max
                x, y, w, h = (30 + posx, 30, 10, 60)
                cv2.rectangle(menu_img, (x, y), (x + w, y + h), (255, 255, 255), 1)
                x, y, w, h = (30 + posx, int(30 + 60 * (val_max - val) / val_max), 10, int(60 * val / val_max))
                cv2.rectangle(menu_img, (x, y), (x + w, y + h), (255, 255, 255), -1)

            pil_image = Image.fromarray(cv2.cvtColor(menu_img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            for item in visual_msg['bar_chart_items']:  # text
                posx = item['posx']
                text = item['title_refresh']
                name = item['title']
                val = item['val']
                val_min = item['val_min']
                val_max = item['val_max']
                if val < val_min:
                    val = val_min
                if val > val_max:
                    val = val_max
                draw.text((32 + posx - len(text.format(val)) * 3, 8), text.format(val), font=font, fill=font_color)
                draw.text((32 + posx - len(name) * 3, 94), name, font=font, fill=font_color)

            time_str = datetime.now().strftime("%H:%M:%S")
            draw.text((640 - 100, 20), time_str, font=font_big, fill=font_color)
            menu_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        img_show_[-show_h:, :show_w] = menu_img
        img = img_show_
    return img


def draw_charts_v2(img: np.ndarray, visual_msg) -> np.ndarray:
    if len(img.shape) == 3 and img.shape[0] == 720 and img.shape[1] == 1280:
        img_show_ = img.copy()
        show_h, show_w = 160, 1280
        menu_img = img_show_[-show_h:, :show_w]
        menu_mask = np.zeros_like(menu_img, dtype=np.uint8)
        menu_img = cv2.addWeighted(menu_img, 0.5, menu_mask, 0.5, 0)
        # print(visual_msg)
        i_gear = 1
        i_speed = 240
        i_rpm = 6100
        i_throttle = 70
        i_brake = 3  # front_brake
        i_fl_disc = 720
        i_fr_disc = 810
        i_rl_disc = 200
        i_rr_disc = 550
        i_fl_tyre = 100
        i_fr_tyre = 50
        i_rl_tyre = 50
        i_rr_tyre = 50
        f_psa_pos = -10
        f_gx = 0.0
        f_gy = 0.0

        f_s_flag = 0.0
        f_s_distance = 0.0
        f_s_cure = 100.0
        f_real_perc = 0.0
        i_lap_count = 0

        f_cpu = 0.0
        cpu_pos_x, cpu_val_min, cpu_val_max, cpu_text, cpu_fmt = 1210, 0, 100, "CPU", "{:.1f}%"
        f_cpu_temp = 0.0
        ct_pos_x, ct_val_min, ct_val_max, ct_text, ct_fmt = 1150, 0, 120, "CPU-Temp", "{:.1f}C"
        f_mem = 0.0
        mem_pos_x, mem_val_min, mem_val_max, mem_text, mem_fmt = 1090, 0, 128, "Mem", "{:.1f}G"
        f_disk = 0.0
        dsk_pos_x, dsk_val_min, dsk_val_max, dsk_text, dsk_fmt = 1030, 0.0, 15.2, "Disk", "{:.1f}TB"
        f_water_temp = 0.0
        wt_pos_x, wt_val_min, wt_val_max, wt_text, wt_fmt = 970, 0, 120, "Water", "{:.1f}C"
        f_lateral_err = 0.0
        le_pos_x, le_val_min, le_val_max, le_text, le_fmt = 910, 0, 10, "Lateral-Err", "{:.1f}m"
        if visual_msg is not None:
            if 'ice_actual_gear' in visual_msg:
                i_gear = int(visual_msg['ice_actual_gear'])
            if 'ice_actual_throttle' in visual_msg:
                i_throttle = int(visual_msg['ice_actual_throttle'])
            if 'ice_engine_speed_rpm' in visual_msg:
                i_rpm = int(visual_msg['ice_engine_speed_rpm'])
            if 'ice_water_temp_deg_c' in visual_msg:
                f_water_temp = visual_msg['ice_water_temp_deg_c']
            if 'front_brake' in visual_msg:
                i_brake = int(visual_msg['front_brake'])
            if 'velocity_body_ins' in visual_msg:
                i_speed = int(visual_msg['velocity_body_ins'][0] * 3.6)
            if 'psa_actual_pos_rad' in visual_msg:
                f_psa_pos = - visual_msg['psa_actual_pos_rad']
            if 'acceleration_ins' in visual_msg:
                f_gx = visual_msg['acceleration_ins'][0] / 9.8
                f_gy = visual_msg['acceleration_ins'][1] / 9.8
            if 'cpu' in visual_msg:
                f_cpu = visual_msg['cpu']
                f_cpu = min(100, f_cpu)
                f_cpu = max(0, f_cpu)
            if 'cpu_temp' in visual_msg:
                f_cpu_temp = visual_msg['cpu_temp']
                f_cpu = min(120, f_cpu)
                f_cpu = max(0, f_cpu)
            if 'mem' in visual_msg:
                f_mem = visual_msg['mem']
                f_mem = min(mem_val_max, f_mem)
                f_mem = max(mem_val_min, f_mem)
            if 'disk' in visual_msg:
                f_disk = visual_msg['disk']
                f_disk = min(dsk_val_max, f_disk)
                f_disk = max(dsk_val_min, f_disk)
            if 'lateral_error' in visual_msg:
                f_lateral_err = visual_msg['lateral_error']
                f_lateral_err = min(le_val_max, f_lateral_err)
                f_lateral_err = max(le_val_min, f_lateral_err)
            if 'tyre_temp_fl' in visual_msg:
                i_fl_tyre = visual_msg['tyre_temp_fl'][0]
            if 'tyre_temp_fr' in visual_msg:
                i_fr_tyre = visual_msg['tyre_temp_fr'][0]
            if 'tyre_temp_rl' in visual_msg:
                i_rl_tyre = visual_msg['tyre_temp_rl'][0]
            if 'tyre_temp_rr' in visual_msg:
                i_rr_tyre = visual_msg['tyre_temp_rr'][0]
            if 'brake_disk_temp_fl' in visual_msg:
                i_fl_disc = visual_msg['brake_disk_temp_fl']
            if 'brake_disk_temp_fr' in visual_msg:
                i_fr_disc = visual_msg['brake_disk_temp_fr']
            if 'brake_disk_temp_rl' in visual_msg:
                i_rl_disc = visual_msg['brake_disk_temp_rl']
            if 'brake_disk_temp_rr' in visual_msg:
                i_rr_disc = visual_msg['brake_disk_temp_rr']
            if 's_flag' in visual_msg:
                f_s_flag = visual_msg['s_flag']
            if 's_distance' in visual_msg:
                f_s_distance = visual_msg['s_distance']
            if 's_cure' in visual_msg:
                f_s_cure = visual_msg['s_cure']
            if 'real_perc' in visual_msg:
                f_real_perc = visual_msg['real_perc']
            if 'lap_count' in visual_msg:
                i_lap_count = visual_msg['lap_count']

        # CPU
        x, y, w, h = (30 + cpu_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + cpu_pos_x, int(30 + 100 * (cpu_val_max - f_cpu) / cpu_val_max), 10,
                      int(100 * f_cpu / cpu_val_max))
        color = colors_g2r[int(f_cpu * 10 / cpu_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)
        # CPU-Temp
        x, y, w, h = (30 + ct_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + ct_pos_x, int(30 + 100 * (ct_val_max - f_cpu_temp) / ct_val_max), 10,
                      int(100 * f_cpu_temp / ct_val_max))
        color = colors_g2r[int(f_cpu_temp * 10 / ct_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)
        # Memory
        x, y, w, h = (30 + mem_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + mem_pos_x, int(30 + 100 * (mem_val_max - f_mem) / mem_val_max), 10,
                      int(100 * f_mem / mem_val_max))
        color = colors_g2r[int(f_mem * 10 / mem_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)
        # Disk
        x, y, w, h = (30 + dsk_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + dsk_pos_x, int(30 + 100 * (dsk_val_max - f_disk) / dsk_val_max), 10,
                      int(100 * f_disk / dsk_val_max))
        color = colors_g2r[int(f_disk * 10 / dsk_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)
        # Water-Temp
        x, y, w, h = (30 + wt_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + wt_pos_x, int(30 + 100 * (wt_val_max - f_water_temp) / wt_val_max), 10,
                      int(100 * f_water_temp / wt_val_max))
        color = colors_g2r[int(f_water_temp * 10 / wt_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)
        # Lateral-Err
        x, y, w, h = (30 + le_pos_x, 30, 10, 100)
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), (30, 30, 30), -1)
        x, y, w, h = (30 + le_pos_x, int(30 + 100 * (le_val_max - f_lateral_err) / le_val_max), 10,
                      int(100 * f_lateral_err / le_val_max))
        color = colors_g2r[int(f_lateral_err * 10 / le_val_max)]
        cv2.rectangle(menu_img, (x, y), (x + w, y + h), color, -1)

        # Front-Left Brake Disc
        i_fl_disc = min(1000, i_fl_disc)
        i_fl_disc = max(0, i_fl_disc)
        cv2.circle(menu_img, (45, 80 - 30), 22, colors_g2r[int(i_fl_disc / 100)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 80 - 30), 10, (100, 100, 100), 6, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 80 - 30), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 80 - 30), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Front-Right Brake Disc
        i_fr_disc = min(1000, i_fr_disc)
        i_fr_disc = max(0, i_fr_disc)
        cv2.circle(menu_img, (105, 80 - 30), 22, colors_g2r[int(i_fr_disc / 100)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 80 - 30), 10, (100, 100, 100), 6, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 80 - 30), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 80 - 30), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Rear-Left Brake Disc
        i_rl_disc = min(1000, i_rl_disc)
        i_rl_disc = max(0, i_rl_disc)
        cv2.circle(menu_img, (45, 160 - 35), 22, colors_g2r[int(i_rl_disc / 100)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 160 - 35), 10, (100, 100, 100), 6, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 160 - 35), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (45, 160 - 35), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Rear-Right Brake Disc
        i_rr_disc = min(1000, i_rr_disc)
        i_rr_disc = max(0, i_rr_disc)
        cv2.circle(menu_img, (105, 160 - 35), 22, colors_g2r[int(i_rr_disc / 100)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 160 - 35), 10, (100, 100, 100), 6, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 160 - 35), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (105, 160 - 35), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Front-Left Tyre
        i_fl_tyre = min(200, i_fl_tyre)
        i_fl_tyre = max(0, i_fl_tyre)
        cv2.circle(menu_img, (175, 50), 25, colors_g2r[int(i_fl_tyre / 20)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 50), 14, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 50), 15, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(menu_img, (175 - 14, 50), (175 + 14, 50), (255, 255, 255), 1)
        cv2.line(menu_img, (175, 50 - 14), (175, 50 + 14), (255, 255, 255), 1)
        cv2.line(menu_img, (175 - 10, 50 - 10), (175 + 10, 50 + 10), (255, 255, 255), 1)
        cv2.line(menu_img, (175 - 10, 50 + 10), (175 + 10, 50 - 10), (255, 255, 255), 1)
        cv2.circle(menu_img, (175, 50), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 50), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Front-Right Tyre
        i_fr_tyre = min(200, i_fr_tyre)
        i_fr_tyre = max(0, i_fr_tyre)
        cv2.circle(menu_img, (240, 50), 25, colors_g2r[int(i_fr_tyre / 20)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 50), 14, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 50), 15, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(menu_img, (240 - 14, 50), (240 + 14, 50), (255, 255, 255), 1)
        cv2.line(menu_img, (240, 50 - 14), (240, 50 + 14), (255, 255, 255), 1)
        cv2.line(menu_img, (240 - 10, 50 - 10), (240 + 10, 50 + 10), (255, 255, 255), 1)
        cv2.line(menu_img, (240 - 10, 50 + 10), (240 + 10, 50 - 10), (255, 255, 255), 1)
        cv2.circle(menu_img, (240, 50), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 50), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Rear-Left Tyre
        i_rl_tyre = min(200, i_rl_tyre)
        i_rl_tyre = max(0, i_rl_tyre)
        cv2.circle(menu_img, (175, 125), 25, colors_g2r[int(i_rl_tyre / 20)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 125), 14, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 125), 15, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(menu_img, (175 - 14, 125), (175 + 14, 125), (255, 255, 255), 1)
        cv2.line(menu_img, (175, 125 - 14), (175, 125 + 14), (255, 255, 255), 1)
        cv2.line(menu_img, (175 - 10, 125 - 10), (175 + 10, 125 + 10), (255, 255, 255), 1)
        cv2.line(menu_img, (175 - 10, 125 + 10), (175 + 10, 125 - 10), (255, 255, 255), 1)
        cv2.circle(menu_img, (175, 125), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (175, 125), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Rear-Right Tyre
        i_rr_tyre = min(200, i_rr_tyre)
        i_rr_tyre = max(0, i_rr_tyre)
        cv2.circle(menu_img, (240, 125), 25, colors_g2r[int(i_rr_tyre / 20)], -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 125), 14, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 125), 15, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(menu_img, (240 - 14, 125), (240 + 14, 125), (255, 255, 255), 1)
        cv2.line(menu_img, (240, 125 - 14), (240, 125 + 14), (255, 255, 255), 1)
        cv2.line(menu_img, (240 - 10, 125 - 10), (240 + 10, 125 + 10), (255, 255, 255), 1)
        cv2.line(menu_img, (240 - 10, 125 + 10), (240 + 10, 125 - 10), (255, 255, 255), 1)
        cv2.circle(menu_img, (240, 125), 6, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (240, 125), 6, (255, 255, 255), 1, cv2.LINE_AA)
        # Acceleration Panel
        cv2.circle(menu_img, (355, 80), 48, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80), 32, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80), 16, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.line(menu_img, (355 - 48, 80), (355 + 48, 80), (255, 255, 255), 1)
        cv2.line(menu_img, (355, 80 - 48), (355, 80 + 48), (255, 255, 255), 1)
        cv2.circle(menu_img, (355 - 16, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 - 16, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 16, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 16, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 16), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 16), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 16), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 16), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 - 32, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 - 32, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 32, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 32, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 32), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 32), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 32), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 32), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 - 48, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 - 48, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 48, 80), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355 + 48, 80), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 48), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 - 48), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 48), 3, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(menu_img, (355, 80 + 48), 3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.line(menu_img, (355 - 75, 80 + 48), (355, 80 + 48), (255, 255, 255), 1)
        f_gx_s, f_gy_s = f_gx, f_gy
        f_gx_s = min(f_gx_s, 3)
        f_gx_s = max(f_gx_s, -3)
        f_gy_s = min(f_gy_s, 3)
        f_gy_s = max(f_gy_s, -3)
        if len(accel_list) >= 10:
            del accel_list[0]
        accel_list.append([f_gy_s, f_gx_s])
        if len(accel_list) >= 10:
            for j in range(9):
                cv2.circle(menu_img, (int(355 + accel_list[j][0] * 16), int(80 + accel_list[j][1] * 16)), 4,
                           (150, 150, 150), -1, cv2.LINE_AA)
            cv2.circle(menu_img, (int(355 + accel_list[-1][0] * 16), int(80 + accel_list[-1][1] * 16)), 4, (255, 144, 30),
                       -1, cv2.LINE_AA)

        # RPM-Rect
        cv2.rectangle(menu_img, (640 - 160, 15), (640 + 160, 35), (30, 30, 30), -1)
        i_rpm_s = min(7500, i_rpm)
        i_rpm_s = max(0, i_rpm_s)
        if i_rpm_s == 7500:
            cv2.rectangle(menu_img, (480, 15), (480 + int(i_rpm_s / 7500 * 320), 35), (0, 69, 255), -1)
        elif i_rpm_s > 6000:
            cv2.rectangle(menu_img, (480, 15), (480 + int(i_rpm_s / 7500 * 320), 35), (0, 215, 255), -1)
        else:
            cv2.rectangle(menu_img, (480, 15), (480 + int(i_rpm_s / 7500 * 320), 35), (255, 255, 255), -1)
        # Steer-Rect
        cv2.rectangle(menu_img, (640 - 160, 130), (640 + 160, 145), (30, 30, 30), -1)
        cv2.line(menu_img, (640, 130), (640, 145), (255, 255, 255), 1)
        cv2.line(menu_img, (640 - 160, 130), (640 - 160, 145), (255, 255, 255), 1)
        cv2.line(menu_img, (640 + 160, 130), (640 + 160, 145), (255, 255, 255), 1)
        if f_psa_pos > 0:
            f_psa_pos_s = min(15, f_psa_pos)
            cv2.rectangle(menu_img, (641, 130), (641 + int(f_psa_pos_s / 15.0 * 158), 145), (255, 144, 30), -1)
        else:
            f_psa_pos_s = max(-15, f_psa_pos)
            cv2.rectangle(menu_img, (639 - int(abs(f_psa_pos_s) / 15.0 * 158), 130), (639, 145), (255, 144, 30), -1)
        # Brake-Rect
        cv2.rectangle(menu_img, (640 - 200, 15), (640 - 180, 145), (30, 30, 30), -1)
        if i_brake > 0:
            x1, y1, x2, y2 = (440, int(15 + 130 * (1 - (i_brake / 100.0))), 460, 145)
            cv2.rectangle(menu_img, (x1, y1), (x2, y2), (0, 0, 255), -1)
        # Throttle-Rect
        cv2.rectangle(menu_img, (640 + 180, 15), (640 + 200, 145), (30, 30, 30), -1)
        if i_throttle > 0:
            x1, y1, x2, y2 = (820, int(15 + 130 * (1 - (i_throttle / 100.0))), 840, 145)
            cv2.rectangle(menu_img, (x1, y1), (x2, y2), (0, 255, 0), -1)
        cv2.line(menu_img, (640 - 40, 45), (640 - 40, 120), (255, 255, 255), 1)
        cv2.line(menu_img, (640 + 40, 45), (640 + 40, 120), (255, 255, 255), 1)
        pil_image = Image.fromarray(cv2.cvtColor(menu_img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        draw.text((32 + cpu_pos_x - len(cpu_fmt.format(f_cpu)) * 3, 8), cpu_fmt.format(f_cpu), font=font,
                  fill=font_color)
        draw.text((32 + cpu_pos_x - len(cpu_text) * 3, 134), cpu_text, font=font, fill=font_color)
        draw.text((32 + ct_pos_x - len(ct_fmt.format(f_cpu_temp)) * 3, 8), ct_fmt.format(f_cpu_temp), font=font,
                  fill=font_color)
        draw.text((32 + ct_pos_x - len(ct_text) * 3, 134), ct_text, font=font, fill=font_color)
        draw.text((32 + mem_pos_x - len(mem_fmt.format(f_mem)) * 3, 8), mem_fmt.format(f_mem), font=font,
                  fill=font_color)
        draw.text((32 + mem_pos_x - len(mem_text) * 3, 134), mem_text, font=font, fill=font_color)
        draw.text((32 + dsk_pos_x - len(dsk_fmt.format(f_disk)) * 3, 8), dsk_fmt.format(f_disk), font=font,
                  fill=font_color)
        draw.text((32 + dsk_pos_x - len(dsk_text) * 3, 134), dsk_text, font=font, fill=font_color)
        draw.text((32 + wt_pos_x - len(wt_fmt.format(f_water_temp)) * 3, 8), wt_fmt.format(f_water_temp), font=font,
                  fill=font_color)
        draw.text((32 + wt_pos_x - len(wt_text) * 3, 134), wt_text, font=font, fill=font_color)
        draw.text((32 + le_pos_x - len(le_fmt.format(f_lateral_err)) * 3, 8), le_fmt.format(f_lateral_err),
                  font=font, fill=font_color)
        draw.text((32 + le_pos_x - len(le_text) * 3, 134), le_text, font=font, fill=font_color)

        # Front-Left Brake Disc
        draw.text((27, 3), str(i_fl_disc) + '`C', font=font, fill=font_color)
        # Front-Right Brake Disc
        draw.text((88, 3), str(i_fr_disc) + '`C', font=font, fill=font_color)
        # Rear-Left Brake Disc
        draw.text((27, 78), str(i_rl_disc) + '`C', font=font, fill=font_color)
        # Rear-Right Brake Disc
        draw.text((88, 78), str(i_rr_disc) + '`C', font=font, fill=font_color)
        # Front-Left Tyre
        draw.text((160, 3), str(i_fl_tyre) + '`C', font=font, fill=font_color)
        # Front-Right Tyre
        draw.text((222, 3), str(i_fr_tyre) + '`C', font=font, fill=font_color)
        # Rear-Left Tyre
        draw.text((160, 78), str(i_rl_tyre) + '`C', font=font, fill=font_color)
        # Rear-Right Tyre
        draw.text((222, 78), str(i_rr_tyre) + '`C', font=font, fill=font_color)
        # Acceleration Panel
        f_gx_t = max(0, f_gx)
        draw.text((345, 10), "{:.1f}".format(f_gx_t), font=font, fill=font_color)
        f_gx_t = min(0, f_gx)
        f_gx_t = abs(f_gx_t)
        draw.text((345, 130), "{:.1f}".format(f_gx_t), font=font, fill=font_color)
        f_gy_t = max(0, f_gy)
        draw.text((410, 70), "{:.1f}".format(f_gy_t), font=font, fill=font_color)
        f_gy_t = min(0, f_gy)
        f_gy_t = abs(f_gy_t)
        draw.text((280, 70), "{:.1f}".format(f_gy_t), font=font, fill=font_color)
        draw.text((280, 108), "3.0G", font=font, fill=font_color)

        draw.text((640 - 15, 25), str(i_gear), font=font_big, fill=font_color)
        draw.text((640 - 20, 95), "Gear", font=font_20, fill=font_color)
        text_width = draw.textlength(str(i_speed), font=font_big)
        draw.text((640 - 60 - text_width, 25), str(i_speed), font=font_big, fill=font_color)
        draw.text((640 - 120, 95), "KM/H", font=font_20, fill=font_color)
        draw.text((640 + 56, 30), str(i_rpm), font=font_50, fill=font_color)
        draw.text((640 + 70, 95), "RPM", font=font_20, fill=font_color)

        draw.text((640 - 170, 110), "-15", font=font, fill=font_color)
        draw.text((640 + 145, 110), "+15", font=font, fill=font_color)
        menu_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        img_show_[-show_h:, :show_w] = menu_img
        img = img_show_
        """
        if 'bar_chart_items' in visual_msg:
            for item in visual_msg['bar_chart_items']:  # chart
                posx = item['posx']
                val = item['val']
                val_min = item['val_min']
                val_max = item['val_max']
                if val < val_min:
                    val = val_min
                if val > val_max:
                    val = val_max
                x, y, w, h = (30 + posx, 30, 10, 60)
                cv2.rectangle(menu_img, (x, y), (x + w, y + h), (255, 255, 255), 1)
                x, y, w, h = (30 + posx, int(30 + 60 * (val_max - val) / val_max), 10, int(60 * val / val_max))
                cv2.rectangle(menu_img, (x, y), (x + w, y + h), (255, 255, 255), -1)

            pil_image = Image.fromarray(cv2.cvtColor(menu_img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            for item in visual_msg['bar_chart_items']:  # text
                posx = item['posx']
                text = item['title_refresh']
                name = item['title']
                val = item['val']
                val_min = item['val_min']
                val_max = item['val_max']
                if val < val_min:
                    val = val_min
                if val > val_max:
                    val = val_max
                draw.text((32 + posx - len(text.format(val)) * 3, 8), text.format(val), font=font, fill=font_color)
                draw.text((32 + posx - len(name) * 3, 94), name, font=font, fill=font_color)

            time_str = datetime.now().strftime("%H:%M:%S")
            draw.text((640 - 100, 20), time_str, font=font_big, fill=font_color)
            menu_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        img_show_[-show_h:, :show_w] = menu_img
        img = img_show_
        """

    return img


g_track_left = None
g_track_bottom = None
g_track_height = None


def track_coordinate_convert(pts, left=None, bottom=None, height=None, margin_=100) -> np.ndarray:
    global g_track_left, g_track_bottom, g_track_height
    assert g_track_left is not None or left is not None
    assert g_track_bottom is not None or bottom is not None
    assert g_track_height is not None or height is not None
    if g_track_left is None:
        g_track_left = left
    if g_track_bottom is None:
        g_track_bottom = bottom
    if g_track_height is None:
        g_track_height = height
    pts[:, 0] += (0 - g_track_left) + margin_
    pts[:, 1] += (0 - g_track_bottom) + margin_
    pts[:, 1] = g_track_height - pts[:, 1]
    return pts


def track_boundary_parse():
    # traj_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/trajectories.csv')
    traj_right_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/yas_full_right.csv')
    traj_left_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../res/yas_full_left.csv')
    left_line = []
    right_line = []
    mid_line = []
    f_right = open(traj_right_path, 'r')
    f_left = open(traj_left_path, 'r')
    csv_list = csv.reader(f_right)
    for i, csv_row in enumerate(csv_list):
        if i > 0:
            right_line.append([csv_row[0], csv_row[1]])
    f_right.close()
    csv_list = csv.reader(f_left)
    for i, csv_row in enumerate(csv_list):
        if i > 0:
            left_line.append([csv_row[0], csv_row[1]])
    f_left.close()
    """
    with open(traj_path, 'r') as f:
        csv_list = csv.reader(f)
        for i, csv_row in enumerate(csv_list):
            if i > 0:
                # left_line.append([csv_row[0], csv_row[1]])  # x, y
                # right_line.append([csv_row[2], csv_row[3]])
                mid_line.append([csv_row[4], csv_row[5]])
    """
    left_line = np.array(left_line, dtype=np.float32)
    right_line = np.array(right_line, dtype=np.float32)
    # mid_line = np.array(mid_line, dtype=np.float32)
    line_left = left_line[:, 0].min()
    line_bottom = left_line[:, 1].min()
    line_right = left_line[:, 0].max()
    line_top = left_line[:, 1].max()
    margin = 100
    w, h = (line_right - line_left) + 2 * margin, (line_top - line_bottom) + 2 * margin

    # pts = track_coordinate_convert(mid_line, line_left, line_bottom, h, margin).astype(np.int32)
    left_line = track_coordinate_convert(left_line, line_left, line_bottom, h, margin).astype(np.int32)
    right_line = track_coordinate_convert(right_line).astype(np.int32)

    img = np.zeros((int(h), int(w), 3), np.uint8)
    # img_sml = np.zeros((int(h / 2), int(w / 2), 3), np.uint8)
    # img_big = np.zeros((int(h) * 2, int(w) * 2, 3), np.uint8)
    """
    for pt in pts:
        img = cv2.circle(img, pt, 4, (255, 255, 255), -1)
    for pt in left_line:
        img = cv2.circle(img, pt, 4, (255, 0, 0), -1)
    """
    # img = cv2.polylines(img, [pts], True, (255, 255, 255), 1)
    """
    left_line_big = np.array([[pt[0] * 2, pt[1] * 2] for pt in left_line], dtype=np.int32)
    right_line_big = np.array([[pt[0] * 2, pt[1] * 2] for pt in right_line], dtype=np.int32)
    mg_big = cv2.polylines(img_big, [left_line_big], True, (255, 255, 255), 1, cv2.LINE_AA)
    img_big = cv2.polylines(img_big, [right_line_big], True, (255, 255, 255), 1, cv2.LINE_AA)

    left_line_sml = np.array([[pt[0] / 2, pt[1] / 2] for pt in left_line], dtype=np.int32)
    right_line_sml = np.array([[pt[0] / 2, pt[1] / 2] for pt in right_line], dtype=np.int32)
    img_sml = cv2.polylines(img_sml, [left_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
    img_sml = cv2.polylines(img_sml, [right_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
    """
    img = cv2.polylines(img, [left_line], True, (255, 255, 255), 1, cv2.LINE_AA)
    img = cv2.polylines(img, [right_line], True, (255, 255, 255), 1, cv2.LINE_AA)

    # img = cv2.resize(img, (int(img.shape[1] / 3), int(img.shape[0] / 3)))
    # cv2.imwrite('C:/deep/track.png', img)
    # cv2.imshow("img", img)
    return left_line, right_line, (int(w), int(h))


def draw_track_map(
    img: np.ndarray,
    left_line: np.ndarray,
    right_line: np.ndarray,
    map_size: tuple,
    localization: tuple,
    orientation_z: float,
    velocity: float,
    acceleration: float,
    code19_info: tuple
):
    if len(img.shape) == 3 and img.shape[0] == 720 and img.shape[1] == 1280:
        img_show_ = img.copy()
        # 316, 600
        draw_map_h = 599
        draw_map_w = 316
        if True:
            full_map_h = draw_map_h * 8
            full_map_w = draw_map_w * 8
            scale_x = full_map_w / map_size[0]
            scale_y = full_map_h / map_size[1]
            map_mask = np.zeros((full_map_h, full_map_w, 3), dtype=np.uint8)

            left_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in left_line], dtype=np.int32)
            right_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in right_line], dtype=np.int32)
            map_mask = cv2.polylines(map_mask, [left_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
            map_mask = cv2.polylines(map_mask, [right_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
            loc = np.array([localization]).astype(np.float64)
            loc = track_coordinate_convert(loc)
            loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in loc], dtype=np.int32)
            pt = loc[0]
            map_mask = cv2.circle(map_mask, pt, 4, (0, 0, 255), -1, cv2.LINE_AA)

            pil_image = Image.fromarray(cv2.cvtColor(map_mask, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            draw.text((pt[0], pt[1] - 30), "{:.2f} m/s".format(velocity), font=font, fill=font_color)
            draw.text((pt[0], pt[1] - 50), "{:.2f} m/s^2".format(acceleration), font=font, fill=font_color)
            map_mask = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            # [10, 0]
            r = 20
            arrow_x = int(np.cos(orientation_z) * r)
            arrow_y = int(np.sin(-orientation_z) * r)
            map_mask = cv2.line(map_mask, pt, (pt[0] + arrow_x, pt[1] + arrow_y), (0, 255, 255), 1, cv2.LINE_AA)
            x1 = pt[0] - draw_map_w / 2
            x2 = pt[0] + draw_map_w / 2
            y1 = pt[1] - draw_map_h / 2
            y2 = pt[1] + draw_map_h / 2
            if x1 < 0:
                x1 = 0
                x2 = draw_map_w
            if y1 < 0:
                y1 = 0
                y2 = draw_map_h
            if x2 > full_map_w:
                x2 = full_map_w
                x1 = full_map_w - draw_map_w
            if y2 > full_map_h:
                y2 = full_map_h
                y1 = full_map_h - draw_map_h
            map_mask = map_mask[int(y1): int(y2), int(x1): int(x2)]
            img_map = img_show_[:draw_map_h, -draw_map_w:]
            # print(map_mask.shape)
            # print(img_map.shape)
            img_map = cv2.addWeighted(img_map, 0.5, map_mask, 0.5, 0)
            img_show_[:draw_map_h, -draw_map_w:] = img_map
            # img = img_show_
        if True:
            scale_x = draw_map_w / map_size[0]
            scale_y = draw_map_h / map_size[1]

            img_map = img_show_[:draw_map_h, :draw_map_w]
            map_mask = np.zeros_like(img_map, dtype=np.uint8)
            img_map = cv2.addWeighted(img_map, 0.5, map_mask, 0.5, 0)

            left_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in left_line], dtype=np.int32)
            right_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in right_line], dtype=np.int32)
            img_map = cv2.polylines(img_map, [left_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
            img_map = cv2.polylines(img_map, [right_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)

            loc = np.array([localization]).astype(np.float64)
            loc = track_coordinate_convert(loc)
            loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in loc], dtype=np.int32)
            ptfe = loc[0]
            img_map = cv2.circle(img_map, ptfe, 4, (0, 0, 255), -1, cv2.LINE_AA)
            img_map = cv2.circle(img_map, ptfe, 4, (0, 0, 0), 1, cv2.LINE_AA)

            code19_loc = np.array([[code19_info[0], code19_info[1]]]).astype(np.float64)
            code19_loc = track_coordinate_convert(code19_loc)
            code19_loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in code19_loc], dtype=np.int32)
            pt19 = code19_loc[0]
            img_map = cv2.circle(img_map, pt19, 4, (255, 0, 0), -1, cv2.LINE_AA)
            img_map = cv2.circle(img_map, pt19, 4, (0, 0, 0), 1, cv2.LINE_AA)

            pil_image = Image.fromarray(cv2.cvtColor(img_map, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            draw.text((ptfe[0], ptfe[1] - 30), "{:.2f} m/s".format(velocity), font=font, fill=font_color)
            draw.text((pt19[0], pt19[1] - 30), "{:.2f} m/s".format(code19_info[2]), font=font, fill=font_color)
            img_map = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            img_show_[:draw_map_h, :draw_map_w] = img_map
            img = img_show_
    return img


def draw_track_map_v2(
    img: np.ndarray,
    left_line: np.ndarray,
    right_line: np.ndarray,
    map_size: tuple,
    visual_msg
):
    if len(img.shape) == 3 and img.shape[0] == 720 and img.shape[1] == 1280:
        img_show_ = img.copy()
        # 316, 600

        localization = [-122.2, -627.5, 0]
        velocity = 0
        acceleration = 0
        orientation_z = 0
        slip_f = 0
        slip_r = 0
        safe_stop_mode = 0
        reason = ''

        f_s_flag = 0.0
        f_s_distance = 0.0
        f_s_cure = 100.0
        f_real_perc = 0.0
        i_lap_count = 0
        i_kistler_status = 0
        if visual_msg is not None:
            """
            if 'velocity_body_ins' in visual_msg:
                velocity = visual_msg['velocity_body_ins'][0]
            if 'position_enu_ins' in visual_msg:
                localization = visual_msg['position_enu_ins']
            if 'acceleration_ins' in visual_msg:
                acceleration = visual_msg['acceleration_ins'][0]
            if 'orientation_ypr' in visual_msg:
                orientation_z = visual_msg['orientation_ypr'][2]
            """
            if 'ego_velocity' in visual_msg:
                velocity = visual_msg['ego_velocity'][0]
            if 'ego_position' in visual_msg:
                localization = visual_msg['ego_position']
            if 'ego_acceleration' in visual_msg:
                acceleration = visual_msg['ego_acceleration'][0]
            if 'ego_orientation_ypr' in visual_msg:
                orientation_z = visual_msg['ego_orientation_ypr'][2]
            if 'slip_f' in visual_msg:
                slip_f = visual_msg['slip_f']
            if 'slip_r' in visual_msg:
                slip_r = visual_msg['slip_r']
            if 'safe_stop_mode' in visual_msg:
                safe_stop_mode = visual_msg['safe_stop_mode']
            if 'reason_for_safestop' in visual_msg:
                reason = visual_msg['reason_for_safestop']
            if 's_flag' in visual_msg:
                f_s_flag = visual_msg['s_flag']
            if 's_distance' in visual_msg:
                f_s_distance = visual_msg['s_distance']
            if 's_cure' in visual_msg:
                f_s_cure = visual_msg['s_cure']
            if 'real_perc' in visual_msg:
                f_real_perc = visual_msg['real_perc']
            if 'lap_count' in visual_msg:
                i_lap_count = visual_msg['lap_count']
            if 'kistler_status' in visual_msg:
                i_kistler_status = visual_msg['kistler_status']

        draw_map_h = 279  # 599
        draw_map_w = 295  # 316
        img_map = img_show_[280: 280 + draw_map_h, -draw_map_w:]
        map_mask = np.zeros_like(img_map, dtype=np.uint8)
        img_map = cv2.addWeighted(img_map, 0.5, map_mask, 0.5, 0)

        pil_image = Image.fromarray(cv2.cvtColor(img_map, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        draw_red_f2s = False
        draw_red_r2s = False
        if slip_f > 0.15:
            draw_red_f2s = True
        if slip_r > 0.15:
            draw_red_r2s = True
        if draw_red_f2s:
            draw.text((10, 10), "slip_f: {:.2f}".format(slip_f), font=font, fill=(255, 0, 0))
        else:
            draw.text((10, 10), "slip_f: {:.2f}".format(slip_f), font=font, fill=font_color)
        if draw_red_r2s:
            draw.text((100, 10), "slip_r: {:.2f}".format(slip_r), font=font, fill=(255, 0, 0))
        else:
            draw.text((100, 10), "slip_r: {:.2f}".format(slip_r), font=font, fill=font_color)
        draw.text((10, 35), "s_flag: {}".format(int(f_s_flag)), font=font, fill=font_color)
        draw.text((10, 60), "s_distance: {:.3f}".format(f_s_distance), font=font, fill=font_color)
        draw.text((10, 85), "s_curt: {:.3f}".format(f_s_cure), font=font, fill=font_color)
        # f_real_perc
        draw.text((10, 110), "real_perc: {}".format(int(f_real_perc)), font=font, fill=font_color)
        draw.text((10, 135), "lap_count: {}".format(int(i_lap_count)), font=font, fill=font_color)

        # i_kistler_status
        if i_kistler_status == 1:
            draw.text((10, 160), "Kistler ON", font=font, fill=(0, 255, 0))
        else:
            draw.text((10, 160), "Kistler OFF", font=font, fill=(255, 0, 0))

        if safe_stop_mode == 0:
            draw.text((10, 205), "safe_stop_mode: {}".format(safe_stop_mode), font=font, fill=(60, 179, 113))
        else:
            draw.text((10, 205), "safe_stop_mode: {}".format(safe_stop_mode), font=font, fill=(255, 69, 0))
            draw.text((10, 225), "reason:", font=font, fill=(255, 69, 0))
            if len(reason) > 65:
                draw.text((10, 245), "{}-".format(reason[:65]), font=font_s, fill=(255, 69, 0))
                draw.text((10, 257), "-{}".format(reason[65:]), font=font_s, fill=(255, 69, 0))
            else:
                draw.text((10, 245), "{}".format(reason), font=font_s, fill=(255, 69, 0))
        img_map = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        img_show_[280: 280 + draw_map_h, -draw_map_w:] = img_map
        if True:
            draw_map_h = 279  # 599
            draw_map_w = 295  # 316
            full_map_h = draw_map_h * 12
            full_map_w = draw_map_w * 12
            scale_x = full_map_w / map_size[0]
            scale_y = full_map_h / map_size[1]

            global full_map_mask
            if full_map_mask is None:
                full_map_mask = np.zeros((full_map_h, full_map_w, 3), dtype=np.uint8)

                left_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in left_line], dtype=np.int32)
                right_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in right_line], dtype=np.int32)
                full_map_mask = cv2.polylines(full_map_mask, [left_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
                full_map_mask = cv2.polylines(full_map_mask, [right_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)

            map_mask = full_map_mask.copy()

            loc = np.array([localization]).astype(np.float64)
            loc = track_coordinate_convert(loc)
            loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in loc], dtype=np.int32)
            pt = loc[0]

            x1 = pt[0] - draw_map_w / 2
            x2 = pt[0] + draw_map_w / 2
            y1 = pt[1] - draw_map_h / 2
            y2 = pt[1] + draw_map_h / 2
            if x1 < 0:
                x1 = 0
                x2 = draw_map_w
            if y1 < 0:
                y1 = 0
                y2 = draw_map_h
            if x2 > full_map_w:
                x2 = full_map_w
                x1 = full_map_w - draw_map_w
            if y2 > full_map_h:
                y2 = full_map_h
                y1 = full_map_h - draw_map_h
            map_mask = map_mask[int(y1): int(y2), int(x1): int(x2)]
            img_map = img_show_[:draw_map_h, -draw_map_w:]
            # print(map_mask.shape)
            # print(img_map.shape)
            img_map = cv2.addWeighted(img_map, 0.5, map_mask, 0.5, 0)

            img_map = cv2.circle(img_map, (int(pt[0] - x1), int(pt[1] - y1)), 4, (0, 0, 255), -1,
                                 cv2.LINE_AA)
            # map_mask = cv2.circle(map_mask, pt, 5, (255, 255, 255), 1, cv2.LINE_AA)

            pil_image = Image.fromarray(cv2.cvtColor(img_map, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            draw.text((int(pt[0] - x1), int(pt[1] - y1) - 30), "{:.2f} m/s".format(velocity),
                      font=font, fill=font_color)
            draw.text((int(pt[0] - x1), int(pt[1] - y1) - 50), "{:.2f} m/s^2".format(acceleration),
                      font=font, fill=font_color)
            img_map = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            # [10, 0]
            r = 20
            arrow_x = int(np.cos(orientation_z) * r)
            arrow_y = int(np.sin(-orientation_z) * r)
            img_map = cv2.line(img_map, (int(pt[0] - x1), int(pt[1] - y1)),
                               (int(pt[0] - x1) + arrow_x, int(pt[1] - y1) + arrow_y),
                               (0, 255, 255), 1, cv2.LINE_AA)

            img_show_[:draw_map_h, -draw_map_w:] = img_map
            # img = img_show_
        if True:
            draw_map_h = 559  # 599
            draw_map_w = 295  # 316
            scale_x = draw_map_w / map_size[0]
            scale_y = draw_map_h / map_size[1]

            img_map = img_show_[:draw_map_h, :draw_map_w]
            map_mask = np.zeros_like(img_map, dtype=np.uint8)
            img_map = cv2.addWeighted(img_map, 0.5, map_mask, 0.5, 0)

            left_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in left_line], dtype=np.int32)
            right_line_sml = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in right_line], dtype=np.int32)
            img_map = cv2.polylines(img_map, [left_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)
            img_map = cv2.polylines(img_map, [right_line_sml], True, (255, 255, 255), 1, cv2.LINE_AA)

            loc = np.array([localization]).astype(np.float64)
            loc = track_coordinate_convert(loc)
            loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in loc], dtype=np.int32)
            ptfe = loc[0]
            img_map = cv2.circle(img_map, ptfe, 6, (0, 0, 255), -1, cv2.LINE_AA)
            img_map = cv2.circle(img_map, ptfe, 7, (255, 255, 255), 1, cv2.LINE_AA)

            """
            code19_loc = np.array([[code19_info[0], code19_info[1]]]).astype(np.float64)
            code19_loc = track_coordinate_convert(code19_loc)
            code19_loc = np.array([[pt[0] * scale_x, pt[1] * scale_y] for pt in code19_loc], dtype=np.int32)
            pt19 = code19_loc[0]
            img_map = cv2.circle(img_map, pt19, 4, (255, 0, 0), -1, cv2.LINE_AA)
            img_map = cv2.circle(img_map, pt19, 4, (0, 0, 0), 1, cv2.LINE_AA)
            """

            pil_image = Image.fromarray(cv2.cvtColor(img_map, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            draw.text((ptfe[0], ptfe[1] - 30), "{:.2f} m/s".format(velocity), font=font, fill=font_color)
            # draw.text((pt19[0], pt19[1] - 30), "{:.2f} m/s".format(code19_info[2]), font=font, fill=font_color)

            draw.text((10, 5), "Team Fly Eagle", font=font, fill=font_color)
            draw.text((167, 5), "Yas Marina Circuit", font=font, fill=font_color)
            # time_str = datetime.now().strftime("")
            # draw.text((10, 500), time_str, font=font, fill=font_color)
            time_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
            draw.text((10, 530), time_str, font=font, fill=font_color)
            img_map = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


            img_show_[:draw_map_h, :draw_map_w] = img_map
            img = img_show_
    return img


if __name__ == '__main__':
    _left_line, _right_line, (_w, _h) = track_boundary_parse()
    print(_left_line.shape)
    print(_right_line.shape)
    print(_w, _h)
    draw_track_map(np.zeros((720, 1280, 3), dtype=np.uint8), _left_line, _right_line, (_w, _h), (0, 0))
