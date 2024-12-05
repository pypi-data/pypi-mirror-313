import tkinter as tk

class Button(tk.Button):
    """自定义蓝色按钮"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            bg="#007bff",          # 背景色
            fg="white",            # 文字颜色           
            padx=8,               # 水平内边距
            # pady=2,                # 垂直内边距，增加高度
            border=0,              # 无边框
        )
        
        # 绑定鼠标事件
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        
    def on_hover(self, event):
        """鼠标悬停效果"""
        self.configure(bg="#0056b3")
        
    def on_leave(self, event):
        """鼠标离开效果"""
        self.configure(bg="#007bff") 