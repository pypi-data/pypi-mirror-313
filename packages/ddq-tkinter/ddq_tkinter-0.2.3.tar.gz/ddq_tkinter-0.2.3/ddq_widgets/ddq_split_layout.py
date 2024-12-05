import tkinter as tk
from tkinter import ttk
from .ddq_scrollable import ScrollableContainer

class SplitLayout(ttk.Frame):
    """左右布局组件，两侧都支持滚动"""
    
    def __init__(
        self,
        master,
        left_width: int = None,
        right_width: int = None,
        spacing: int = 10,
        separator: bool = True,
        left_scrollable: bool = True,   # 添加左侧滚动控制选项
        right_scrollable: bool = True,  # 右侧滚动控制选项
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个容器来控制左右比例
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # 配置容器的列权重
        if left_width and not right_width:
            # 左侧固定宽度，右侧占用剩余空间
            self.container.grid_columnconfigure(0, weight=0)  # 左侧不伸缩
            self.container.grid_columnconfigure(2, weight=1)  # 右侧占用剩余空间
        elif right_width and not left_width:
            # 右侧固定宽度，左侧占用剩余空间
            self.container.grid_columnconfigure(0, weight=1)  # 左侧占用剩余空间
            self.container.grid_columnconfigure(2, weight=0)  # 右侧不伸缩
        else:
            # 其他情况（都有值或都没值），左右均分
            self.container.grid_columnconfigure(0, weight=1, uniform='split')
            self.container.grid_columnconfigure(2, weight=1, uniform='split')
        
        self.container.grid_columnconfigure(1, weight=0)  # 分隔线
        self.container.grid_rowconfigure(0, weight=1)
        
        # 左侧面板
        self.left_frame = ttk.Frame(self.container)
        if left_width:
            self.left_frame.configure(width=left_width)
            self.left_frame.grid_propagate(False)
        self.left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, spacing//2))
        
        if left_scrollable:
            # 使用 ScrollableContainer
            scrollable = ScrollableContainer(self.left_frame)
            scrollable.pack(fill=tk.BOTH, expand=True)
            self.left = scrollable.content
        else:
            # 不需要滚动时，直接使用普通框架
            self.left = ttk.Frame(self.left_frame)
            self.left.pack(fill=tk.BOTH, expand=True)
        
        # 分割线
        if separator:
            self.separator = ttk.Separator(self.container, orient='vertical')
            self.separator.grid(row=0, column=1, sticky='ns')
        
        # 右侧面板
        self.right_frame = ttk.Frame(self.container)
        if right_width:
            self.right_frame.configure(width=right_width)
            self.right_frame.grid_propagate(False)  # 禁止自动调整大小
        self.right_frame.grid(row=0, column=2, sticky='nsew', padx=(spacing//2, 0))
        
        if right_scrollable:
            # 使用 ScrollableContainer
            scrollable = ScrollableContainer(self.right_frame)
            scrollable.pack(fill=tk.BOTH, expand=True)
            self.right = scrollable.content
        else:
            # 不需要滚动时，直接使用普通框架
            self.right = ttk.Frame(self.right_frame)
            self.right.pack(fill=tk.BOTH, expand=True)
                
    def toggle_left(self):
        """切换左侧面板显示状态"""
        if self.left_frame.winfo_ismapped():
            self.left_frame.grid_remove()
            if hasattr(self, 'separator'):
                self.separator.grid_remove()
        else:
            self.left_frame.grid(row=0, column=0, sticky='nsew')
            if hasattr(self, 'separator'):
                self.separator.grid(row=0, column=1, sticky='ns')
                
    def toggle_right(self):
        """切换右侧面板显示状态"""
        if self.right_frame.winfo_ismapped():
            self.right_frame.grid_remove()
            if hasattr(self, 'separator'):
                self.separator.grid_remove()
        else:
            if hasattr(self, 'separator'):
                self.separator.grid(row=0, column=1, sticky='ns')
            self.right_frame.grid(row=0, column=2, sticky='nsew')