import pytest
import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_listbox import Listbox

@pytest.fixture(scope="session")

def test_listbox_creation(root_window):
    """测试列表框的基本创建"""
    listbox = Listbox(root_window)
    assert isinstance(listbox, Listbox)
    assert isinstance(listbox.listbox, tk.Listbox)
    assert isinstance(listbox.scrollbar, ttk.Scrollbar)

def test_listbox_items(root_window):
    """测试列表项的添加和获取"""
    listbox = Listbox(root_window)
    items = ["选项1", "选项2", "选项3"]
    
    # 使用 set_items 方法
    listbox.set_items(items)
    assert listbox.get_items() == items

def test_listbox_add_remove(root_window):
    """测试添加和删除项目"""
    listbox = Listbox(root_window)
    
    # 测试添加
    listbox.add_item("选项1")
    assert "选项1" in listbox.get_items()
    
    # 测试删除
    listbox.remove_item("选项1")
    assert "选项1" not in listbox.get_items()

def test_listbox_selection(root_window):
    """测试选择功能"""
    listbox = Listbox(root_window)
    items = ["选项1", "选项2", "选项3"]
    listbox.set_items(items)
    
    # 测试选择
    listbox.set_selection("选项2")
    assert listbox.get_selection() == "选项2"

def test_listbox_clear(root_window):
    """测试清空功能"""
    listbox = Listbox(root_window)
    items = ["选项1", "选项2", "选项3"]
    listbox.set_items(items)
    
    listbox.clear()
    assert len(listbox.get_items()) == 0

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 