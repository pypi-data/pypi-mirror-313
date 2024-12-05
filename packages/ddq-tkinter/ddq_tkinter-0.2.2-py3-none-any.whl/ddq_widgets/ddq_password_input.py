import tkinter as tk
from tkinter import ttk

class PasswordInput(ttk.Entry):
    """带 placeholder 功能的密码输入框
    
    特性:
    1. 支持 placeholder 提示文本
    2. 自动处理提示文本颜色
    3. 自动处理焦点事件
    4. 自动处理密码掩码显示/隐藏
    5. 提供统一的值获取和设置接口
    """
    
    def __init__(
        self,
        master,
        placeholder: str = None,
        show: str = "*",  # 密码掩码字符
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 保存配置
        self._placeholder = placeholder
        self._show = show
        self.var = tk.StringVar()
        self.configure(textvariable=self.var)
        
        # 初始化 placeholder
        if placeholder:
            self.var.set(placeholder)
            self.configure(foreground='gray', show="")  # placeholder 不显示掩码
            
            # 绑定焦点事件
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
            
    def _on_focus_in(self, event):
        """获得焦点时的处理"""
        current_value = self.var.get()
        if current_value == self._placeholder:
            self.var.set("")  # 清空内容
            self.configure(foreground='black', show=self._show)  # 显示掩码
            
    def _on_focus_out(self, event):
        """失去焦点时的处理"""
        current_value = self.var.get()
        if not current_value:
            self.var.set(self._placeholder)  # 显示 placeholder
            self.configure(foreground='gray', show="")  # 不显示掩码
        else:
            self.configure(foreground='black', show=self._show)  # 有内容时显示掩码
            
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
            self.configure(foreground='gray', show="")  # placeholder 不显示掩码
        else:
            self.var.set(val)
            self.configure(foreground='black', show=self._show)  # 有值时显示掩码 