import ctypes
import time
import sys

# Windows API Structures
class LARGE_INTEGER(ctypes.Structure):
    _fields_ = [("QuadPart", ctypes.c_longlong)]

kernel32 = ctypes.windll.kernel32
powrprof = ctypes.windll.PowrProf
user32 = ctypes.windll.user32

def set_dpi_awareness():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

def force_screen_on(log_func=None):
    if log_func: log_func(">>> 尝试点亮屏幕 <<<", "blue")
    try:
        user32.SetCursorPos(100, 100)
        time.sleep(0.1)
        user32.SetCursorPos(105, 105)
        user32.keybd_event(0x10, 0, 0, 0) # Shift down
        user32.keybd_event(0x10, 0, 2, 0) # Shift up
    except: pass

def system_sleep_with_timer(seconds, log_func=None, check_running_func=None):
    """
    设置硬件定时器并使系统进入S3睡眠。
    seconds: 睡眠秒数
    """
    if log_func: log_func(f"设置硬件唤醒定时器: {seconds:.1f} 秒 ({seconds/60:.2f} 分钟)...", "blue")
    
    timer_handle = kernel32.CreateWaitableTimerW(None, True, "NuanNuanWakeTimer")
    if not timer_handle:
        if log_func: log_func("错误：无法创建唤醒定时器！", "red")
        return False

    due_time = LARGE_INTEGER()
    due_time.QuadPart = -1 * int(seconds * 10000000)
    success = kernel32.SetWaitableTimer(timer_handle, ctypes.byref(due_time), 0, None, None, True)

    if not success:
        if log_func: log_func("错误：无法激活唤醒定时器", "red")
        kernel32.CloseHandle(timer_handle)
        return False

    if log_func: 
        log_func(">>> 系统即将进入睡眠 (S3) <<<", "blue")
        log_func(">>> 10秒后进入睡眠 <<<", "blue")
    
    # 睡眠前的缓冲
    # 注意：在睡眠前也要检查一下是否已经被停止，防止刚点开始就点停止，结果还是睡下去了
    for _ in range(100): # 10秒，每0.1秒检查一次
        if check_running_func and not check_running_func():
            kernel32.CloseHandle(timer_handle)
            return False
        time.sleep(0.1)
    
    # 执行休眠
    powrprof.SetSuspendState(0, 0, 0)
    
    # 阻塞等待定时器唤醒
    woken_by_timer = False
    while True:
        # 优先检查是否被用户停止
        if check_running_func and not check_running_func():
            # 用户停止，不需要设置 woken_by_timer 为 True
            break
        
        # 500ms 检查一次定时器状态
        res = kernel32.WaitForSingleObject(timer_handle, 500)
        if res == 0: 
            # 定时器触发，正常唤醒
            woken_by_timer = True
            break
    
    kernel32.CloseHandle(timer_handle)

    # 只有当确实是定时器唤醒时，才打印日志和点亮屏幕
    # 如果是用户停止导致的 break，这里直接跳过
    if woken_by_timer:
        if log_func: log_func(">>> 系统已由定时器唤醒 <<<", "green")
        force_screen_on(log_func)
        return True
    else:
        # 如果不是定时器唤醒（即用户手动停止），直接返回 False
        # worker.py 会在随后调用 check_stop() 并抛出异常，打印 "用户手动停止运行"
        return False

def turn_off_screen(log_func=None):
    if log_func: log_func("睡眠模式未开启，仅关闭屏幕...", "darkorange")
    user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
