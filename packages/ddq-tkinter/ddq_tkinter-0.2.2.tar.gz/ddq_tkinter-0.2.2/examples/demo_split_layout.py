import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_split_layout import SplitLayout

class SplitLayoutDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("SplitLayout 组件示例")
        self.root.geometry("800x600")
        
        # 创建分屏布局
        self.split = SplitLayout(root, right_scrollable=True,left_width=200)
        
        # 在左侧添加一些示例内容
        left_content = ttk.Frame(self.split.left, style='Demo.TFrame')
        left_content.pack(fill=tk.BOTH, expand=True)
        
        # 添加一些控件到左侧
        ttk.Label(left_content, text="左侧面板", font=('Arial', 14)).pack(pady=10)
        ttk.Button(left_content, text="测试按钮1").pack(pady=5)
        ttk.Button(left_content, text="测试按钮2").pack(pady=5)
        
        # 添加一个文本区域
        text = tk.Text(left_content, height=10)
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert('1.0', "这是一个测试文本区域\n" * 5)
        
        # 在右侧添加一些示例内容
        right_content = ttk.Frame(self.split.right, style='Demo.TFrame')
        right_content.pack(fill=tk.BOTH, expand=True)
        
        # 添加一些控件到右侧
        ttk.Label(right_content, text="右侧面板", font=('Arial', 14)).pack(pady=10)
        ttk.Entry(right_content).pack(fill=tk.X, padx=5, pady=5)
        
        # 添加一个列表框
        listbox = tk.Listbox(right_content)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for i in range(20):
            listbox.insert(tk.END, f"列表项 {i+1}")
            
        # 添加控制按钮
        control_frame = ttk.Frame(right_content)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="隐藏左侧", 
                  command=self.split.toggle_left).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="隐藏右侧", 
                  command=self.split.toggle_right).pack(side=tk.LEFT, padx=5)

def main():
    root = tk.Tk()
    app = SplitLayoutDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 