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
        placeholder: str = None
    ):
        super().__init__(master)
        self._mode = mode
        self.filetypes = filetypes or [("所有文件", "*.*")]
        
        # 使用 Input 替代原来的 Entry
        self.path_input = Input(
            self,
            placeholder=placeholder
        )
        self.path_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # path_var 直接使用 input 的 var
        self.path_var = self.path_input.var
        
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
            
    def _select_folder(self):
        """选择目录"""
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)