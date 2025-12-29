import sys
import os
import json5

ASSET_FOLDER = 'imgs'
CONFIG_FILE = 'config.json5'

DEFAULT_CONFIG = {
    "WATER_COOLDOWN_MINUTES": 60,
    "TIMEOUT_FARMING_LOOP": 35,
    "TIMEOUT_PLANTING": 13,
    "TIMEOUT_HOMING": 10,
    "TIMEOUT_FRUIT_HOMING": 10,
    "TIMEOUT_FRUIT_PLANT": 20,
    "TIMEOUT_FRUIT_WATER": 40,
    "NETWORK_RECOVERY_BUFFER": 10,
    "TIMEOUT_ENTER_GAME_MAX": 360,
    "TIMEOUT_LAUNCHER_RESTORE": 300,
    "TIMEOUT_LOADING_STUCK": 60,
    "CLICK_CONFIDENCE_THRESHOLD": 0.6,
    "CHECK_CONFIDENCE_THRESHOLD": 0.7,
    "LAUNCHER_CONFIDENCE": 0.6,
    "ACTION_TIMINGS": {
        "move_step_water_fruit": [0.5, 0.8],
        "move_step_water_normal": [0.4, 0.45],
        "move_step_harvest": [0.4, 0.45],
        "move_step_plant_fruit": [1.4, 2.4],
        "move_step_plant_normal": [1.4, 1.8],
        "wait_after_water_fruit": [0.4, 0.5],
        "wait_after_water_normal": [0.15, 0.35],
        "wait_after_harvest": [0.2, 0.35],
        "wait_after_plant": [0.5, 0.8],
        "water_hold_duration": [0.15, 0.3],
        "key_press_short": [0.15, 0.25],
        "key_press_turn": [0.20, 0.30],
        "sleep_short": [0.4, 0.6],
        "sleep_medium": [0.8, 1.2],
        "sleep_long": [1.8, 2.3]
    },
    "templates": {
        "launcher_window": ['launcher_window_01.png', 'launcher_window_02.png', 'launcher_window_03.png', 'launcher_window_04.png', 'launcher_window_05.png', 'launcher_window_06.png', 'launcher_window_07.png', 'launcher_window_08.png'],
        "game_logo": ['game_logo_01.png', 'game_logo_02.png', 'game_logo_03.png', 'game_logo_04.png', 'game_logo_05.png', 'game_logo_06.png'],
        "ingame_check": ['ingame_view_01.png', 'ingame_view_02.png', 'ingame_view_03.png', 'ingame_view_04.png', 'ingame_view_05.png', 'ingame_view_06.png', 'ingame_view_07.png', 'ingame_view_08.png', 'ingame_view_09.png', 'ingame_view_10.png', 'ingame_view_11.png', 'ingame_view_12.png'],
        "wall_front": ['wall_front_01.png', 'wall_front_02.png', 'wall_front_03.png', 'wall_front_04.png', 'wall_front_05.png', 'wall_front_06.png', 'wall_front_07.png', 'wall_front_08.png'],
        "wall_back": ['wall_back_01.png', 'wall_back_02.png', 'wall_back_03.png', 'wall_back_04.png', 'wall_back_05.png', 'wall_back_06.png', 'wall_back_07.png', 'wall_back_08.png'],
        "launcher_start": ['btn_launcher_start_01.png', 'btn_launcher_start_02.png', 'btn_launcher_start_03.png', 'btn_launcher_start_04.png'],
        "click_enter": ['click_enter_01.png', 'click_enter_02.png', 'click_enter_03.png', 'click_enter_04.png'],
        "loading": ['mark_loading_01.png', 'mark_loading_02.png', 'mark_loading_03.png', 'mark_loading_04.png'],
        "mature": ['mark_mature_01.png', 'mark_mature_02.png', 'mark_mature_03.png', 'mark_mature_04.png'],
        "exit_icon": ['btn_exit_icon_01.png', 'btn_exit_icon_02.png', 'btn_exit_icon_03.png', 'btn_exit_icon_04.png'],
        "exit_confirm": ['btn_exit_confirm_01.png', 'btn_exit_confirm_02.png', 'btn_exit_confirm_03.png', 'btn_exit_confirm_04.png']
    }
}

DEFAULT_CONFIG_CONTENT = """{
    // === 基础超时设置 (单位: 秒) ===
    "WATER_COOLDOWN_MINUTES": 60,
    "TIMEOUT_FARMING_LOOP": 35,
    "TIMEOUT_PLANTING": 15,
    "TIMEOUT_HOMING": 10,
    "TIMEOUT_FRUIT_HOMING": 10,
    "TIMEOUT_FRUIT_PLANT": 15,
    "TIMEOUT_FRUIT_WATER": 40,

    // === 系统与网络设置 ===
    "NETWORK_RECOVERY_BUFFER": 10,
    "TIMEOUT_ENTER_GAME_MAX": 360,
    "TIMEOUT_LAUNCHER_RESTORE": 300,
    "TIMEOUT_LOADING_STUCK": 60,

    // === 图像识别阈值 (0.1 - 1.0) ===
    "CLICK_CONFIDENCE_THRESHOLD": 0.6,
    "CHECK_CONFIDENCE_THRESHOLD": 0.7,
    "LAUNCHER_CONFIDENCE": 0.6,

    // === 动作时间随机区间配置 [最小值, 最大值] (单位: 秒) ===
    "ACTION_TIMINGS": {
        "move_step_water_fruit": [0.5, 0.8],
        "move_step_water_normal": [0.4, 0.45],
        "move_step_harvest": [0.4, 0.45],
        "move_step_plant_fruit": [1.4, 2.4],
        "move_step_plant_normal": [1.4, 1.8],
        "wait_after_water_fruit": [0.3, 0.5],
        "wait_after_water_normal": [0.15, 0.35],
        "wait_after_harvest": [0.2, 0.35],
        "wait_after_plant": [0.5, 0.8],
        "water_hold_duration": [0.15, 0.3],
        "key_press_short": [0.15, 0.25],
        "key_press_turn": [0.20, 0.30],
        "sleep_short": [0.4, 0.6],
        "sleep_medium": [0.8, 1.2],
        "sleep_long": [1.8, 2.3]
    },

    // === 图片模板路径配置 ===
    "templates": {
        "launcher_window": ["launcher_window_01.png", "launcher_window_02.png", "launcher_window_03.png", "launcher_window_04.png", "launcher_window_05.png", "launcher_window_06.png", "launcher_window_07.png", "launcher_window_08.png"],
        "game_logo": ["game_logo_01.png", "game_logo_02.png", "game_logo_03.png", "game_logo_04.png", "game_logo_05.png", "game_logo_06.png"],
        "ingame_check": ["ingame_view_01.png", "ingame_view_02.png", "ingame_view_03.png", "ingame_view_04.png", "ingame_view_05.png", "ingame_view_06.png", "ingame_view_07.png", "ingame_view_08.png", "ingame_view_09.png", "ingame_view_10.png", "ingame_view_11.png", "ingame_view_12.png"],
        "wall_front": ["wall_front_01.png", "wall_front_02.png", "wall_front_03.png", "wall_front_04.png", "wall_front_05.png", "wall_front_06.png", "wall_front_07.png", "wall_front_08.png"],
        "wall_back": ["wall_back_01.png", "wall_back_02.png", "wall_back_03.png", "wall_back_04.png", "wall_back_05.png", "wall_back_06.png", "wall_back_07.png", "wall_back_08.png"],
        "launcher_start": ["btn_launcher_start_01.png", "btn_launcher_start_02.png", "btn_launcher_start_03.png", "btn_launcher_start_04.png"],
        "click_enter": ["click_enter_01.png", "click_enter_02.png", "click_enter_03.png", "click_enter_04.png"],
        "loading": ["mark_loading_01.png", "mark_loading_02.png", "mark_loading_03.png", "mark_loading_04.png"],
        "mature": ["mark_mature_01.png", "mark_mature_02.png", "mark_mature_03.png", "mark_mature_04.png"],
        "exit_icon": ["btn_exit_icon_01.png", "btn_exit_icon_02.png", "btn_exit_icon_03.png", "btn_exit_icon_04.png"],
        "exit_confirm": ["btn_exit_confirm_01.png", "btn_exit_confirm_02.png", "btn_exit_confirm_03.png", "btn_exit_confirm_04.png"]
    }
}"""

def _recursive_update(default_dict, user_dict):
    """递归更新字典，补全缺失的键"""
    for key, value in user_dict.items():
        if key in default_dict:
            if isinstance(value, dict) and isinstance(default_dict[key], dict):
                _recursive_update(default_dict[key], value)
            else:
                default_dict[key] = value

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def load_and_validate_config(log_func=None):
    config = DEFAULT_CONFIG.copy()
    base_path = get_base_path()
    config_path = os.path.join(base_path, CONFIG_FILE)
    
    file_exists = os.path.exists(config_path)

    if file_exists:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json5.load(f)
            _recursive_update(config, user_config)
            if log_func: log_func("配置文件读取成功 (JSON5)。", "green")
        except Exception as e:
            if log_func: log_func(f"配置文件读取失败: {e}，将使用默认值。", "darkorange")
    else:
        if log_func: log_func("未检测到配置文件，将生成默认配置。", "blue")

    try:
        if not file_exists:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(DEFAULT_CONFIG_CONTENT)
    except Exception as e:
        if log_func: log_func(f"无法保存配置文件: {e}", "red")
        
    return config

def get_img_paths(config_dict, key):
    """从配置中获取图片的绝对路径列表"""
    base_path = get_base_path()
    filenames = config_dict['templates'].get(key, [])
    if not filenames: return []
    if isinstance(filenames, str): filenames = [filenames]
    
    return [os.path.join(base_path, ASSET_FOLDER, f) for f in filenames]