import tkinter as tk
from tkinter import ttk
from typing import List

class Radio(ttk.Frame):
    """单选框组组件"""
    
    def __init__(
        self,
        master,
        options: List[str],
        default: str = None,
        layout: str = "horizontal",  # "horizontal" 或 "vertical"
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 创建变量
        self.var = tk.StringVar(value=default or options[0] if options else "")
        
        # 创建单选按钮
        for i, option in enumerate(options):
            radio = ttk.Radiobutton(
                self,
                text=option,
                variable=self.var,
                value=option
            )
            if layout == "horizontal":
                radio.pack(side=tk.LEFT, padx=(0 if i == 0 else 5))
            else:  # vertical
                radio.pack(side=tk.TOP, anchor="w", pady=2)
    
    @property
    def value(self) -> str:
        """获取选中值"""
        return self.var.get()
    
    @value.setter
    def value(self, val: str):
        """设置选中值"""
        self.var.set(val) 