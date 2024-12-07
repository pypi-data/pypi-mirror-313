import pytest
import tkinter as tk
from ddq_widgets import FilePicker

@pytest.fixture
def file_picker(root_window):
    """创建 FilePicker 实例"""
    picker = FilePicker(root_window)
    picker.pack()
    root_window.update()
    return picker

def test_initial_state(file_picker):
    """测试初始状态"""
    # 测试默认模式
    assert file_picker._mode == "file"
    # 测试默认文件类型
    assert file_picker.filetypes == [("所有文件", "*.*")]
    # 测试初始值为空
    assert file_picker.value == ""

def test_value_property(file_picker):
    """测试 value 属性的获取和设置"""
    test_path = "/test/path/file.txt"
    # 设置值
    file_picker.value = test_path
    # 验证值
    assert file_picker.value == test_path
    # 验证路径变量
    assert file_picker.path_var.get() == test_path

def test_placeholder(root_window):
    """测试占位符功能"""
    # 测试默认状态（无占位符）
    default_picker = FilePicker(root_window)
    default_picker.pack()
    root_window.update()
    
    # 默认应该是空字符串，颜色是黑色
    assert default_picker.entry.get() == ""
    assert str(default_picker.entry.cget("foreground")) == "black"
    
    # 测试有占位符的状态
    placeholder = "请选择文件"
    file_picker = FilePicker(root_window, placeholder=placeholder)
    file_picker.pack()
    root_window.update()
    
    # 测试初始状态
    assert file_picker.entry.get() == placeholder
    assert str(file_picker.entry.cget("foreground")) == "gray"
    
    # 测试设置值后的状态
    test_path = "/test/path/file.txt"
    file_picker.value = test_path
    assert file_picker.entry.get() == test_path
    assert str(file_picker.entry.cget("foreground")) == "black"
    
    # 测试清空值后的状态
    file_picker.value = ""
    assert file_picker.entry.get() == placeholder
    assert str(file_picker.entry.cget("foreground")) == "gray"

def test_mode_setting(file_picker):
    """测试模式设置"""
    # 测试文件模式
    file_picker.set_mode("file")
    file_picker.master.update()
    assert file_picker.file_button.winfo_manager() == "pack"
    assert file_picker.folder_button.winfo_manager() == ""
    
    # 测试文件夹模式
    file_picker.set_mode("folder")
    file_picker.master.update()
    assert file_picker.file_button.winfo_manager() == ""
    assert file_picker.folder_button.winfo_manager() == "pack"
    
    # 测试全部模式
    file_picker.set_mode("all")
    file_picker.master.update()
    assert file_picker.file_button.winfo_manager() == "pack"
    assert file_picker.folder_button.winfo_manager() == "pack"
    
    # 测试无效模式
    with pytest.raises(ValueError):
        file_picker.set_mode("invalid")

def test_custom_filetypes(root_window):
    """测试自定义文件类型"""
    filetypes = [
        ("Text files", "*.txt"),
        ("Python files", "*.py")
    ]
    file_picker = FilePicker(root_window, filetypes=filetypes)
    assert file_picker.filetypes == filetypes

def test_set_path(file_picker):
    """测试设置路径方法"""
    # 先测试空路径
    file_picker.set_path("")
    assert file_picker.path_var.get() == ""
    
    # 再测试设置路径
    test_path = "/test/path/file.txt"
    file_picker.set_path(test_path)
    assert file_picker.path_var.get() == test_path
    assert str(file_picker.entry.cget("foreground")) == "black"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 