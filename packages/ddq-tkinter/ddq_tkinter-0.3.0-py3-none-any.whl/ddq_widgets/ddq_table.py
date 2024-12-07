import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from .ddq_button import Button  # 导入自定义按钮组件
import os
import json

class Table(ttk.LabelFrame):
    """高级表格组件"""
    def __init__(self, parent, title, columns, buttons=None, height=10, padding=5, expand=True):
        """
        初始化高级表格组件
        Args:
            parent: 父容器
            title: 标题
            columns: 列配置列表 [{'id': 'col1', 'text': '列1', 'width': 100}]
            buttons: 按钮配置列表 [{'text': '按钮1', 'command': callback}]
            height: 表格高度
            padding: 内边距
            expand: 是否自动扩展
        """
        super().__init__(parent, text=title)
        
        # 自动布局
        if expand:
            self.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)
        
        # 创建主容器
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 如果有按钮配置,创建按钮框架 - 移到最上面
        if buttons:
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(fill="x", pady=5)  # 移除 padx
            for i, btn in enumerate(buttons):
                Button(  # 使用 Button 替换 ttk.Button
                    btn_frame,
                    text=btn['text'],
                    command=btn['command']
                ).pack(side=tk.LEFT, padx=(0, 5))  # 只在右边添加间距
        
        # 创建表格容器
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True)
        
        # 添加序号列到列配置中
        all_columns = ['#'] + [col['id'] for col in columns]
        
        # 创建树形视图
        self.tree = ttk.Treeview(
            table_frame,
            columns=all_columns,
            show='headings',
            height=height
        )
        
        # 配置序号列
        self.tree.heading('#', text='#')
        self.tree.column('#', width=35, anchor='center', stretch=False)  # 序号列保持固定宽度
        
        # 配置其他列 - 先用默认宽度
        for col in columns:
            self.tree.heading(
                col['id'], 
                text=col['text'],
                command=lambda c=col['id']: self.sort_by_column(c)
            )
            self.tree.column(col['id'], width=col.get('width', 100), stretch=True)  # 允许拉伸
            
        # 保存列配置以便后续使用
        self.columns = columns
        
        # 初始化排序状态
        self._sort_states = {}  # 记录每列的排序状态
        
        # 添加直滚动条
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # 添加水平滚动条
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        
        # 使用grid布局
        self.tree.grid(row=0, column=0, sticky="nsew")  # 表格占据主要区域
        vsb.grid(row=0, column=1, sticky="ns")          # 垂直滚动条靠右
        hsb.grid(row=1, column=0, sticky="ew")          # 水平滚动条在底部
        
        # 配置grid权重
        table_frame.grid_columnconfigure(0, weight=1)   # 表格列可以扩展
        table_frame.grid_rowconfigure(0, weight=1)      # 表格行可以扩展
        
    def adjust_columns_width(self):
        """调整所有列的宽度以适应内容"""
        import tkinter.font as tkfont
        
        # 使用默认字体
        font = tkfont.Font(family="TkDefaultFont")
        
        # 计算基础padding - 使用字体大小作为基准
        char_width = font.measure('0')  # 使用数字0的宽度作为基准
        base_padding = char_width * 2   # 左右各留一个字符的空间
        
        # 获取表格总宽度
        table_width = self.tree.winfo_width()
        if table_width <= 1:  # 如果表格还未完全渲染
            self.tree.update_idletasks()  # 更新布局
            table_width = self.tree.winfo_width()
        
        # 序号列固定宽度 - 使用动态计算
        fixed_width = font.measure('000') + base_padding  # 三位数字宽度加padding
        available_width = table_width - fixed_width
        
        # 计算每列所需的最小宽度
        min_widths = {}
        total_min_width = 0
        
        for col in self.columns:
            # 获取列标题宽度
            header_text = self.tree.heading(col['id'])['text'].rstrip(' ↑↓')
            min_width = font.measure(header_text) + base_padding
            
            # 检查所有单元格内容宽度
            for item in self.tree.get_children():
                cell_value = str(self.tree.set(item, col['id']))
                cell_width = font.measure(cell_value) + base_padding
                min_width = max(min_width, cell_width)
            
            min_widths[col['id']] = min_width
            total_min_width += min_width
        
        # 设置列宽
        if available_width >= total_min_width:
            # 如果有额外空间，按比例分配
            extra_space = available_width - total_min_width
            for col in self.columns:
                ratio = min_widths[col['id']] / total_min_width
                width = min_widths[col['id']] + int(extra_space * ratio)
                self.tree.column(col['id'], width=width, minwidth=min_widths[col['id']])
        else:
            # 如果空间不足，使用最小宽度
            for col in self.columns:
                self.tree.column(col['id'], width=min_widths[col['id']], minwidth=min_widths[col['id']])
    
    def insert_record(self, values, index='end'):
        """插入记录
        Args:
            values: 记录值
            index: 插入位置，默认为'end'表示添加到末尾
        """
        # 在值的最前面添加序号
        row_number = len(self.tree.get_children()) + 1
        all_values = [row_number] + list(values)
        self.tree.insert('', index, values=all_values)
        
        # 插入后调整列宽
        self.adjust_columns_width()
        
    def clear_records(self):
        """清空所有记录"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def get_records(self):
        """获取所有记录(不包含序号列)"""
        return [self.tree.item(item)['values'][1:]  # 去掉序号列
                for item in self.tree.get_children()]
        
    def sort_by_column(self, column):
        """按列排序
        Args:
            column: 列ID
        """
        # 获取当前排序状态
        if column not in self._sort_states:
            self._sort_states[column] = 'asc'  # 默认升序
        else:
            # 切换排序方向
            self._sort_states[column] = 'desc' if self._sort_states[column] == 'asc' else 'asc'
            
        # 获取所有项目
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        
        # 根据数据类型进行排序
        try:
            # 尝试数字排序
            items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else x[0],
                      reverse=self._sort_states[column] == 'desc')
        except ValueError:
            # 如果失败则按字符串排序
            items.sort(key=lambda x: x[0],
                      reverse=self._sort_states[column] == 'desc')
        
        # 重新排列项目
        for index, (_, item) in enumerate(items):
            # 获取当前值
            values = list(self.tree.item(item)['values'])
            # 更新序号
            values[0] = index + 1
            # 移动项目并更新值
            self.tree.move(item, '', index)
            self.tree.item(item, values=values)
            
        # 更新列标题显示排序方向
        for col in self.tree['columns']:
            # 移除所有列的排序指示器
            self.tree.heading(col, text=self.tree.heading(col)['text'].rstrip(' ↑↓'))
        
        # 为当前排序列添加排序指示器
        current_text = self.tree.heading(column)['text']
        sort_indicator = ' ↑' if self._sort_states[column] == 'asc' else ' ↓'
        self.tree.heading(column, text=current_text.rstrip(' ↑↓') + sort_indicator)
        
    def export_data(self, file_path=None):
        """导出表格数据
        Args:
            file_path: 文件路径,如果为None则弹出保存对话框
        Returns:
            bool: 是否��出成功
        """
        try:
            # 如果没有指定文件路径,弹出保存对话框
            if not file_path:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[
                        ("CSV files", "*.csv"),
                        ("JSON files", "*.json"),
                        ("All files", "*.*")
                    ]
                )
            if not file_path:
                return False
            
            # 获取数据
            headers = [self.tree.heading(col)['text'].rstrip(' ↑↓') 
                      for col in self.tree['columns']]
            headers = headers[1:]  # 去掉序号列
            records = self.get_records()
            
            # 根据文件扩展名选择导出格式
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.json':
                # 导出为JSON
                data = [dict(zip(headers, record)) for record in records]
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                # 默认导出为CSV
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    import csv
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(records)
            
            return True
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")
            return False