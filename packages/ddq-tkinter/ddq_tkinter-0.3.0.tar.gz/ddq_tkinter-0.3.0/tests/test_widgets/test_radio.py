import pytest
import tkinter as tk
from ddq_widgets.ddq_radio import Radio

@pytest.fixture(scope="session")

def test_radio_creation(root_window):
    """测试单选框组的基本创建"""
    options = ["选项1", "选项2", "选项3"]
    radio = Radio(root_window, options=options)
    
    assert isinstance(radio, Radio)
    assert isinstance(radio, tk.Frame)
    assert len(radio.buttons) == len(options)  # 验证按钮数量
    
    # 验证每个按钮都是 Radiobutton
    for btn in radio.buttons:
        assert isinstance(btn, tk.Radiobutton)

def test_radio_value(root_window):
    """测试单选框的值操作"""
    options = ["选项1", "选项2", "选项3"]
    radio = Radio(root_window, options=options)
    
    # 测试默认值
    assert radio.value == options[0]  # 默认选中第一项
    
    # 测试设置值
    radio.value = "选项2"
    assert radio.value == "选项2"
    assert str(radio.var.get()) == "选项2"

def test_radio_default_value(root_window):
    """测试默认值设置"""
    options = ["选项1", "选项2", "选项3"]
    radio = Radio(root_window, options=options, default="选项2")
    
    assert radio.value == "选项2"  # 验证默认值
    assert str(radio.var.get()) == "选项2"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 