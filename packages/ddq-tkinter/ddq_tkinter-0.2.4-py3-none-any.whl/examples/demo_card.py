import tkinter as tk
from tkinter import ttk
from ddq_widgets import Card, FormItem

class CardDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Card 组件示例")
        self.root.geometry("600x400")
        
        # 创建一个简单的卡片
        simple_card = Card(root, title="简单卡片")
        ttk.Label(simple_card.content, text="这是一个简单的卡片示例").pack(pady=10)
        
        # 创建一个带表单项的卡片
        form_card = Card(root, title="表单项示例")
        
        # 创建容器用于放置表单项
        container = ttk.Frame(form_card.content)
        container.pack(fill=tk.X, padx=20, pady=10)
        
        # 添加各种表单项
        self.input_item = FormItem.input(
            container,
            "用户名:"
        )
        
        self.select_item = FormItem.select(
            container,
            "类型:",
            options=["选项1", "选项2", "选项3"]
        )
        
        self.radio_item = FormItem.radio(
            container,
            "性别:",
            options=["男", "女"]
        )
        
        self.checkbox_item = FormItem.checkbox(
            container,
            "爱好:",
            options=["阅读", "音乐", "运动"]
        )
        
        # 创建一个文件选择器卡片
        file_card = Card(root, title="文件选择器")
        file_container = ttk.Frame(file_card.content)
        file_container.pack(fill=tk.X, padx=20, pady=10)
        
        self.file_item = FormItem.file_picker(
            file_container,
            "选择文件:",
            mode="file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        self.folder_item = FormItem.file_picker(
            file_container,
            "选择目录:",
            mode="folder"
        )

def main():
    root = tk.Tk()
    app = CardDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 