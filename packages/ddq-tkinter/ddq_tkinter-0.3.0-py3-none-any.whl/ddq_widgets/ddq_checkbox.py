import tkinter as tk
from tkinter import ttk
from typing import List

class Checkbox(ttk.Frame):
    """复选框组组件"""
    
    def __init__(
        self,
        master,
        options: List[str],
        default_values: List[str] = None,
        layout: str = "horizontal",  # "horizontal" 或 "vertical"
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 保存选项列表 (改名为 _option_list)
        self._option_list = options
        
        # 创建变量字典
        self.vars = {}
        for option in options:
            is_default = default_values and option in default_values
            self.vars[option] = tk.BooleanVar(value=is_default)
        
        # 创建复选框容器
        self.checkbox_frame = ttk.Frame(self)
        self.checkbox_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建复选框
        self.checkboxes = {}
        for i, option in enumerate(options):
            checkbox = ttk.Checkbutton(
                self.checkbox_frame,
                text=option,
                variable=self.vars[option]
            )
            if layout == "horizontal":
                checkbox.pack(side=tk.LEFT)
            else:  # vertical
                checkbox.pack(side=tk.TOP, anchor="w")
            self.checkboxes[option] = checkbox
    
    @property
    def value(self) -> List[str]:
        """获取选中的选项列表"""
        return [
            option 
            for option, var in self.vars.items() 
            if var.get()
        ]
    
    @value.setter
    def value(self, values: List[str]):
        """设置选中的选项列表"""
        # 先清空所有选择
        for var in self.vars.values():
            var.set(False)
        # 设置新的选择
        for val in values:
            if val in self.vars:
                self.vars[val].set(True)