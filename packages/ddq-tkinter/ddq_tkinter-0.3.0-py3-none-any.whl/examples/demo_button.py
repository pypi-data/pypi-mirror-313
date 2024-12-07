import tkinter as tk
from ddq_widgets.ddq_button import Button

def handle_click():
    """处理按钮点击"""
    print("按钮被点击了!")

def main():
    root = tk.Tk()
    root.title("Button Demo")
    root.geometry("300x200")
    
    # 创建一个标准蓝色按钮
    btn1 = Button(
        root,
        text="标准按钮",
        command=handle_click
    )
    btn1.pack(pady=20)
    
    # 创建一个高按钮
    btn2 = Button(
        root,
        text="高按钮",
        command=handle_click,
        pady=50  # 增加垂直内边距
    )
    btn2.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main() 