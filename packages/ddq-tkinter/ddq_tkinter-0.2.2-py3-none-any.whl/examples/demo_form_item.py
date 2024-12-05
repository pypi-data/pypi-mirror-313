import tkinter as tk
from tkinter import ttk

from ddq_widgets import FormItem

class FormItemDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("FormItem 组件示例")
        self.root.geometry("500x300")
        
        # 创建一个容器 Frame，用于测试 FormItem 的自适应性
        self.container = ttk.Frame(root)
        self.container.pack(fill=tk.X, padx=20, pady=20)
        
        # 创建各种类型的输入控件
        # 1. 文本输入框
        self.input_item = FormItem.input(
            self.container,
            "用户名:"
        )
        
        # 2. 密码输入框
        self.password_item = FormItem.password(
            self.container,
            "密码:"
        )
        
        # 3. 下拉选择框
        self.select_item = FormItem.select(
            self.container,
            "类型:",
            options=["选项1", "选项2", "选项3"]
        )
        
        # 4. 单选框组
        self.radio_item = FormItem.radio(
            self.container,
            "性别:",
            options=["男", "女"]
        )
        
        # 5. 复选框组
        self.checkbox_item = FormItem.checkbox(
            self.container,
            "爱好:",
            options=["阅读", "音乐", "运动"]
        )
        
        # 6. 多行文本框
        self.textarea_item = FormItem.textarea(
            self.container,
            "描述:",
            height=3
        )
        
        # 1. 文件选择器 - 单个文件
        self.file_item = FormItem.file_picker(
            self.container,
            "选择文件:",
            mode="file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            placeholder="请选择文件"
        )
        
        # 2. 文件选择器 - 文件夹
        self.folder_item = FormItem.file_picker(
            self.container,
            "选择目录:",
            mode="folder"
        )
        
        # 3. 文件选择器 - 多按钮模式
        self.multi_item = FormItem.file_picker(
            self.container,
            "多选模式:",
            multiple_buttons=True
        )

def main():
    root = tk.Tk()
    app = FormItemDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 