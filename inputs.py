import math
import time
import random
import pydirectinput
import pyautogui

# 默认 PAUSE (由脚本控制延迟)
pydirectinput.PAUSE = 0 

def _linear_move_steps(x1, y1, x2, y2, step_pixels, sleep_base):
    """辅助函数：分段线性移动"""
    try:
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < 1: return
        
        steps = int(dist / step_pixels)
        if steps < 1: steps = 1
        
        for i in range(1, steps + 1):
            t = i / steps
            current_x = x1 + (x2 - x1) * t
            current_y = y1 + (y2 - y1) * t
            
            pydirectinput.moveTo(int(current_x), int(current_y))
            
            if sleep_base > 0:
                time.sleep(sleep_base + random.uniform(0, 0.002))
    except Exception:
        pass

def human_move_to(x, y):
    """模拟人类操作：快速直线移动到附近 -> 慢速直线定位到目标"""
    try:
        start_x, start_y = pyautogui.position()
        
        end_x = x + random.randint(-2, 2)
        end_y = y + random.randint(-2, 2)
        
        dist = math.hypot(end_x - start_x, end_y - start_y)
        
        if dist < 150:
            _linear_move_steps(start_x, start_y, end_x, end_y, step_pixels=100, sleep_base=0.002)
            return

        # 1. 快速逼近阶段 (粗定位)
        ratio = random.uniform(0.75, 0.85)
        mid_x = start_x + (end_x - start_x) * ratio + random.randint(-15, 15)
        mid_y = start_y + (end_y - start_y) * ratio + random.randint(-15, 15)
        
        _linear_move_steps(start_x, start_y, mid_x, mid_y, step_pixels=200, sleep_base=0.001)
        
        move_interval = random.uniform(0.05, 0.3)
        time.sleep(move_interval)

        # 2. 慢速定位阶段 (精定位)
        _linear_move_steps(mid_x, mid_y, end_x, end_y, step_pixels=100, sleep_base=0.002)
        
    except Exception:
        try:
            pydirectinput.moveTo(x, y)
        except:
            pass

def robust_click(x, y, is_double=False):
    human_move_to(x, y)
    time.sleep(random.uniform(0.1, 0.3))
    
    clicks = 2 if is_double else 1
    for i in range(clicks):
        pydirectinput.mouseDown()
        time.sleep(random.uniform(0.05, 0.15))
        pydirectinput.mouseUp()
        
        if is_double and i == 0:
            time.sleep(random.uniform(0.04, 0.1))
    
    time.sleep(random.uniform(0.1, 0.3))