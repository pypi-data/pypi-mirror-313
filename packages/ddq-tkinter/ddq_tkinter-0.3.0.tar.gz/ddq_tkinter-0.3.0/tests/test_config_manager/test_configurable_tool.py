import pytest
import tkinter as tk
import os
import shutil
from ddq_config_manager.configurable_tool import ConfigurableTool
from ddq_widgets import Form

class TestTool(ConfigurableTool):
    """测试用的工具类"""
    def __init__(self, master):
        # 创建测试配置目录
        self.test_config_dir = "test_configs"
        if os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)
        os.makedirs(os.path.join(self.test_config_dir, "configs"))
        
        default_config = {
            "name": "test",
            "age": "18"
        }
        
        super().__init__(
            master=master,
            tool_name="Test Tool",
            config_dir=self.test_config_dir,
            default_config=default_config
        )
    
    def create_form(self, parent: tk.Widget) -> Form:
        """实现表单创建"""
        form = Form(parent)
        form.input("name", "姓名:")
        form.input("age", "年龄:")
        return form
        
    def __del__(self):
        """清理测试配置目录"""
        if hasattr(self, 'test_config_dir') and os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)

@pytest.fixture(scope="session")

def test_tool_creation(root_window):
    """测试工具的基本创建"""
    tool = TestTool(root_window)
    assert isinstance(tool, ConfigurableTool)
    assert tool.tool_name == "Test Tool"
    assert tool.default_config == {"name": "test", "age": "18"}

def test_form_creation(root_window):
    """测试表单创建"""
    tool = TestTool(root_window)
    assert isinstance(tool._form, Form)
    
    # 验证表单项
    form_values = tool._form.get_values()
    assert "name" in form_values
    assert "age" in form_values

def test_config_loading(root_window):
    """测试配置加载"""
    tool = TestTool(root_window)
    
    # 设置表单值
    tool._form.set_values(tool.default_config)
    
    # 验证配置被正确加载
    values = tool._form.get_values()
    assert values["name"] == "test"
    assert values["age"] == "18"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 