import os
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable, List
from ddq_widgets import SplitLayout, ButtonGroup, Form
from .config_manager import ConfigManager
from .config_panel import ConfigPanel
import re
from abc import ABC, abstractmethod

class ConfigurableTool(ttk.Frame, ABC):
    """可配置的工具基类"""
    def __init__(
        self, 
        master, 
        tool_name: str, 
        config_dir: str,
        buttons: List[Dict[str, Any]] = None,
        default_config: Dict[str, Any] = None,
        on_form_change: Callable[[Dict[str, Any]], None] = None
    ):
        super().__init__(master)
        self.tool_name = tool_name
        self.master = master
        
        # 创建分割布局
        self.split = SplitLayout(self, left_width=300, left_scrollable=False)
        
        # 创建配置管理器和配置面板
        self.config_manager = ConfigManager(config_dir)
        self.config_panel = ConfigPanel(self.split.left, self.config_manager)
        
        # 保存回调方法
        self._on_form_change = on_form_change
        self.default_config = default_config or {}
        
        # 创建右侧容器
        self.right_container = ttk.Frame(self.split.right)
        self.right_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮组
        self.button_group = ButtonGroup(self.right_container)
        if buttons:
            for btn in buttons:
                handler_name = btn.get('handler', '')
                if handler_name and hasattr(self, handler_name):
                    handler = getattr(self, handler_name)
                    self.button_group.add_new(
                        text=btn['text'],
                        command=handler,
                        **{k: v for k, v in btn.items() if k not in ['text', 'handler']}
                    )
        
        # 创建表单
        self._form = self.create_form(self.right_container)
        if self._form and self._on_form_change:
            self._form.on_change(self._on_form_change)
            
        # 设置配置回调
        self.config_panel.on_config_save = self._save_current_config
        self.config_panel.on_config_load = self._load_config
        
        # 加载上次配置或默认配置
        self.after(100, self._load_initial_config)
        
        # 加载窗口状态
        window_state = self.config_manager.get_window_state()
        if window_state['width'] and window_state['height']:
            geometry = f"{window_state['width']}x{window_state['height']}"
            if window_state['x'] is not None and window_state['y'] is not None:
                geometry += f"+{window_state['x']}+{window_state['y']}"
            self.master.geometry(geometry)
        
        # 绑定窗口关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    @abstractmethod
    def create_form(self, parent: tk.Widget) -> Form:
        """创建表单的抽象方法，子类必须实现"""
        pass

    def _on_closing(self):
        """窗口关闭时保存窗口状态和当前配置"""
        # 保存当前配置
        last_selected = self.config_manager.get_last_selected()
        if last_selected and self._form:
            current_config = self._form.get_values()
            if current_config:
                self.config_manager.save_config(last_selected, current_config)
        
        # 保存窗口状态
        geometry = self.master.geometry()
        match = re.match(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", geometry)
        if match:
            width, height, x, y = map(int, match.groups())
            self.config_manager.save_window_state(width, height, x, y)
        
        self.master.destroy()
        
    def _save_current_config(self) -> Dict[str, Any]:
        """保存当前配置"""
        return self._form.get_values()
        
    def _load_config(self, config_name: str, config_data: Dict[str, Any]):
        """加载配置"""
        self._form.set_values(config_data)
        # 加载配置后触发一次表单变化事件，确保联动规则生效
        if self._on_form_change:
            self._on_form_change(config_data)

    def _load_initial_config(self):
        """加载上次配置或默认配置"""
        # 让配置面板选中上次的配置
        self.config_panel.select_last_config()
        
        # 如果没有上次配置，使用默认配置
        if not self.config_manager.get_last_selected():
            self._form.set_values(self.default_config)
            if self._on_form_change:
                self._on_form_change(self.default_config)