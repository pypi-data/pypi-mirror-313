import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_scrollable import ScrollableContainer
from ddq_widgets.ddq_text import Text
from ddq_widgets.ddq_card import Card

class ScrollableTextDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("ScrollableText 组件示例")
        self.root.geometry("600x400")
        
        # 创建一个卡片来包装内容
        self.card = Card(root, title="滚动文本示例")
        
        # 创建可滚动容器
        self.scroll_container = ScrollableContainer(self.card.content)
        
        # 在滚动容器中创建文本
        self.text = Text(self.scroll_container.content)
        
        # 添加一些测试内容
        test_content = []
        for i in range(30):
            test_content.append(f"这是第 {i+1} 行测试文本内容")
        
        # 设置文本内容
        self.text.set_text("\n".join(test_content))
        
        # 添加一个按钮来动态添加更多内容
        self.button = ttk.Button(
            root, 
            text="添加更多内容", 
            command=self.add_more_content
        )
        self.button.pack(pady=10)
        
    def add_more_content(self):
        """添加更多测试内容"""
        current_text = self.text.get_text()
        new_content = "\n".join([
            f"新增的第 {i+1} 行内容" 
            for i in range(5)
        ])
        self.text.set_text(current_text + "\n" + new_content)

def main():
    root = tk.Tk()
    app = ScrollableTextDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 