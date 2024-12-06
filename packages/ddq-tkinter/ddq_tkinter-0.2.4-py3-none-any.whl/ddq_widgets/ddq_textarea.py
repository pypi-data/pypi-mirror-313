import tkinter as tk
from tkinter import ttk

class Textarea(ttk.Frame):
    """自适应文本域组件
    
    特性：
    1. 自动适应父容器大小
    2. 内置滚动条
    3. 支持只读/禁用状态
    4. 支持自动换行
    5. 支持最大行数限制
    """
    
    def __init__(
        self,
        master,
        height: int = 10,           
        max_lines: int = 1000,      
        wrap: str = tk.WORD,        
        readonly: bool = False,
        placeholder: str = None,     # 添加 placeholder 参数
        **kwargs
    ):
        super().__init__(master)
        
        # 保存 placeholder
        self._placeholder = placeholder
        
        # 创建文本框和滚动条
        self.text = tk.Text(
            self,
            height=height,
            wrap=wrap,
            **kwargs
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.text.yview
        )
        
        # 关联文本框和滚动条
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始化 placeholder
        if placeholder:
            self.text.insert('1.0', placeholder)
            self.text.configure(foreground='gray')
            
            # 绑定焦点事件
            self.text.bind('<FocusIn>', self._on_focus_in)
            self.text.bind('<FocusOut>', self._on_focus_out)
        
        # 保存配置
        self.max_lines = max_lines
        self._readonly = readonly
        
        # 设置初始状态
        if readonly:
            self.set_readonly(True)
            
    def _on_focus_in(self, event):
        """获得焦点时的处理"""
        if self.text.get('1.0', 'end-1c') == self._placeholder:
            self.text.delete('1.0', 'end')
            self.text.configure(foreground='black')
            
    def _on_focus_out(self, event):
        """失去焦点时的处理"""
        if not self.text.get('1.0', 'end-1c').strip():
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', self._placeholder)
            self.text.configure(foreground='gray')
            
    def get_text(self) -> str:
        """获取文本内容"""
        return self.text.get("1.0", "end-1c")
        
    def set_text(self, content: str):
        """设置文本内容"""
        # 暂时启用文本框以便设置内容
        current_state = self.text.cget('state')
        self.text.configure(state='normal')
        
        # 设置内容
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self._check_max_lines()
        
        # 恢复原来的状态
        self.text.configure(state=current_state)
        
    def append_text(self, content: str):
        """追加文本内容"""
        self.text.insert(tk.END, content)
        self._check_max_lines()
        
    def clear(self):
        """清空文本内容"""
        self.text.delete("1.0", tk.END)
        
    def set_readonly(self, readonly: bool = True):
        """设置只读状态"""
        self._readonly = readonly
        state = 'disabled' if readonly else 'normal'
        self.text.configure(state=state)
        
    def set_disabled(self, disabled: bool = True):
        """设置禁用状态"""
        state = 'disabled' if disabled else 'normal'
        self.text.configure(state=state)
        
    def _check_max_lines(self):
        """检查并限制最大行数"""
        if self.max_lines <= 0:
            return
            
        # 获取当前行数
        num_lines = int(self.text.index('end-1c').split('.')[0])
        
        # 如果超过最大行数，删除前面的行
        if num_lines > self.max_lines:
            # 删除前面一半的行数
            lines_to_delete = num_lines - self.max_lines
            self.text.delete("1.0", f"{lines_to_delete + 1}.0")
            
    @property
    def value(self) -> str:
        """获取值(用于表单)"""
        current = self.text.get('1.0', 'end-1c')
        # 如果是 placeholder，返回空值
        if current == self._placeholder:
            return ""
        return current
        
    @value.setter
    def value(self, content: str):
        """设置值(用于表单)"""
        # 暂时启用文本框以便设置内容
        current_state = self.text.cget('state')
        self.text.configure(state='normal')
        
        # 设置内容
        self.text.delete('1.0', 'end')
        if not content and self._placeholder:
            self.text.insert('1.0', self._placeholder)
            self.text.configure(foreground='gray')
        else:
            self.text.insert('1.0', content or "")
            self.text.configure(foreground='black')
        
        # 检查最大行数
        self._check_max_lines()
        
        # 恢复原来的状态
        self.text.configure(state=current_state) 