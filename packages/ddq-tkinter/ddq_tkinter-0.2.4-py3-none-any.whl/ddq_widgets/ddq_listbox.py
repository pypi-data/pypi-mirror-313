import tkinter as tk
from tkinter import ttk

class Listbox(ttk.Frame):
    """列表框组件，自带滚动条支持
    
    特性：
    1. 自动处理滚动条显示/隐藏
    2. 支持选择事件
    3. 简化的数据操作接口
    """
    def __init__(
        self,
        master,
        width: int = 30,
        height: int = None,
        exportselection: bool = False,
        **kwargs
    ):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建 Listbox
        self.listbox = tk.Listbox(
            self,
            width=width,
            height=height,
            exportselection=exportselection,
            **kwargs
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建滚动条但不立即显示
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.listbox.yview
        )
        
        # 配置 Listbox 的滚动
        self.listbox.configure(yscrollcommand=self._on_scroll)
        
        # 保存选择事件回调
        self._select_callback = None
        
    def _on_scroll(self, *args):
        """处理滚动事件，根据需要显示/隐藏滚动条"""
        first, last = args
        
        # 如果内容未充满显示区域（last=1.0），隐藏滚动条
        if float(last) == 1.0 and float(first) == 0.0:
            self.scrollbar.pack_forget()
        else:
            # 否则显示滚动条
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        # 更新滚动条位置
        self.scrollbar.set(*args)
        
    def set_items(self, items: list):
        """设置列表项"""
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
            
    def get_items(self) -> list:
        """获取所有列表项"""
        return list(self.listbox.get(0, tk.END))
        
    def add_item(self, item):
        """添加列表项"""
        self.listbox.insert(tk.END, item)
        
    def remove_item(self, item):
        """移除列表项"""
        items = self.get_items()
        if item in items:
            idx = items.index(item)
            self.listbox.delete(idx)
            
    def clear(self):
        """清空列表"""
        self.listbox.delete(0, tk.END)
        
    def get_selection(self) -> str:
        """获取当前选中项"""
        selection = self.listbox.curselection()
        if selection:
            return self.listbox.get(selection[0])
        return None
        
    def set_selection(self, item):
        """选中指定项"""
        items = self.get_items()
        if item in items:
            idx = items.index(item)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)
            
    def on_select(self, callback):
        """设置选择事件回调"""
        self._select_callback = callback
        self.listbox.bind('<<ListboxSelect>>', self._handle_select)
        
    def _handle_select(self, event):
        """处理选择事件"""
        if self._select_callback:
            selection = self.get_selection()
            self._select_callback(selection) 