import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Optional, List, Tuple, Literal
from .ddq_input import Input

class FilePicker(ttk.Frame):
    def __init__(
        self,
        master,
        label: str = "",
        mode: str = "file",  # 'file', 'folder' 或 'all'
        filetypes: Optional[List[Tuple[str, str]]] = None,
        multiple_buttons: bool = False,
        placeholder: str = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self._mode = mode
        self.filetypes = filetypes or [("所有文件", "*.*")]
        
        # 创建路径变量
        self.path_var = tk.StringVar()
        
        # 监听路径变化
        def on_path_change(*args):
            value = self.path_var.get()
            if value and value != self._placeholder:
                self.entry.config(foreground='black')
                
        self.path_var.trace_add('write', on_path_change)
        
        # 创建输入框
        self.entry = ttk.Entry(
            self,
            textvariable=self.path_var
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 保存占位符文本
        self._placeholder = placeholder
        
        # 如果有占位符，设置占位符样式
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(foreground='gray')
            
            def on_focus_in(event):
                if self.entry.get() == self._placeholder:
                    self.entry.delete(0, tk.END)
                    self.entry.config(foreground='black')
                    
            def on_focus_out(event):
                if not self.entry.get():
                    self.entry.insert(0, self._placeholder)
                    self.entry.config(foreground='gray')
                    
            self.entry.bind('<FocusIn>', on_focus_in)
            self.entry.bind('<FocusOut>', on_focus_out)
        
        # 创建按钮框架
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        # 创建选择文件按钮
        self.file_button = ttk.Button(
            self.button_frame, 
            text="选择文件",
            command=self._select_file
        )
        
        # 创建选择目录按钮
        self.folder_button = ttk.Button(
            self.button_frame, 
            text="选择目录",
            command=self._select_folder
        )
        
        # 根据模式显示按钮
        self._update_buttons()
        
    def _update_buttons(self):
        """根据模式更新按钮显示"""
        # 先移除所有按钮
        self.file_button.pack_forget()
        self.folder_button.pack_forget()
        
        if self._mode == "file":
            self.file_button.pack(side=tk.LEFT)
        elif self._mode == "folder":
            self.folder_button.pack(side=tk.LEFT)
        else:  # "all"
            self.file_button.pack(side=tk.LEFT)
            self.folder_button.pack(side=tk.LEFT, padx=(5, 0))
        
    def set_mode(self, mode: str):
        """设置模式（文件/文件夹/全部）"""
        if mode not in ["file", "folder", "all"]:
            raise ValueError("mode must be 'file', 'folder' or 'all'")
        self._mode = mode
        self._update_buttons()
        
    def _select_file(self):
        """选择文件"""
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.path_var.set(path)
            self.entry.config(foreground='black')
            
    def _select_folder(self):
        """选择目录"""
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            self.entry.config(foreground='black')
            
    def set_path(self, path: str):
        """设置路径"""
        if path:
            self.path_var.set(path)
            self.entry.config(foreground='black')
            
    @property
    def value(self):
        """获取值"""
        return self.path_var.get()
        
    @value.setter
    def value(self, val):
        """设置值"""
        self.path_var.set(val)