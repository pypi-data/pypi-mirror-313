import tkinter as tk
from tkinter import ttk
from ddq_widgets import Listbox

class ListboxDemo:
    def __init__(self, master):
        self.master = master
        self.master.title("Listbox 组件示例")
        
        # 创建主框架
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧列表区域
        left_frame = ttk.LabelFrame(main_frame, text="列表操作示例")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 创建 Listbox
        self.listbox = Listbox(left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加一些测试数据
        test_data = [f"列表项 {i}" for i in range(1, 21)]
        self.listbox.set_items(test_data)
        
        # 绑定选择事件
        self.listbox.on_select(self.on_item_select)
        
        # 创建右侧控制区域
        right_frame = ttk.LabelFrame(main_frame, text="控制面板")
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        
        # 添加控制按钮
        ttk.Button(right_frame, text="添加项", command=self.add_item).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="删除选中项", command=self.remove_selected).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="清空列表", command=self.clear_list).pack(fill=tk.X, pady=2)
        
        # 添加选中项显示
        ttk.Label(right_frame, text="当前选中:").pack(pady=(10, 0))
        self.selection_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.selection_var).pack()
        
        # 添加项目数量显示
        ttk.Label(right_frame, text="项目数量:").pack(pady=(10, 0))
        self.count_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.count_var).pack()
        
        # 更新显示
        self.update_count()
        
    def on_item_select(self, item):
        """处理列表项选择事件"""
        self.selection_var.set(item or "无")
        
    def add_item(self):
        """添加新列表项"""
        count = len(self.listbox.get_items())
        self.listbox.add_item(f"新项目 {count + 1}")
        self.update_count()
        
    def remove_selected(self):
        """删除选中的列表项"""
        selected = self.listbox.get_selection()
        if selected:
            self.listbox.remove_item(selected)
            self.update_count()
            self.selection_var.set("无")
            
    def clear_list(self):
        """清空列表"""
        self.listbox.clear()
        self.update_count()
        self.selection_var.set("无")
        
    def update_count(self):
        """更新项目数量显示"""
        count = len(self.listbox.get_items())
        self.count_var.set(str(count))

def main():
    root = tk.Tk()
    root.geometry("400x500")
    app = ListboxDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 