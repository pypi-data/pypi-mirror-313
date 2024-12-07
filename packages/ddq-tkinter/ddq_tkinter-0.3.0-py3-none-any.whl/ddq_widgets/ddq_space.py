import tkinter as tk
from tkinter import ttk
from typing import Literal, Union, Optional

class Space(ttk.Frame):
    """空间布局组件"""
    
    def __init__(
        self,
        master,
        direction: Literal["vertical", "horizontal"] = "vertical",
        size: Union[int, tuple[int, int]] = 4,
        fill: bool = True,
        expand: bool = True,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 保存布局属性
        self.direction = direction
        self.size = size
        
        # 应用布局
        if fill or expand:
            self.pack(
                fill=tk.BOTH if fill else tk.NONE,
                expand=expand
            )
        
        # 内部变量
        self._children = []
        
    def add(self, widget: tk.Widget, expand: bool = False):
        """添加子组件"""
        self._children.append(widget)
        
        if self.direction == "vertical":
            widget.pack(
                fill=tk.X,  # 垂直布局时，子组件水平填充
                expand=expand,
                pady=(self.size if len(self._children) > 1 else 0, 0)  # 组件间距
            )
        else:
            widget.pack(
                side=tk.LEFT,
                fill=tk.X if expand else tk.NONE,  # 水平布局时，可选择是否填充
                expand=expand,
                padx=(self.size if len(self._children) > 1 else 0, 0)  # 组件间距
            )
                
    def remove(self, widget: tk.Widget):
        """移除子组件"""
        if widget in self._children:
            widget.pack_forget()
            self._children.remove(widget)
            
    def clear(self):
        """清除所有子组件"""
        for child in self._children:
            child.pack_forget()
        self._children.clear()
        
    def _layout_vertical(self):
        """垂直布局"""
        for i, child in enumerate(self._children):
            # 配置行权重
            self.content.grid_rowconfigure(i, weight=0)
            
            child.grid(
                in_=self.content,
                row=i,
                column=0,
                sticky="ew",  # 水平填充
                pady=(self.size if i > 0 else 0)
            )
            
    def _layout_horizontal(self):
        """水平布局"""
        for i, child in enumerate(self._children):
            child.grid(
                in_=self.content,
                row=0,
                column=i,
                sticky="ns",  # 垂直填充
                padx=(0 if i == 0 else self.size[0], 0)  # 只设置左边距
            )
            
        # 设置列权重
        if self.expand:
            for i in range(len(self._children)):
                self.content.grid_columnconfigure(i, weight=1)
                
    def _layout_vertical(self):
        """垂直布局"""
        for i, child in enumerate(self._children):
            # 配置行权重
            self.content.grid_rowconfigure(i, weight=0)
            
            child.grid(
                in_=self.content,
                row=i,
                column=0,
                sticky="ew",  # 水平填充
                pady=(self.size if i > 0 else 0)
            )
            
    def _layout_horizontal(self):
        """水平布局"""
        for i, child in enumerate(self._children):
            child.grid(
                in_=self.content,
                row=0,
                column=i,
                sticky="ns",  # 垂直填充
                padx=(0 if i == 0 else self.size[0], 0)  # 只设置左边距
            )
            
        # 设置列权重
        if self.expand:
            for i in range(len(self._children)):
                self.content.grid_columnconfigure(i, weight=1)
                
    def remove(self, child: tk.Widget):
        """移除子组件"""
        if child in self._children:
            child.grid_remove()
            self._children.remove(child)
            self._layout_vertical() if self.direction == "vertical" else self._layout_horizontal()
            
    def clear(self):
        """清除所有子组件"""
        for child in self._children:
            child.grid_remove()
        self._children.clear()
        self._current_row = 0
        self._current_col = 0 