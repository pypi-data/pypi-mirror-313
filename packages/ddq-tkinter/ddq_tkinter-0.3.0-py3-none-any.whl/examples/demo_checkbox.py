import tkinter as tk
from ddq_widgets import Checkbox, Card

class CheckboxDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkbox 组件示例")
        self.root.geometry("600x400")
        
        # 水平布局示例
        h_card = Card(self.root, title="水平布局")
        
        # 创建水平复选框组
        h_options = ["选项A", "选项B", "选项C"]
        h_checkbox = Checkbox(
            h_card.content,
            options=h_options,
            default_values=["选项A"],  # 默认选中第一个选项
            layout="horizontal"
        )
        h_checkbox.pack()
        
        # 添加值显示标签
        h_label = tk.Label(h_card.content, text="当前值: ['选项A']")
        h_label.pack()
        
        # 更新值显示
        def update_h_label():
            h_label.config(text=f"当前值: {h_checkbox.value}")
            self.root.after(100, update_h_label)
        update_h_label()
        
        # 垂直布局示例
        v_card = Card(self.root, title="垂直布局")
        
        # 创建垂直复选框组
        v_options = ["Python开发", "Web前端", "数据分析", "人工智能"]
        v_checkbox = Checkbox(
            v_card.content,
            options=v_options,
            layout="vertical"
        )
        v_checkbox.pack()
        
        # 添加值显示标签
        v_label = tk.Label(v_card.content, text="当前值: []")
        v_label.pack()
        
        # 更新值显示
        def update_v_label():
            v_label.config(text=f"当前值: {v_checkbox.value}")
            self.root.after(100, update_v_label)
        update_v_label()
        
        # 添加控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        
        # 全选按钮
        def select_all():
            v_checkbox.value = v_options
        select_btn = tk.Button(control_frame, text="全选", command=select_all)
        select_btn.pack(side=tk.LEFT)
        
        # 取消全选按钮
        def clear_all():
            v_checkbox.value = []
        clear_btn = tk.Button(control_frame, text="取消全选", command=clear_all)
        clear_btn.pack(side=tk.LEFT)

def main():
    root = tk.Tk()
    app = CheckboxDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 