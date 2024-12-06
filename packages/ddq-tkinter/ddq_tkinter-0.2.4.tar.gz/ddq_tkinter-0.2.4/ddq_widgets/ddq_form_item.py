import tkinter as tk
from tkinter import ttk
from typing import Optional, Literal, Any, List

# 添加 FilePicker 导入
from .ddq_file_picker import FilePicker
from .ddq_radio import Radio
from .ddq_checkbox import Checkbox
from .ddq_text import Text
from .ddq_input import Input  # 导入新的 Input 组件
from .ddq_textarea import Textarea  # 导入新的 Textarea 组件
from .ddq_password_input import PasswordInput  # 导入新组件

class FormItem(ttk.Frame):
    """表单项组件,处理标签和输入控件的布局和对齐"""
    
    def __init__(
        self,
        master,
        label: str,
        required: bool = False,  # 添加必填参数
        widget: Optional[tk.Widget] = None,
        label_width: int = 12,
        label_anchor: Literal["w", "e"] = "e",
        layout: Literal["horizontal", "vertical"] = "horizontal",
        **kwargs
    ):
        # 扩展需要过滤的参数列表
        frame_kwargs = {k: v for k, v in kwargs.items() 
                    if k not in [
                        'mode', 
                        'filetypes',
                        'placeholder',
                        'multiple_buttons',
                        'height',
                        'options',
                        'default'
                    ]}
        
        super().__init__(master, **frame_kwargs)
        self.pack(fill=tk.X)
        self._visible = True  # 添加可见性标记
        self._form = None  # 新增: Form 引用
        
        # 创建标签，如果是必填项则使用红色
        self.label = ttk.Label(
            self,
            text=label,
            anchor=label_anchor,
            width=label_width,
            foreground="red" if required else "black"  # 如果是必填项，文本为红色
        )
        
        # 设置输入控件
        self.widget = None
        if widget is not None:
            self.widget = self._setup_widget(widget)
            
        # 应用布局
        self._apply_layout(layout)
        
        # 添加事件回列表
        self._change_callbacks = []
        
    def _create_label(self, label: str, width: int, anchor: str) -> ttk.Label:
        """创建并配置标签"""
        return ttk.Label(
            self,
            text=label,
            anchor=anchor,
            width=width
        )

    def _setup_widget(self, widget: tk.Widget) -> tk.Widget:
        """设置输入控件"""
        widget.master = self
        
        # 绑定变量
        if hasattr(widget, 'var'):
            self.var = widget.var
        if hasattr(widget, 'vars'):
            self.vars = widget.vars
            
        return widget
    
    def _apply_layout(self, layout: str):
        """应用布局"""
        if layout == "horizontal":
            # 水平布局：标签在左，输入控件在右
            self.label.pack(side=tk.LEFT, padx=(0, 4))
            if self.widget:
                self.widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        else:
            # 垂直布局：标签在上，输入控件在下
            self.label.pack(side=tk.TOP, anchor="w", pady=(0, 4))
            if self.widget:
                self.widget.pack(side=tk.TOP, fill=tk.X, expand=True)

    def set_state(self, state: str):
        """统一的状设置方法"""
        if isinstance(self.widget, FilePicker):
            self.widget.set_state(state)
        elif isinstance(self.widget, (ttk.Entry, ttk.Combobox)):
            self.widget.configure(state=state)
        elif isinstance(self.widget, tk.Text):
            self.widget.configure(state='disabled' if state != 'normal' else 'normal')
        elif isinstance(self.widget, ttk.Frame):
            for child in self.widget.winfo_children():
                if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton, ttk.Button)):
                    child.configure(state=state)
        elif isinstance(self.widget, Text):
            self.widget.set_state(state)

    @classmethod
    def input(cls, master, label: str, placeholder=None, **kwargs) -> 'FormItem':
        """创建输入框"""
        item = cls(master, label, **kwargs)
        # 使用新的 Input 组件替代原来的 Entry
        entry = Input(item, placeholder=placeholder)
        item.widget = item._setup_widget(entry)
        item.var = entry.var  # 直接使用 Input 的 var
        
        # 保存 placeholder 到 FormItem 实例
        if placeholder:
            item._placeholder = placeholder
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def password(cls, master, label: str, placeholder=None, **kwargs) -> 'FormItem':
        """创建密码输入框"""
        item = cls(master, label, **kwargs)
        # 使用专门的密码输入组件
        entry = PasswordInput(item, placeholder=placeholder)
        item.widget = item._setup_widget(entry)
        item.var = entry.var
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def select(cls, master, label: str, options: List[str], **kwargs) -> 'FormItem':
        """创建下拉选择框"""
        item = cls(master, label, **kwargs)
        var = tk.StringVar()
        combo = ttk.Combobox(
            item,
            values=options,
            textvariable=var,
            state='readonly'
        )
        item.widget = item._setup_widget(combo)
        item.var = var
        
        # 设置默认选项
        if options:
            combo.set(options[0])
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def textarea(cls, master, label: str, height: int = 4, placeholder=None, **kwargs) -> 'FormItem':
        """创建多行文本框"""
        item = cls(master, label, **kwargs)
        
        # 使用 Textarea 组件替代原来的 tk.Text
        text = Textarea(
            item, 
            height=height,
            placeholder=placeholder
        )
        item.widget = item._setup_widget(text)
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def radio(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建单选框表单项"""
        # 从 kwargs 中分离出 frame 的参数和 Radio 的参数
        frame_kwargs = {k: v for k, v in kwargs.items() 
                       if k not in ['options', 'default', 'layout']}
        
        # 创建表单项
        item = cls(master, label, **frame_kwargs)
        
        # 创建单选框组
        radio = Radio(
            item,
            options=kwargs.get('options', []),
            default=kwargs.get('default'),
            layout=kwargs.get('layout', 'horizontal')
        )
        item.widget = item._setup_widget(radio)
        item.var = radio.var  # 保存变量引用
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        
        # 绑定变量变化事件
        item.var.trace_add('write', item._notify_change)
        
        return item
    
    @classmethod
    def checkbox(cls, master, label: str, options: List[str], **kwargs) -> 'FormItem':
        """创建复选框组"""
        item = cls(master, label, **kwargs)
        checkbox = Checkbox(item, options=options)
        item.widget = item._setup_widget(checkbox)
        item.vars = checkbox.vars  # 保存变量引用列表
        
        # 为每个复选框变量添加 trace
        for var in item.vars:
            var.trace_add('write', item._notify_change)
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def file_picker(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建文件选择器表单项"""
        # 从 kwargs 中分离出 FilePicker 支持的参数
        picker_kwargs = {
            k: v for k, v in kwargs.items() 
            if k in ['mode', 'filetypes', 'multiple_buttons', 'placeholder']
        }
        
        # 分离出 FormItem 支持的参数
        form_item_kwargs = {
            k: v for k, v in kwargs.items()
            if k in ['required', 'label_width', 'label_anchor', 'layout']
        }
        
        # 创建表单项，只传入 FormItem 支持的参数
        item = cls(master, label, **form_item_kwargs)
        
        # 创建 FilePicker，只传入它支持的参数
        picker = FilePicker(
            item,
            label="",
            **picker_kwargs
        )
        item.widget = item._setup_widget(picker)
        item.var = picker.path_var
        
        # 直接在 FormItem 上添加 set_mode 方法
        def set_mode(mode):
            if hasattr(picker, 'set_mode'):
                picker.set_mode(mode)
        item.set_mode = set_mode
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
    @property
    def value(self) -> Any:
        """获取输入控件的值"""
        if hasattr(self.widget, 'value'):
            return self.widget.value
        return ""
    
    @value.setter
    def value(self, val: Any):
        """设置输入控件的值"""
        if hasattr(self.widget, 'value'):
            self.widget.value = val
    
    def set_label_width(self, width: int):
        """设置标签宽度"""
        self.label.configure(width=width)
        
    def set_label_anchor(self, anchor: Literal["w", "e"]):
        """设置标签对齐方式"""
        self.label.configure(anchor=anchor)
        
    def on_change(self, callback):
        """添加变化事件回调"""
        self._change_callbacks.append(callback)
        return self
        
    def _notify_change(self, *args):
        """通知所有回调"""
        value = self.value
        for callback in self._change_callbacks:
            callback(value)

    def show(self):
        """显示表单项"""
        if not self._visible:
            # 获取当前项在 Form 中的位置
            if self._form and hasattr(self._form, '_items_order'):
                # 优化: 直接用 items() 反向查找太低效了
                # 可以在 Form._add_item 时就记录 name
                current_name = self._name if hasattr(self, '_name') else None
                
                if current_name:
                    # 找到当前项在顺序列表中的位置
                    current_index = self._form._items_order.index(current_name)
                    
                    # 找到下一个应该在它之前的可见项
                    before_widget = None
                    for name in self._form._items_order[current_index + 1:]:
                        item = self._form._items[name]
                        if item._visible:
                            before_widget = item
                            break
                    
                    if before_widget:
                        self.pack(fill=tk.X, pady=2, before=before_widget)
                    else:
                        self.pack(fill=tk.X, pady=2)
                else:
                    self.pack(fill=tk.X, pady=2)
            
            self._visible = True
        
    def hide(self):
        """隐藏表单项"""
        if self._visible:
            self.pack_forget()
            self._visible = False

    @property
    def visible(self) -> bool:
        """获取可见性"""
        return self._visible

    @classmethod
    def text(cls, master, label: str = "", text: str = "", **kwargs) -> 'FormItem':
        """创建文本展示项
        Args:
            master: 父级容器
            label: 标签文本，可选
            text: 显示的文本内容
            **kwargs: 其他参数
        """
        item = cls(master, label, **kwargs)
        text_widget = Text(item, text=text)
        item.widget = item._setup_widget(text_widget)
        
        # 如果没有标签，隐藏标签组件
        if not label:
            item.label.pack_forget()
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
