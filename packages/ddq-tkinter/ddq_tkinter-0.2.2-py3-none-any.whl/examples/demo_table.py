import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_table import Table

def export_data():
    """导出数据"""
    table.export_data()

def add_record():
    """添加记录"""
    # 模拟添加一条新记录
    table.insert_record([
        "新员工",
        "25",
        "开发",
        "本科",
        "8000"
    ])

def main():
    root = tk.Tk()
    root.title("Table Demo")
    root.geometry("800x600")
    
    # 定义列配置
    columns = [
        {"id": "name", "text": "姓名"},
        {"id": "age", "text": "年龄"},
        {"id": "dept", "text": "部门"},
        {"id": "education", "text": "学历"},
        {"id": "salary", "text": "薪资"},
    ]
    
    # 定义按钮配置
    buttons = [
        {"text": "添加", "command": add_record},
        {"text": "导出", "command": export_data},
    ]
    
    # 创建表格
    global table  # 使其可以在回调函数中访问
    table = Table(
        root,
        title="员工列表",
        columns=columns,
        buttons=buttons
    )
    
    # 插入一些示例数据
    sample_data = [
        ["张三", "30", "技术部", "本科", "10000"],
        ["李四", "25", "市场部", "硕士", "12000"],
        ["王五", "35", "销售部", "大专", "15000"],
        ["赵六", "28", "技术部", "本科", "11000"],
        ["钱七", "32", "人事部", "本科", "9000"],
    ]
    
    # 添加示例数据
    for record in sample_data:
        table.insert_record(record)
    
    root.mainloop()

if __name__ == "__main__":
    main() 