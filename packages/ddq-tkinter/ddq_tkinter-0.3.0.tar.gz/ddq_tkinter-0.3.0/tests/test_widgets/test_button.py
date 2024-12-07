import pytest
import tkinter as tk
from ddq_widgets.ddq_button import Button

@pytest.fixture(scope="session")
def test_button_creation(root_window):
    """测试按钮的基本创建"""
    btn = Button(root_window, text="测试按钮")
    assert isinstance(btn, Button)
    assert isinstance(btn, tk.Button)
    assert btn.cget("text") == "测试按钮"

def test_button_style(root_window):
    """测试按钮样式"""
    btn = Button(root_window)
    
    # 验证默认样式
    assert btn.cget("bg") == "#007bff"  # 背景色
    assert btn.cget("fg") == "white"    # 文字颜色
    assert int(btn.cget("border")) == 0  # 无边框
    assert int(btn.cget("padx")) == 8   # 水平内边距

def test_button_hover_effect(root_window):
    """测试按钮悬停效果"""
    btn = Button(root_window)
    
    # 直接调用悬停方法
    btn.on_hover(None)  # None 代替事件对象
    assert btn.cget("bg") == "#0056b3"  # 悬停背景色
    
    # 直接调用离开方法
    btn.on_leave(None)  # None 代替事件对象
    assert btn.cget("bg") == "#007bff"  # 恢复默认背景色

def test_button_command(root_window):
    """测试按钮点击事件"""
    clicked = False
    
    def on_click():
        nonlocal clicked
        clicked = True
    
    btn = Button(root_window, command=on_click)
    
    # 模拟按钮点击
    btn.invoke()
    assert clicked is True

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 