import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QLineEdit, 
                             QCheckBox, QPushButton, QTextEdit, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from worker import FarmWorker
import config_manager as cm

class FarmGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("无限暖暖家园种植小助手 v1.48")
        self.resize(350, 750)
        self.setMinimumSize(100, 200)
        self.setMaximumSize(960, 1000)
        
        base_path = cm.get_base_path()
        icon_path = os.path.join(base_path, cm.ASSET_FOLDER, 'logo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 13px;")
        
        self.init_ui()
        self.worker = None

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. 顶部提示区
        tip_box = QGroupBox("注意事项")
        tip_layout = QVBoxLayout()
        tips = """在进入游戏前：
1.请先按照要求摆放好田地，并调整好视角。
2.切换能力为种植能力，并持有足够多的种子。
3.确保已切换浇水药水为免费药水。
4.确保游戏启动器已经启动。
5.运行脚本后不要最小化游戏，不要动鼠标和键盘。
6.确保图片素材已放入 'imgs' 文件夹。
7.对于果树类作物(类型6和7)，脚本程序仅支持播种和浇水操作。"""
        tip_label = QLabel(tips)
        tip_label.setWordWrap(True)
        tip_label.setStyleSheet("color: #FF6347;")
        tip_layout.addWidget(tip_label)
        tip_box.setLayout(tip_layout)
        main_layout.addWidget(tip_box)

        # 2. 作物设置区
        setting_box = QGroupBox("作物设置")
        setting_layout = QVBoxLayout()
        
        setting_layout.addWidget(QLabel("选择作物类型："))
        self.combo_crop = QComboBox()
        self.crop_options = {
            '1': "杯杯香 (30分钟成熟作物通用)",
            '2': "铃铃草 (1小时成熟作物通用)",
            '3': "蓬蓬兰 (2小时成熟作物通用)",
            '4': "迷迭枝 (3小时成熟作物通用)",
            '5': "团团花 (6小时成熟作物通用)",
            '6': "叮当果树 (10小时成熟作物通用)",
            '7': "织云树 (20小时成熟作物通用)"
        }
        for k in sorted(self.crop_options.keys()):
            self.combo_crop.addItem(f"{k}. {self.crop_options[k]}", k)
        self.combo_crop.setCurrentIndex(1) 
        self.combo_crop.currentIndexChanged.connect(self.on_crop_changed)
        setting_layout.addWidget(self.combo_crop)

        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("种植循环次数："))
        self.input_loop = QLineEdit("3")
        loop_layout.addWidget(self.input_loop)
        setting_layout.addLayout(loop_layout)

        self.chk_sleep = QCheckBox("开启电脑睡眠模式（推荐）")
        self.chk_sleep.setChecked(True)
        setting_layout.addWidget(self.chk_sleep)
        setting_layout.addWidget(QLabel("*若无法唤醒，取消勾选即可切换为【仅关闭屏幕】模式"))
        
        self.chk_water = QCheckBox("启用后续自动浇水（仅对类型3-7生效）")
        self.chk_water.setEnabled(False) 
        setting_layout.addWidget(self.chk_water)
        
        setting_box.setLayout(setting_layout)
        main_layout.addWidget(setting_box)

        # 3. 控制按钮
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ 开始运行")
        self.style_start_normal = "background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;"
        self.style_start_disabled = "background-color: #A5D6A7; color: white; font-weight: bold; padding: 8px;"
        self.btn_start.setStyleSheet(self.style_start_normal)
        self.btn_start.clicked.connect(self.start_farm)
        
        self.btn_stop = QPushButton("⏹️ 停止运行")
        self.style_stop_normal = "background-color: #f44336; color: white; font-weight: bold; padding: 8px;"
        self.style_stop_disabled = "background-color: #EF9A9A; color: white; font-weight: bold; padding: 8px;"
        self.btn_stop.setStyleSheet(self.style_stop_disabled)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_farm)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        main_layout.addLayout(btn_layout)

        # 4. 日志区
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #f0f0f0;")
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # 5. 底部署名
        footer = QLabel("by 辰风")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 12px;")
        main_layout.addWidget(footer)

    def on_crop_changed(self):
        key = self.combo_crop.currentData()
        if int(key) >= 3:
            self.chk_water.setEnabled(True)
        else:
            self.chk_water.setChecked(False)
            self.chk_water.setEnabled(False)

    def start_farm(self):
        try:
            loop_count = int(self.input_loop.text())
            if loop_count <= 0: raise ValueError
        except:
            self.log_message("错误：请输入有效的循环次数！", "red")
            return

        crop_key = self.combo_crop.currentData()
        wait_map = {'1': 10, '2': 40, '3': 100, '4': 160, '5': 340, '6': 580, '7': 1180}
        initial_wait = wait_map[crop_key]
        
        water_count = 0
        final_wait = initial_wait
        if self.chk_water.isChecked():
            # 注意：这里的 60 应与 config 中的 WATER_COOLDOWN_MINUTES 保持概念一致
            # 但 GUI 中先用硬编码 60 估算次数
            water_count = initial_wait // 60 
            final_wait = initial_wait % 60

        settings = {
            'crop_choice': crop_key,
            'loop_count': loop_count,
            'initial_wait': initial_wait,
            'enable_water': self.chk_water.isChecked(),
            'water_count': water_count,
            'final_wait': final_wait,
            'enable_sleep': self.chk_sleep.isChecked()
        }

        self.worker = FarmWorker(settings)
        self.worker.log_signal.connect(self.log_message)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()
        
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet(self.style_start_disabled)
        
        self.btn_stop.setEnabled(True)
        self.btn_stop.setStyleSheet(self.style_stop_normal)
        
        self.combo_crop.setEnabled(False)
        self.input_loop.setEnabled(False)
        self.chk_sleep.setEnabled(False)
        self.chk_water.setEnabled(False)

    def stop_farm(self):
        if self.worker:
            self.worker.stop()
            self.log_message("正在停止脚本...", "red")

    def on_finished(self):
        self.btn_start.setEnabled(True)
        self.btn_start.setStyleSheet(self.style_start_normal)
        
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet(self.style_stop_disabled)
        
        self.combo_crop.setEnabled(True)
        self.input_loop.setEnabled(True)
        self.chk_sleep.setEnabled(True)
        self.on_crop_changed() 
        self.log_message("脚本已停止。", "red")

    def log_message(self, msg, color):
        self.log_text.append(f'<span style="color:{color}">{msg}</span>')
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())