import tkinter as tk
from ddq_widgets import ButtonGroup

class ButtonGroupDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("ButtonGroup 组件示例")
        self.root.geometry("600x400")
        
        # 水平按钮组
        horizontal_group = ButtonGroup(
            self.root,
            direction="horizontal",
            spacing=8,
            align="left"
        )
        
        # 添加几个按钮
        horizontal_group.add_new("按钮1", command=lambda: self.show_message("按钮1"))
        horizontal_group.add_new("按钮2", command=lambda: self.show_message("按钮2"))
        horizontal_group.add_new("按钮3", command=lambda: self.show_message("按钮3"))
        
        # 垂直按钮组
        vertical_group = ButtonGroup(
            self.root,
            direction="vertical",
            spacing=4,
            align="left"
        )
        
        # 添加几个按钮
        vertical_group.add_new("垂直按钮1", command=lambda: self.show_message("垂直按钮1"))
        vertical_group.add_new("垂直按钮2", command=lambda: self.show_message("垂直按钮2"))
        
        # 右对齐按钮组
        right_group = ButtonGroup(
            self.root,
            direction="horizontal",
            spacing=8,
            align="right"
        )
        
        # 添加操作按钮
        right_group.add_new("保存", command=self.save)
        right_group.add_new("取消", command=self.cancel)
        
    def show_message(self, button_text):
        """显示按钮点击消息"""
        print(f"点击了 {button_text}")
        
    def save(self):
        """保存操作"""
        print("执行保存操作")
        
    def cancel(self):
        """取消操作"""
        print("执行取消操作")

def main():
    root = tk.Tk()
    app = ButtonGroupDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 