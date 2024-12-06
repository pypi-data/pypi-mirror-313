import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_text import Text
from ddq_widgets.ddq_card import Card

def main():
    root = tk.Tk()
    root.title("Text Demo")
    root.geometry("400x300")
    
    # 创建一个卡片
    card = Card(root, title="文本展示")
    
    # 在卡片内创建文本
    text = Text(
        card.content,
        text="这是一段示例文本，用来演示 Text 组件的自动换行功能。" * 3
    )
    
    root.mainloop()

if __name__ == "__main__":
    main() 