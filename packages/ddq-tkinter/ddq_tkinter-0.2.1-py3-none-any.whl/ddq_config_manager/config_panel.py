import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ddq_widgets import ButtonGroup, Card, Listbox
from .config_manager import ConfigManager

class ConfigPanel(ttk.Frame):
    """配置管理面板组件"""
    def __init__(self, master, config_manager: ConfigManager):
        super().__init__(master)
        self.config_manager = config_manager
        
        # 确保面板本身填充父容器
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个带表单项的卡片
        form_card = Card(self, title="已保存的配置", expand=True)
        form_card.pack(fill=tk.BOTH, expand=True)
        
        # 使用 ButtonGroup 创建按钮组
        self.button_group = ButtonGroup(form_card.content)
        self.button_group.add_new("另存为", command=self._save_as)
        self.button_group.add_new("重命名", command=self._rename)
        self.button_group.add_new("删除", command=self._delete)
        self.button_group.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # 使用 Listbox 组件
        self.config_listbox = Listbox(form_card.content)
        self.config_listbox.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # 绑定选择事件
        self.config_listbox.on_select(self._on_select)
        
        # 分别定义获取和设置配置的回调
        self.on_config_save = None  # 用于获取当前配置
        self.on_config_load = None  # 用于加载新配置
        
        # 刷新配置列表
        self.refresh_config_list()
        
    def refresh_config_list(self):
        """刷新配置列表"""
        # 使用 Listbox 的 set_items 方法
        self.config_listbox.set_items(self.config_manager.get_config_names())
            
    def _on_select(self, name):
        """处理配置选择事件"""
        if not name:
            return
            
        # 先保存当前配置
        last_selected = self.config_manager.get_last_selected()
        if last_selected and self.on_config_save:
            current_config = self.on_config_save()
            if current_config:
                self.config_manager.save_config(last_selected, current_config)
        
        # 加载新配置
        if self.on_config_load:
            config_data = self.config_manager.get_config(name)
            self.on_config_load(name, config_data)
        
        # 更新最后选中的配置
        self.config_manager.set_last_selected(name)
        
    def select_last_config(self):
        """选择上次使用的配置"""
        last_selected = self.config_manager.get_last_selected()
        if last_selected:
            # 获取配置内容
            config = self.config_manager.get_config(last_selected)
            
            # 在列表中选中该配置
            self.config_listbox.set_selection(last_selected)
            
            # 加载配置
            if self.on_config_load:
                self.on_config_load(last_selected, config)
                
    def _save_as(self):
        """另存为新配置"""
        name = simpledialog.askstring("保存配置", "请输入配置名称：")
        if name:
            if name == "默认配置":
                messagebox.showwarning("警告", "不能使用'默认配置'作为配置名")
                return
            if name in self.config_manager.get_config_names():
                if not messagebox.askyesno("确认", f"配置'{name}'已存在，是否覆盖？"):
                    return
                
            # 获取当前配置
            if self.on_config_save:
                current_config = self.on_config_save()
                if current_config:
                    # 保存配置
                    self.config_manager.save_config(name, current_config)
                    # 刷新列表
                    self.refresh_config_list()
                    # 选中新保存的配置
                    self.config_listbox.set_selection(name)
                    self.config_manager.set_last_selected(name)
        
    def _rename(self):
        """重命名配置"""
        selected = self.config_listbox.get_selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要重命名的配置")
            return
        
        if selected == "默认配置":
            messagebox.showwarning("警告", "默认配置不能重命名")
            return
        
        new_name = simpledialog.askstring("重命名配置", "请输入新的配置名称：", initialvalue=selected)
        if new_name and new_name != selected:
            if new_name == "默认配置":
                messagebox.showwarning("警告", "不能使用'默认配置'作为配置名")
                return
            if new_name in self.config_manager.get_config_names():
                messagebox.showwarning("警告", f"配置名'{new_name}'已存在")
                return
            
            self.config_manager.rename_config(selected, new_name)
            self.refresh_config_list()
            # 选中重命名后的配置
            self.config_listbox.set_selection(new_name)
            
    def _delete(self):
        """删除配置"""
        selected = self.config_listbox.get_selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的配置")
            return
        
        if selected == "默认配置":
            messagebox.showwarning("警告", "默认配置不能删除")
            return
        
        if messagebox.askyesno("确认", f"确定要删除配置'{selected}'吗？"):
            # 删除配置
            self.config_manager.delete_config(selected)
            self.refresh_config_list()
            
            # 获取所有配置名
            items = self.config_listbox.get_items()
            
            # 如果还有其他配置，选中第一个配置
            if items:
                self.config_listbox.set_selection(items[0])
                # 加载选中的配置
                if self.on_config_load:
                    config_data = self.config_manager.get_config(items[0])
                    self.on_config_load(items[0], config_data)
                    # 更新最后选中的配置
                    self.config_manager.set_last_selected(items[0])