import pytest
import tkinter as tk
from ddq_widgets import Input

@pytest.fixture(scope="session")

def test_input_creation(root_window):
    """测试输入框的基本创建"""
    input = Input(root_window)
    assert isinstance(input, Input)
    assert hasattr(input, 'var')
    assert isinstance(input.var, tk.StringVar)

def test_input_placeholder(root_window):
    """测试输入框的占位符功能"""
    placeholder = "请输入内容"
    input = Input(root_window, placeholder=placeholder)
    
    # 初始状态应显示占位符
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"
    
    # 模拟获得焦点
    input.event_generate('<FocusIn>')
    root_window.update()
    assert input.var.get() == ""
    assert str(input.cget("foreground")) == "black"
    
    # 模拟失去焦点（无输入）
    input.event_generate('<FocusOut>')
    root_window.update()
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"

def test_input_value(root_window):
    """测试输入框的值操作"""
    input = Input(root_window)
    
    # 测试设置值
    test_value = "test_input"
    input.value = test_value
    assert input.value == test_value
    assert input.var.get() == test_value
    assert str(input.cget("foreground")) == "black"
    
    # 测试清空值
    input.value = ""
    assert input.value == ""
    assert input.var.get() == ""

def test_input_with_placeholder_value(root_window):
    """测试带占位符的输入框的值操作"""
    placeholder = "请输入内容"
    input = Input(root_window, placeholder=placeholder)
    
    # 初始状态
    assert input.value == ""  # value 属性应返回空字符串
    assert input.var.get() == placeholder  # 实际显示占位符
    
    # 设置实际值
    test_value = "test_input"
    input.value = test_value
    assert input.value == test_value
    assert input.var.get() == test_value
    assert str(input.cget("foreground")) == "black"
    
    # 清空值后应显示占位符
    input.value = ""
    assert input.value == ""
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"

def test_input_focus_events(root_window):
    """测试输入框的焦点事件"""
    placeholder = "请输入内容"
    input = Input(root_window, placeholder=placeholder)
    
    # 模拟获得焦点
    input.event_generate('<FocusIn>')
    root_window.update()
    assert input.var.get() == ""
    assert str(input.cget("foreground")) == "black"
    
    # 输入内容
    test_value = "test_input"
    input.var.set(test_value)
    
    # 模拟失去焦点（有输入）
    input.event_generate('<FocusOut>')
    root_window.update()
    assert input.var.get() == test_value
    assert str(input.cget("foreground")) == "black"
    
    # 清空内容
    input.var.set("")
    
    # 模拟失去焦点（无输入）
    input.event_generate('<FocusOut>')
    root_window.update()
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"

def test_input_change_event(root_window):
    """测试输入框的值变化事件"""
    input = Input(root_window)
    
    # 记录回调次数和值
    callback_count = 0
    last_value = None
    
    def on_change(value):
        nonlocal callback_count, last_value
        callback_count += 1
        last_value = value
    
    # 添加回调
    if hasattr(input, '_change_callbacks'):
        input._change_callbacks.append(on_change)
    
    # 设置值
    test_value = "test_input"
    input.value = test_value
    root_window.update()
    
    # 验证回调
    if hasattr(input, '_change_callbacks'):
        assert callback_count > 0
        assert last_value == test_value

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 