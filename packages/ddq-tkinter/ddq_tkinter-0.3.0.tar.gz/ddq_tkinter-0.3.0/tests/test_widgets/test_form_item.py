import pytest
import tkinter as tk
from tkinter import ttk
from ddq_widgets import FormItem

@pytest.fixture(scope="session")

def test_form_item_basic(root_window):
    """测试基本的表单项创建"""
    item = FormItem(root_window, "测试标签")
    assert isinstance(item, FormItem)
    assert item.label.cget("text") == "测试标签"
    assert item.widget is None

def test_form_item_required(root_window):
    """测试必填项功能"""
    item = FormItem(root_window, "必填项", required=True)
    assert item.required is True
    assert str(item.label.cget("foreground")) == "red"

def test_form_item_input(root_window):
    """测试输入框表单项"""
    item = FormItem.input(root_window, "用户名", placeholder="请输入用户名")
    assert item.label.cget("text") == "用户名"
    assert hasattr(item, "var")
    
    # 测试值的设置和获取
    item.value = "test_user"
    assert item.value == "test_user"

def test_form_item_password(root_window):
    """测试密码输入框"""
    item = FormItem.password(root_window, "密码", placeholder="请输入密码")
    assert item.label.cget("text") == "密码"
    assert hasattr(item, "var")
    
    # 测试值的设置和获取
    item.value = "123456"
    assert item.value == "123456"

def test_form_item_select(root_window):
    """测试下拉选择框"""
    options = ["选项1", "选项2", "选项3"]
    item = FormItem.select(root_window, "选择", options=options)
    assert item.label.cget("text") == "选择"
    assert isinstance(item.widget, ttk.Combobox)
    assert list(item.widget["values"]) == options
    
    # 测试值的设置和获取
    item.value = "选项2"
    assert item.value == "选项2"

def test_form_item_radio(root_window):
    """测试单选框组"""
    options = ["选项1", "选项2", "选项3"]
    item = FormItem.radio(root_window, "单选", options=options)
    assert item.label.cget("text") == "单选"
    
    # 测试值的设置和获取
    item.value = "选项2"
    assert item.value == "选项2"

def test_form_item_checkbox(root_window):
    """测试复选框组"""
    options = ["选项1", "选项2", "选项3"]
    item = FormItem.checkbox(root_window, "多选", options=options)
    assert item.label.cget("text") == "多选"
    
    # 测试值的设置和获取
    item.value = ["选项1", "选项3"]
    assert item.value == ["选项1", "选项3"]

def test_form_item_textarea(root_window):
    """测试多行文本框"""
    item = FormItem.textarea(root_window, "描述", height=3)
    assert item.label.cget("text") == "描述"
    
    # 测试值的设置和获取
    test_text = "这是一段测试文本\n第二行"
    item.value = test_text
    assert item.value == test_text

def test_form_item_file_picker(root_window):
    """测试文件选择器"""
    item = FormItem.file_picker(
        root_window, 
        "文件",
        mode="file",
        filetypes=[("文本文件", "*.txt")]
    )
    assert item.label.cget("text") == "文件"
    assert hasattr(item, "var")

def test_form_item_visibility(root_window):
    """测试表单项的显示和隐藏"""
    item = FormItem.input(root_window, "测试")
    assert item.visible is True
    
    item.hide()
    assert item.visible is False
    
    item.show()
    assert item.visible is True

def test_form_item_state(root_window):
    """测试表单项状态设置"""
    item = FormItem.input(root_window, "测试")
    
    item.set_state("disabled")
    assert str(item.widget.cget("state")) == "disabled"
    
    item.set_state("normal")
    assert str(item.widget.cget("state")) == "normal"

def test_form_item_change_event(root_window):
    """测试值变化事件"""
    item = FormItem.input(root_window, "测试")
    
    callback_count = 0
    def on_change(value):
        nonlocal callback_count
        callback_count += 1
    
    item.on_change(on_change)
    item.value = "new value"
    
    # 等待事件处理
    for _ in range(10):  # 多次更新以确保事件被处理
        root_window.update()
        if callback_count > 0:
            break
            
    assert callback_count > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 