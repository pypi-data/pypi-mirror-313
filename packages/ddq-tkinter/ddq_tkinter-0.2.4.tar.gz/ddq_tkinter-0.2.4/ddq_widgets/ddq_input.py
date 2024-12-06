import tkinter as tk
from tkinter import ttk

class Input(ttk.Entry):
    """带 placeholder 功能的输入框基类
    
    特性:
    1. 支持 placeholder 提示文本
    2. 自动处理提示文本颜色
    3. 自动处理焦点事件
    4. 提供统一的值获取和设置接口
    """
    
    def __init__(
        self,
        master,
        placeholder: str = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 保存 placeholder
        self._placeholder = placeholder
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)
        
        # 初始化 placeholder
        if placeholder:
            self.var.set(placeholder)
            self.configure(foreground='gray')
            
            # 绑定焦点事件
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
            
    def _on_focus_in(self, event):
        """获得焦点时的处理"""
        if self.var.get() == self._placeholder:
            self.var.set("")
            self.configure(foreground='black')
            
    def _on_focus_out(self, event):
        """失去焦点时的处理"""
        if not self.var.get():
            self.var.set(self._placeholder)
            self.configure(foreground='gray')
        else:
            self.configure(foreground='black')
            
    @property 
    def value(self) -> str:
        """获取真实值"""
        current = self.var.get()
        if current == self._placeholder:
            return ""
        return current
        
    @value.setter
    def value(self, val: str):
        """设置值"""
        if not val and self._placeholder:
            self.var.set(self._placeholder)
            self.configure(foreground='gray')
        else:
            self.var.set(val)
            self.configure(foreground='black') 