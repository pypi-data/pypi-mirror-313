import tkinter as tk
from tkinter import ttk

class Text(ttk.Label):
    """纯文本展示组件
    
    特性：
    1. 基于 ttk.Label
    2. 支持自动换行
    3. 支持左对齐
    4. 支持设置值的接口
    5. 自动适应父级宽度
    """
    
    def __init__(
        self,
        master,
        text: str = "",
        wraplength: int = None,  # 改为默认 None，表示自动适应
        justify: str = tk.LEFT,  # 文本对齐方式
        **kwargs
    ):
        super().__init__(
            master,
            text=text,
            justify=justify,
            **kwargs
        )
        
        # 自动设置布局
        self.pack(fill=tk.X, padx=5, pady=5)
        
        # 绑定大小变化事件
        self.bind('<Configure>', self._on_resize)
        self._wraplength = wraplength
        
    def _on_resize(self, event):
        """处理大小变化事件"""
        # 如果没有指定固定的换行宽度，就使用组件当前宽度
        if self._wraplength is None:
            self.configure(wraplength=event.width)
            
    def get_text(self) -> str:
        """获取文本内容"""
        return self.cget('text')
        
    def set_text(self, content: str):
        """设置文本内容"""
        self.configure(text=content)
        
    @property
    def value(self) -> str:
        """获取值(用于表单)"""
        return self.get_text()
        
    @value.setter
    def value(self, content: str):
        """设置值(用于表单)"""
        self.set_text(content) 