import tkinter as tk
from tkinter import ttk

class ScrollableContainer(ttk.Frame):
    """通用的可滚动容器组件
    
    特性：
    1. 支持任意内容的垂直滚动
    2. 自动/始终/从不显示滚动条
    3. 支持鼠标滚轮
    4. 自动适应内容高度
    """
    
    def __init__(
        self,
        master,
        scrollbar: str = "auto",  # auto/always/never
        **kwargs
    ):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar_mode = scrollbar
        
        # 创建滚动条
        if scrollbar != "never":
            self.scrollbar = ttk.Scrollbar(self)
            if scrollbar == "always":
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # auto 模式下先不显示，等内容超出时再显示
        else:
            self.scrollbar = None
        
        # 创建画布，并禁用焦点边框
        self.canvas = tk.Canvas(
            self, 
            yscrollcommand=self._on_scroll if self.scrollbar else None,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        if self.scrollbar:
            self.scrollbar.config(command=self.canvas.yview)
        
        # 创建内容框架
        self.content = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.content,
            anchor='nw',
            tags='content',
            width=self.canvas.winfo_width()
        )
        
        # 绑定事件
        self.content.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # 绑定鼠标进入/离开事件
        self.canvas.bind('<Enter>', self._bind_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_mousewheel)
        
    def _on_scroll(self, *args):
        """处理滚动事件，用于自动显示/隐藏滚动条"""
        if self.scrollbar_mode == "auto":
            # 检查是否需要显示滚动条
            bbox = self.canvas.bbox("all")
            if bbox and bbox[3] > self.canvas.winfo_height():
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self.scrollbar.pack_forget()
        
        # 更新滚动条位置
        if self.scrollbar:
            if args:  # 确保有参数传入
                self.scrollbar.set(*args)
            else:
                # 如果没有参数，使用当前视图的位置
                first = self.canvas.yview()[0]
                last = self.canvas.yview()[1]
                self.scrollbar.set(first, last)
        
    def _on_frame_configure(self, event=None):
        """当内容框架大小改变时，更新画布滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # 传入正确的参数
        first = self.canvas.yview()[0]
        last = self.canvas.yview()[1]
        self._on_scroll(first, last)
        
    def _on_canvas_configure(self, event):
        """当画布大小改变时，调整内容框架宽度"""
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )
        
    def _bind_mousewheel(self, event=None):
        """当鼠标进入画布时绑定滚轮事件"""
        # 检查是否有可滚动内容
        bbox = self.canvas.bbox("all")
        if bbox and bbox[3] > self.canvas.winfo_height():
            self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        
    def _unbind_mousewheel(self, event=None):
        """当鼠标离开画布时解绑滚轮事件"""
        self.canvas.unbind_all('<MouseWheel>')
        
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        # 获取鼠标相对于画布的位置
        x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        
        # 检查鼠标是否在画布区域内
        if (0 <= x <= self.canvas.winfo_width() and 
            0 <= y <= self.canvas.winfo_height()):
            # 检查是否有可滚动内容
            bbox = self.canvas.bbox("all")
            if bbox and bbox[3] > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")