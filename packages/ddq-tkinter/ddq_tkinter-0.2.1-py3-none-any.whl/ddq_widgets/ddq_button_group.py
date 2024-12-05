import tkinter as tk
from tkinter import ttk
from typing import Literal

# 使用相对导入
from .ddq_space import Space
from .ddq_button import Button

class ButtonGroup(ttk.Frame):
    """按钮组组件
    
    特性：
    1. 支持水平/垂直布局
    2. 统一的按钮间距
    3. 支持左中右对齐
    """
    
    def __init__(
        self,
        master,
        direction: Literal["horizontal", "vertical"] = "horizontal",  # 布局方向
        spacing: int = 5,                                            # 按钮间距
        align: Literal["left", "center", "right"] = "left",         # 对齐方式
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 设置自身的布局
        self.pack(fill="x", padx=5, pady=2)
        
        self.direction = direction
        self.spacing = spacing
        self.align = align
        
        # 创建 Space 容器
        self.container = Space(
            self,
            direction=direction,
            size=spacing,
            fill=True,
            expand=False
        )
        
        # 根据对齐方式设置容器布局
        if direction == "horizontal":
            self.container.pack(side=align)
        else:
            self.container.pack(fill="both", expand=True)
        
        # 保存按钮列表
        self.buttons = []
        
    def add(self, button: Button):
        """添加按钮"""
        self.buttons.append(button)
        button.master = self.container
        
        # 使用 Space 添加按钮
        self.container.add(button)
            
    def add_new(self, text: str, command=None, **kwargs) -> Button:
        """创建并添加新按钮"""
        button = Button(self.container, text=text, command=command, **kwargs)
        self.add(button)
        return button
        
    def clear(self):
        """清除所有按钮"""
        self.container.clear()
        self.buttons.clear() 