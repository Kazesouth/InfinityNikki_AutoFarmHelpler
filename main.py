import sys
import ctypes
from PyQt5.QtWidgets import QApplication
from gui import FarmGUI
import system_ops

if __name__ == "__main__":
    # 设置 Windows 任务栏图标 ID
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ChenFeng.NikkiFarmhelper.v1.48")
    except:
        pass
    
    # 设置 DPI 感知 (防止高分屏模糊)
    system_ops.set_dpi_awareness()

    app = QApplication(sys.argv)
    window = FarmGUI()
    window.show()
    sys.exit(app.exec_())