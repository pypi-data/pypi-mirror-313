import json
import os
import sys
from typing import Dict, List

class ConfigManager:
    """工具配置管理器"""
    
    def __init__(self, tool_dir: str):
        """初始化配置管理器"""
        # 直接使用传入的目录，在其下创建 configs 目录
        self.config_dir = os.path.join(tool_dir, 'configs')
        
        # 确保配置目录存在
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.config_file = os.path.join(self.config_dir, 'configs.json')
        print(f"配置文件路径: {self.config_file}")
        
        # 初始化配置
        self.configs = self._load_configs()
        if not self.configs:
            self.configs = {
                '_meta': {
                    'last_selected': '默认配置',
                    'window': {
                        'width': 800,
                        'height': 600,
                        'x': None,
                        'y': None
                    }
                },
                '默认配置': {}
            }
            self._save_to_file()

    def _validate_configs(self, configs: Dict) -> bool:
        """验证配置数据的有效性"""
        if not isinstance(configs, dict):
            return False
            
        # 验证_meta
        if '_meta' not in configs or not isinstance(configs['_meta'], dict):
            return False
        if 'last_selected' not in configs['_meta']:
            return False
            
        # 验证默认配置
        if '默认配置' not in configs:
            return False
            
        return True

    def _load_configs(self) -> Dict:
        """加载配置"""
        default_configs = {
            '_meta': {'last_selected': '默认配置'},
            '默认配置': {}
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    configs = json.load(f)
                    
                    # 验证配置数据结构
                    if not self._validate_configs(configs):
                        print("配置文件格式无效，使用默认配置")
                        return default_configs
                    
                    # 确保默认配置不是 None
                    if configs['默认配置'] is None:
                        configs['默认配置'] = {}
                        
                    print(f"加载的配置: {configs}")
                    return configs
            else:
                print(f"配置文件不存在，使用默认配置: {self.config_file}")
                return default_configs
                
        except json.JSONDecodeError as e:
            print(f"配置文件解析失败: {e}")
            # 尝试备份损坏的配置文件
            self._backup_corrupted_config()
            
        except Exception as e:
            print(f"加载配置出错: {e}")
            
        return default_configs

    def _backup_corrupted_config(self):
        """备份损坏的配置文件"""
        try:
            if os.path.exists(self.config_file):
                backup_file = f"{self.config_file}.bak"
                os.rename(self.config_file, backup_file)
                print(f"已备份损坏的配置文件到: {backup_file}")
        except Exception as e:
            print(f"备份配置文件失败: {e}")

    def _save_to_file(self) -> bool:
        """保存配置到文件"""
        try:
            # 验证配置数据
            if not self._validate_configs(self.configs):
                print("配置数据无效，取消保存")
                return False
                
            # 创建临时文件
            temp_file = f"{self.config_file}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, ensure_ascii=False, indent=2)
                
            # 安全替换原文件
            os.replace(temp_file, self.config_file)
            return True
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def save_config(self, name: str, config_data: Dict) -> None:
        """保存配置"""
        self.configs[name] = config_data
        self._save_to_file()

    def get_config(self, name: str) -> Dict:
        """获取配置"""
        return self.configs.get(name, {})

    def get_config_names(self) -> List[str]:
        """获取所有配置名称"""
        return [name for name in self.configs.keys() if name != '_meta']

    def delete_config(self, name: str) -> None:
        """删除配置"""
        if name in self.configs:
            del self.configs[name]
            if self.configs['_meta']['last_selected'] == name:
                self.configs['_meta']['last_selected'] = '默认配置'
            self._save_to_file()

    def set_last_selected(self, name: str) -> None:
        """设置最后选中的配置"""
        self.configs['_meta']['last_selected'] = name
        self._save_to_file()

    def get_last_selected(self) -> str:
        """获取最后选中的配置"""
        return self.configs['_meta'].get('last_selected', '默认配置')

    def rename_config(self, old_name: str, new_name: str) -> None:
        """重命名配置"""
        if old_name in self.configs and old_name != '默认配置':
            # 保存配置内容
            config_data = self.configs[old_name]
            # 删除旧配置
            del self.configs[old_name]
            # 添加新配置
            self.configs[new_name] = config_data
            # 如果重命名的是当前选中的配置，更新last_selected
            if self.configs['_meta']['last_selected'] == old_name:
                self.configs['_meta']['last_selected'] = new_name
            # 保存到文件
            self._save_to_file()

    def save_window_state(self, width: int, height: int, x: int = None, y: int = None) -> None:
        """保存窗口状态"""
        if '_meta' not in self.configs:
            self.configs['_meta'] = {}
        if 'window' not in self.configs['_meta']:
            self.configs['_meta']['window'] = {}
        
        self.configs['_meta']['window'].update({
            'width': width,
            'height': height,
            'x': x,
            'y': y
        })
        self._save_to_file()

    def get_window_state(self) -> Dict:
        """获取窗口状态"""
        if '_meta' in self.configs and 'window' in self.configs['_meta']:
            return self.configs['_meta']['window']
        return {
            'width': 800,
            'height': 600,
            'x': None,
            'y': None
        }