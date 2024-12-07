import pytest
import tkinter as tk
from tkinter import ttk
from ddq_widgets.ddq_split_layout import SplitLayout

@pytest.fixture(scope="session")
def root_window():
    """创建一个根窗口"""
    root = tk.Tk()
    root.geometry("800x600")
    return root

def test_split_layout_creation(root_window):
    """测试分割布局的基本创建"""
    split = SplitLayout(root_window)
    
    assert isinstance(split, SplitLayout)
    assert isinstance(split, ttk.Frame)
    assert hasattr(split, 'left')  # 验证左侧容器
    assert hasattr(split, 'right')  # 验证右侧容器
    
    # 验证容器类型
    assert isinstance(split.left, ttk.Frame)
    assert isinstance(split.right, ttk.Frame)

def test_split_layout_children(root_window):
    """测试分割布局的子组件添加"""
    split = SplitLayout(root_window)
    
    # 在左右容器中添加标签
    left_label = ttk.Label(split.left, text="左侧")
    right_label = ttk.Label(split.right, text="右侧")
    left_label.pack()
    right_label.pack()
    
    # 验证标签是否正确添加
    assert left_label.master == split.left
    assert right_label.master == split.right

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 