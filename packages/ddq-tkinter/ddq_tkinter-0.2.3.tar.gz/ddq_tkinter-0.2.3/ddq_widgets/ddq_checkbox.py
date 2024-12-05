import tkinter as tk
from tkinter import ttk
from typing import List

class Checkbox(ttk.Frame):
    """复选框组组件"""
    
    def __init__(
        self,
        master,
        options: List[str],
        defaults: List[bool] = None,
        layout: str = "horizontal",  # "horizontal" 或 "vertical"
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 创建变量列表
        if defaults is None:
            defaults = [False] * len(options)
        self.vars = [tk.BooleanVar(value=default) for default in defaults]
        
        # 创建复选框
        for i, (option, var) in enumerate(zip(options, self.vars)):
            checkbox = ttk.Checkbutton(
                self,
                text=option,
                variable=var
            )
            if layout == "horizontal":
                checkbox.pack(side=tk.LEFT, padx=(0 if i == 0 else 5))
            else:  # vertical
                checkbox.pack(side=tk.TOP, anchor="w", pady=2)
    
    @property
    def value(self) -> List[bool]:
        """获取选中状态列表"""
        return [var.get() for var in self.vars]
    
    @value.setter
    def value(self, val: List[bool]):
        """设置选中状态列表"""
        if len(val) == len(self.vars):
            for var, v in zip(self.vars, val):
                var.set(v) 