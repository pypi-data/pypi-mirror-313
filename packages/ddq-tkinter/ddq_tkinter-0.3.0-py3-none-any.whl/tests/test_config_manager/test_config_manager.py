import pytest
import os
import shutil
import json
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
    
    yield manager
    
    # 清理测试目录
    if os.path.exists(test_config_dir):
        shutil.rmtree(test_config_dir)

def test_config_manager_creation(config_manager):
    """测试配置管理器的基本创建"""
    assert isinstance(config_manager, ConfigManager)
    # 配置文件会在第一次保存时创建
    assert hasattr(config_manager, 'config_file')

def test_save_get_config(config_manager):
    """测试配置的保存和获取"""
    test_config = {"name": "test", "age": "18"}
    
    # 保存配置
    config_manager.save_config("test_config", test_config)
    
    # 验证配置文件存��
    assert "test_config" in config_manager.get_config_names()
    
    # 获取并验证配置
    configs = config_manager.configs
    assert "test_config" in configs
    assert configs["test_config"] == test_config

def test_get_config_names(config_manager):
    """测试获取配置名称列表"""
    # 保存一些测试配置
    config_manager.save_config("config1", {"name": "test1"})
    config_manager.save_config("config2", {"name": "test2"})
    
    # 获取配置名称列表
    names = config_manager.get_config_names()
    assert "config1" in names
    assert "config2" in names

def test_delete_config(config_manager):
    """测试删除配置"""
    # 先保存一个配置
    config_manager.save_config("test_config", {"name": "test"})
    assert "test_config" in config_manager.get_config_names()
    
    # 删除配置
    config_manager.delete_config("test_config")
    assert "test_config" not in config_manager.get_config_names()

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 