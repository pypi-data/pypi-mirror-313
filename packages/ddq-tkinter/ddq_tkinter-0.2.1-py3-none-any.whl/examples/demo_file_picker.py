import tkinter as tk
from tkinter import ttk
from ddq_widgets import FilePicker

class FilePickerDemo(ttk.Frame):
    """FilePicker 组件示例"""
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 基本文件选择器
        ttk.Label(self, text="基本文件选择器:").pack(anchor=tk.W, pady=(0, 5))
        picker1 = FilePicker(self)
        picker1.pack(fill=tk.X)
        
        # 带提示文本的文件选择器
        ttk.Label(self, text="带提示文本的文件选择器:").pack(anchor=tk.W, pady=(10, 5))
        picker2 = FilePicker(self, placeholder="请选择文件...")
        picker2.pack(fill=tk.X)
        
        # 文件夹选择器
        ttk.Label(self, text="文件夹选择器:").pack(anchor=tk.W, pady=(10, 5))
        picker3 = FilePicker(
            self, 
            mode="folder",
            placeholder="请选择目录..."
        )
        picker3.pack(fill=tk.X)
        
        # 带文件类型过滤的选择器
        ttk.Label(self, text="带文件类型过滤的选择器:").pack(anchor=tk.W, pady=(10, 5))
        picker4 = FilePicker(
            self,
            filetypes=[
                ("Markdown文件", "*.md"),
                ("文本文件", "*.txt")
            ],
            placeholder="请选择 MD 或 TXT 文件..."
        )
        picker4.pack(fill=tk.X)
        
        # 同时支持文件和目录的选择器
        ttk.Label(self, text="文件和目录选择器:").pack(anchor=tk.W, pady=(10, 5))
        picker5 = FilePicker(
            self,
            mode="all",
            placeholder="请选择文件或目录..."
        )
        picker5.pack(fill=tk.X)
        
        # 值变化监听
        ttk.Label(self, text="当前选择的路径:").pack(anchor=tk.W, pady=(10, 5))
        self.path_label = ttk.Label(self, text="")
        self.path_label.pack(anchor=tk.W)
        
        # 监听最后一个选择器的值变化
        picker5.path_var.trace_add('write', lambda *args: self._on_path_change(picker5))
        
        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame,
            text="获取路径",
            command=lambda: self._show_path(picker5)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            btn_frame,
            text="清空",
            command=lambda: picker5.path_var.set("")
        ).pack(side=tk.LEFT, padx=5)
        
    def _on_path_change(self, picker):
        """路径变化回调"""
        self.path_label.configure(text=picker.path_var.get() or "未选择")
        
    def _show_path(self, picker):
        """显示当前路径"""
        from tkinter import messagebox
        path = picker.path_var.get()
        messagebox.showinfo("当前路径", f"选择的路径是: {path or '未选择'}")

def main():
    root = tk.Tk()
    root.title("FilePicker 组件示例")
    root.geometry("600x500")
    
    app = FilePickerDemo(root)
    
    root.mainloop()

if __name__ == "__main__":
    main() 