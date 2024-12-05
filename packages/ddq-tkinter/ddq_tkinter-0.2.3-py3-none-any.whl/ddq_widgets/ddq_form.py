import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Union, Optional

# 使用相对导入
from .ddq_card import Card
from .ddq_form_item import FormItem
from tkinter import messagebox


class Form(ttk.Frame):
    """表单容器组件，自动处理表单项的布局和样式"""
    
    def __init__(
        self,
        master,
        title: str = "",
        label_width: int = 12,
        spacing: int = 4,
        columns: int = 1,  # 添加列数参数
        use_card: bool = False,  # 添加是否使用卡片样式的选项
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 移除 expand=True，只保留水平方向的填充
        self.pack(fill=tk.X)
        
        # 如果需要卡片样式，创建 Card 作为容器
        if use_card:
            self.container = Card(self, title=title)
            self.container.pack(fill=tk.X)
            self.content = self.container.content
            parent = self.container.content
        else:
            parent = self
            self.content = self
            
        # 创建网格布局容器
        self.grid_frame = ttk.Frame(parent)
        self.grid_frame.pack(fill=tk.X)  # 这里也改为只填充水平方向
        
        self.label_width = label_width
        self._items: Dict[str, FormItem] = {}
        self._items_order: List[str] = []  # 新增: 记录表单项顺序
        self._change_callback = None
        self._current_row = 0
        self._current_col = 0
        self.columns = columns
        
        # 设置列权重
        for i in range(columns):
            self.grid_frame.columnconfigure(i, weight=1)
            
        self._default_values: Dict[str, Any] = {}
        self._initializing = True
        
        # 绑定点击事件，用于失去焦点
        self.bind('<Button-1>', self._handle_click)
        self.grid_frame.bind('<Button-1>', self._handle_click)
        
        # 如果使用了卡片样式，也需要绑定卡片的点击事件
        if use_card:
            self.container.bind('<Button-1>', self._handle_click)
            self.container.content.bind('<Button-1>', self._handle_click)

        self._submit_callback = None  # 添加提交回调

        print("Form initializing...")  # 添加日志
        
        self._initializing = False  # 初始化完成
        print("Form initialization complete")  # 添加日志

    def _create_form_item(self, item_type: str, name: str, label: str, **kwargs) -> FormItem:
        """统一的表单项创建方法"""
        print(f"Creating form item: {item_type}, {name}, {label}")  # 添加日志
        print(f"Current grid frame: {self.grid_frame}")  # 添加日志
        print(f"kwargs: {kwargs}")  # 添加日志
        # 获取对应的 FormItem 类方法
        create_method = getattr(FormItem, item_type)
        
        # 创建表单项
        item = create_method(self.grid_frame, label, **kwargs)
        print(f"Item created: {item}")  # 添加日志
        
        self._add_item(name, item)
       
        
        # 统一处理事件绑定
        self._bind_item_events(name, item)
        
        return item
        
    def _bind_item_events(self, name: str, item: FormItem):
        """统一的事件绑定处理"""
        print(f"Binding events for item: {name}")
        
        def on_item_change(*args):
            print(f"Item {name} changed, value: {item.value}")  # 添加值的日志
            if not self._initializing:
                print(f"Not initializing, triggering form change")
                self._notify_change()
            else:
                print(f"Still initializing, skipping form change")
            
        if isinstance(item, Form):
            print(f"Item {name} is a Form")
            item._change_callback = lambda values: self._notify_change()
        else:
            print(f"Item {name} is a FormItem")
            if hasattr(item, 'var'):
                print(f"Binding to var for {name}")
                item._change_callbacks = []
                item.var.trace_add('write', on_item_change)
                # 添加立即触发一次
                on_item_change()
            elif hasattr(item, 'vars'):
                print(f"Binding to vars for {name}")
                item._change_callbacks = []
                for var in item.vars:
                    var.trace_add('write', on_item_change)

    def _handle_click(self, event):
        """处理点击事件，使当前焦点的输入框失去焦点"""
        # 获取当前焦点控件
        focused = self.focus_get()
        if focused:
            # 如果当前有焦点控件，且点击的不是这个控件
            # 且不是 Combobox（下拉框）
            if (event.widget != focused and 
                not isinstance(focused, ttk.Combobox) and 
                not isinstance(event.widget, ttk.Combobox)):
                # 将焦点转移到表单容器上
                self.focus_set()
        
    def on_change(self, callback):
        """设置表单变化回调"""
        self._change_callback = callback
        
        # 如果是在初始化完成后设置回调，立即触发一次通知
        if not self._initializing:
            self._notify_change()
        return self
        
    def _add_item(self, name: str, item: FormItem):
        """添加表单项到网格"""
        item.pack(fill=tk.X, pady=2)
        self._items[name] = item
        self._items_order.append(name)
        item._form = self
        item._name = name  # 新增: 记录项的名称
        
    def _notify_change(self):
        """通知表单变化"""
        print("Form._notify_change called")
        print(f"Has callback: {self._change_callback is not None}")
        print(f"Initializing: {self._initializing}")
        
        if self._change_callback and not self._initializing:
            values = self.get_values()
            print(f"Form values: {values}")
            try:
                self._change_callback(values)
                print("Callback executed successfully")
            except Exception as e:
                print(f"Error in form change callback: {e}")
                
    def _create_change_callback(self, name: str):
        """创建变化回调"""
        def callback(*args):
            if not self._initializing:  # 确保不是在初始化阶段
                self._notify_change()
        return callback

    # 简化后的表单项方法
    def input(self, name: str, label: str, required: bool = False, **kwargs) -> FormItem:
        """创建输入框"""
        return self._create_form_item('input', name, label, required=required, **kwargs)
        
    def password(self, name: str, label: str, required: bool = False, **kwargs) -> FormItem:
        """添加密码输入框"""
        return self._create_form_item('password', name, label, required=required, **kwargs)
        
    def select(self, name: str, label: str, options: List[str], required: bool = False, **kwargs) -> FormItem:
        """添加下拉选择框"""
        kwargs['options'] = options
        return self._create_form_item('select', name, label, required=required, **kwargs)
        
    def textarea(self, name: str, label: str, required: bool = False, **kwargs) -> FormItem:
        """添加多行文本框"""
        return self._create_form_item('textarea', name, label, required=required, **kwargs)
        
    def radio(self, name: str, label: str, options: List[str], required: bool = False, **kwargs) -> FormItem:
        """添加单选框组"""
        kwargs['options'] = options
        return self._create_form_item('radio', name, label, required=required, **kwargs)
        
    def checkbox(self, name: str, label: str, options: List[str], required: bool = False, **kwargs) -> FormItem:
        """添加复选框组"""
        kwargs['options'] = options
        return self._create_form_item('checkbox', name, label, required=required, **kwargs)
        
    def file_picker(self, name: str, label: str, required: bool = False, **kwargs) -> FormItem:
        """添加文件选择器"""
        return self._create_form_item('file_picker', name, label, required=required, **kwargs)

    def get_values(self) -> Dict[str, Any]:
        """获取所有表单项的值，包括分区中的表单项"""
        values = {}
        
        # 遍历所有表单项
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区
                # 获取分区中的所有值并合并到主表单的值中
                section_values = item.get_values()
                values.update(section_values)
            else:
                # 普通表单项，直接获取值
                values[name] = item.value
        
        return values

    def set_values(self, values: Dict[str, Any]):
        """设置表单项的值"""
        # 遍历所有分区和表单项
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区
                # 过滤出属于这个分区的值
                section_values = {k: v for k, v in values.items() 
                                if k in item._items}
                item.set_values(section_values)  # 递归设置分区的值
            elif name in values:
                item.value = values[name]
        return self

    def set_defaults(self, values: Dict[str, Any]):
        """设置表单默认值"""
        self._default_values = values.copy()  # 保存默认值的副本
        
        # 遍历所有分区和表单项
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区
                # 过滤出属于这个分区的默认值
                section_values = {k: v for k, v in values.items() 
                                if k in item._items}
                item.set_defaults(section_values)  # 递归设置分区的默认值
        
        self.set_values(values)  # 设置当前值
        
        # 如果不是在初始化阶段，才触发变更通知
        if not self._initializing:
            self._notify_change()
        return self
        
    def set_state(self, state: str):
        """设置表单所有项的状态"""
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区
                item.set_state(state)  # 递归设置状态
            else:
                item.set_state(state)
        return self
    def reset(self, names: List[str] = None):
        """重置表单项到默认值"""
        if names is None:
            # 重置所有表单项，包括分区中的
            for name, item in self._items.items():
                if isinstance(item, Form):  # 如果是分区
                    item.reset()  # 递归重置分区
                elif name in self._default_values:
                    try:
                        # 直接设置默认值，不处理状态
                        item.value = self._default_values.get(name, "")
                    except Exception as e:
                        print(f"Reset error for {name}: {str(e)}")
        else:
            # 重置指定的表单项
            for name in names:
                if name in self._default_values:
                    for item_name, item in self._items.items():
                        if isinstance(item, Form):
                            if name in item._items:
                                item.reset([name])
                        elif item_name == name:
                            try:
                                item.value = self._default_values[name]
                            except Exception as e:
                                print(f"Reset error for {name}: {str(e)}")
        
        # 触发变更通知
        self._notify_change()
        
    def is_modified(self, name: str = None) -> Union[bool, Dict[str, bool]]:
        """检查表单项是否被修改"""
        current_values = self.get_values()
        
        if name is not None:
            # 检查指定表单项
            if name not in self._default_values:
                # 如果没有默认值，且当前值为空或默认空值，则认为未修改
                current_value = current_values.get(name)
                return bool(current_value) and current_value not in ('', [], None)
            return current_values[name] != self._default_values[name]
            
        # 检查所有表单项
        modified = {}
        for name, value in current_values.items():
            if name in self._default_values:
                modified[name] = value != self._default_values[name]
            else:
                # 如果没有默认值，且当前值为空或默认空值，则认为未修改
                modified[name] = bool(value) and value not in ('', [], None)
                
        return modified

    def section(self, title: str = "", columns: int = 1, content: Optional[tk.Widget] = None) -> 'Form':
        """创建表单分区
        Args:
            title: 分区标题
            columns: 列数
            content: 自定义内容组件，如果提供则使用此组件而不是创建新的Form
        Returns:
            Form: 分区表单对象
        """
        if content is not None:
            # 创建卡片容器
            card = Card(self.grid_frame, title=title)
            card.pack(fill=tk.X)
            
            # 将自定义内容放入卡片
            content.pack(in_=card.content, fill=tk.X)
            
            # 将卡片添加到items中以便管理
            section_name = title or f"section_{len(self._items)}"
            self._add_item(section_name, card)
            
            return card
        else:
            # 原有的Form创建逻辑
            sub_form = Form(
                self.grid_frame,
                title=title,
                columns=columns,
                use_card=True,
                label_width=self.label_width
            )
            
            section_name = title or f"section_{len(self._items)}"
            self._add_item(section_name, sub_form)
            
            sub_form._initializing = self._initializing
            sub_form._change_callback = lambda values: self._notify_change()
            
            return sub_form

    def submit(self) -> bool:
        """提交表单
        Returns:
            bool: 是否提交成功
        """
        # 1. 验证必填项
        empty_required = []
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区，递归验证
                if not item.submit():  # 如果子表单验证失败
                    return False
            elif hasattr(item, 'required') and item.required:
                value = item.value
                # 检查值是否为空（考虑不同类型的空值）
                is_empty = (
                    value is None 
                    or value == "" 
                    or value == [] 
                    or value == [""]
                )
                if is_empty:
                    empty_required.append(item.label.cget('text'))

        # 如果有必填项为空，显示错误消息
        if empty_required:
            fields = "\n".join(empty_required)
            messagebox.showerror(
                "表单验证失败",
                f"以下必填项不能为空：\n{fields}"
            )
            return False

        # 2. 收集所有数据
        values = self.get_values()

        # 3. 调用提交回调
        if self._submit_callback:
            try:
                self._submit_callback(values)
                return True
            except Exception as e:
                messagebox.showerror("提交失败", str(e))
                return False
        
        return True

    def on_submit(self, callback):
        """设置表单提交回调
        Args:
            callback: 接收表单数据的回调函数
        """
        self._submit_callback = callback
        return self

    def show(self):
        """显示表单"""
        self.pack(fill=tk.X)
        
    def hide(self):
        """隐藏表单"""
        self.pack_forget()

    def _reorder_visible_items(self):
        """重新排序所有可见的表单项"""
        visible_items = []
        
        # 按原始顺序收集所有可见项
        for name in self._items_order:
            item = self._items[name]
            if item._visible:
                item.pack_forget()  # 先取消布局
                visible_items.append(item)
        
        # 按顺序重新布局
        for item in visible_items:
            item.pack(fill=tk.X, pady=2)

    def text(self, name: str, label: str = "", text: str = "", **kwargs) -> FormItem:
        """添加文本展示项
        Args:
            name: 字段名
            label: 标签文本，可选
            text: 显示的文本内容
            **kwargs: 其他参数
        """
        return self._create_form_item('text', name, label, text=text, **kwargs)