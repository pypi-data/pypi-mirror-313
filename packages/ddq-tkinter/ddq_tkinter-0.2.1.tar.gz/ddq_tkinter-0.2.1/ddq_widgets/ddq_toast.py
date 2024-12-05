import tkinter as tk
from tkinter import ttk

class Toast:
    """通用的悬浮提示组件"""
    def __init__(self, master):
        self.master = master
        self.window = None
        
    def show(self, message, duration=1000):
        """显示悬浮提示
        Args:
            message: 提示信息
            duration: 显示时长(毫秒)
        """
        # 如果已有提示窗口，先销毁
        if self.window:
            self.window.destroy()
            
        # 创建提示窗口
        self.window = tk.Toplevel()
        self.window.overrideredirect(True)  # 无边框窗口
        self.window.attributes('-topmost', True)  # 保持在最顶层
        
        # 设置样式
        frame = ttk.Frame(self.window, style='Toast.TFrame')
        frame.pack(padx=2, pady=2)
        
        label = ttk.Label(frame, text=message, padding=2,
                         background='#666666', foreground='white')
        label.pack()
        
        # 计算位置（在主窗口顶部中心，距离上方16px）
        window_width = self.window.winfo_reqwidth()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - window_width) // 2
        y = self.master.winfo_rooty() + 8  # 设置距离顶部8px
        
        self.window.geometry(f"+{x}+{y}")
        
        # 设置定时器自动关闭
        self.window.after(duration, self.window.destroy) 