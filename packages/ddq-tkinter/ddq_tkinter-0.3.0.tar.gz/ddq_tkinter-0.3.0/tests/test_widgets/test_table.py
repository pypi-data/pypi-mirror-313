import pytest
import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_table import Table

@pytest.fixture(scope="session")

def test_table_creation(root_window):
    """测试表格的基本创建"""
    columns = [
        {'id': 'name', 'text': '姓名', 'width': 100},
        {'id': 'age', 'text': '年龄', 'width': 80},
        {'id': 'gender', 'text': '性别', 'width': 80}
    ]
    table = Table(root_window, title="测试表格", columns=columns)
    assert isinstance(table, Table)
    assert isinstance(table.tree, ttk.Treeview)

def test_table_data(root_window):
    """测试表格数据的添加和获取"""
    columns = [
        {'id': 'name', 'text': '姓名', 'width': 100},
        {'id': 'age', 'text': '年龄', 'width': 80},
        {'id': 'gender', 'text': '性别', 'width': 80}
    ]
    data = [
        {"name": "张三", "age": "20", "gender": "男"},
        {"name": "李四", "age": "25", "gender": "女"}
    ]
    
    table = Table(root_window, title="测试表格", columns=columns)
    table.data = data

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 