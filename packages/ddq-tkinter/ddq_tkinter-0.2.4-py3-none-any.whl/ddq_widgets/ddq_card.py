import tkinter as tk
from tkinter import ttk

class Card(ttk.LabelFrame):
    """卡片容器组件
    
    特性：
    1. 默认只填充水平方向
    2. 内置内容区域
    3. 统一的内边距
    4. 可选的标题
    """
    
    def __init__(
        self,
        master,
        title: str = "",
        padding: int = 5,
        expand: bool = True,  # 改为默认 True
        fill: str = tk.BOTH,  # 改为默认 BOTH
        **kwargs
    ):
        super().__init__(master, text=title, **kwargs)
        
        # 确保卡片本身填充
        self.pack(fill=fill, expand=expand, padx=padding, pady=padding)
        
        # 内容区域也要填充
        self.content = ttk.Frame(self)
        self.content.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)  # 内容区域始终 BOTH
