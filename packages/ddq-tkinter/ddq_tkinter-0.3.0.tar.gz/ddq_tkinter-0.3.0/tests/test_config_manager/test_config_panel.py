import pytest
import tkinter as tk
import os
import shutil
from ddq_config_manager.config_panel import ConfigPanel
from ddq_config_manager.config_manager import ConfigManager

@pytest.fixture
def config_manager():
    """创建测试用的配置管理器"""
    # 创建测试配置目录
    test_config_dir = "test_configs"
    if os.path.exists(test_config_dir):
        shutil.rmtree(test_config_dir)
    os.makedirs(os.path.join(test_config_dir, "configs"))
    
    # 创建配置管理器
    manager = ConfigManager(test_config_dir)
    
    # 添加一些测试配置
    manager.save_config("config1", {"name": "test1", "age": "18"})
    manager.save_config("config2", {"name": "test2", "age": "20"})
    
    yield manager
    
    # 清理测试目录
    if os.path.exists(test_config_dir):
        shutil.rmtree(test_config_dir)

def test_config_panel_creation(root_window, config_manager):
    """测试配置面板的基本创建"""
    panel = ConfigPanel(root_window, config_manager)
    assert isinstance(panel, ConfigPanel)

def test_config_list_refresh(root_window, config_manager):
    """测试配置列表刷新"""
    panel = ConfigPanel(root_window, config_manager)
    
    # 验证初始配置列表
    items = panel.config_listbox.get_items()
    assert "config1" in items
    assert "config2" in items

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 