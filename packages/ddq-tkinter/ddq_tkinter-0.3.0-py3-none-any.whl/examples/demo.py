import tkinter as tk
from tkinter import ttk

from ddq_widgets import Form
from ddq_widgets.ddq_text import Text
from ddq_widgets.ddq_card import Card
from ddq_widgets.ddq_button_group import ButtonGroup
from ddq_widgets.ddq_split_layout import SplitLayout
from tkinter import messagebox
from ddq_widgets.ddq_toast import Toast
from ddq_widgets.ddq_scrollable import ScrollableContainer

class FormItemDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("FormItem 组件示例")
        self.root.geometry("1000x600")
        
        # 调整 SplitLayout 配置
        self.split = SplitLayout(root)
        
        # 创建左侧容器
        left_container = ttk.Frame(self.split.left)
        left_container.pack(fill=tk.BOTH, expand=True)
        
        # 添加按钮组到左侧容器顶部
        self.button_group = ButtonGroup(left_container, align="left")
        self.button_group.add_new("全部禁用", command=self.disable_all)
        self.button_group.add_new("全部启用", command=self.enable_all)
        self.button_group.add_new("查看修改", command=self.show_modified)
        self.button_group.add_new("提交", command=self.handle_submit)
        self.button_group.add_new("重置", command=self.handle_reset)
        
        # 创建滚动容器，放在按钮组下方
        self.left_scroll = ScrollableContainer(left_container)
        
        # 创建表单容器，放在滚动容器中
        self.form = Form(self.left_scroll.content)
        
        # 创建基本信息分区
        self.basic_section = self.form.section("基本信息")
        
        # 1. 文本输入框（必填）
        self.input_item = self.basic_section.input(
            "username",
            "用户名:",
            required=True
        )
        
        # 2. 密码输入框（必填）
        self.password_item = self.basic_section.password(
            "password",
            "密码:",
            required=True
        )
        
        # 3. 下拉选择框（必填）
        self.select_item = self.basic_section.select(
            "type",
            "类型:",
            options=["普通用户", "管理员", "游客"],
            required=True
        )
        
        # 4. 单选框组
        self.radio_item = self.basic_section.radio(
            "gender",
            "性别:",
            options=["男", "女"]
        )
        
        # 创建详细信息分区
        self.detail_section = self.form.section("详细信息")
        
        # 5. 复选框组
        self.checkbox_item = self.detail_section.checkbox(
            "hobbies",
            "爱好:",
            options=["阅读", "音乐", "运动"]
        )
        
        # 6. 多行文本框
        self.textarea_item = self.detail_section.textarea(
            "description",
            "描述:",
            height=3
        )
        
        # 7. 文件选择器 - 单个文件
        self.file_item = self.detail_section.file_picker(
            "file",
            "选择文件:",
            mode="file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        # 8. 文件选择器 - 文件夹
        self.folder_item = self.detail_section.file_picker(
            "folder",
            "选择目录:",
            mode="folder"
        )
        
        # 9. 文件选择器 - 多按钮模式
        self.multi_item = self.detail_section.file_picker(
            "multi",
            "多选模式:",
            multiple_buttons=True
        )
        
            # 设置默认值
        self.form.set_defaults({
            "username": "admin",
            "password": "",
            "type": "普通用户",
            "gender": "男",
            "hobbies": ["阅读"],
            "description": "这是一段默认描述",
            "file": "",
            "folder": "",
            "multi": ""
        })

        # 初始化完成后设置标志
        self.form._initializing = False
        self.basic_section._initializing = False
        self.detail_section._initializing = False
        
        self.toast = Toast(root)  # 创建Toast实例
        
        # 创建右侧实时数据显示区域
        self.create_data_display()
        
        # 绑定表单变化事件
        self.form.on_change(self.on_form_change)
        
        # 初始化完成后设置标志
        self.form._initializing = False
        self.basic_section._initializing = False
        self.detail_section._initializing = False
        
    def create_data_display(self):
        """创建右侧实时数据显示区域"""
        # 使用 Card 组件包装数据显示区域
        self.display_card = Card(self.split.right, title="实时数据")
        
        # 创建可滚动容器
        self.scroll_container = ScrollableContainer(self.display_card.content)
        
        # 在滚动容器中创建文本
        self.data_display = Text(self.scroll_container.content)
    def on_form_change(self, values):
        """处理表单变化事件"""
        # 处理类型选择联动
        user_type = values.get("type")
        if user_type == "游客":
            self.detail_section.pack_forget()  # 隐藏详细信息分区
        else:
            self.detail_section.pack()  # 显示详细信息分区

        # 更新数据显示
        display_text = []
        for key, value in values.items():
            if isinstance(value, list):
                value = f"[{', '.join(map(str, value))}]"
            display_text.append(f"{key}：{value}")
        
        formatted_text = "\n".join(display_text)
        self.data_display.set_text(formatted_text)

    def disable_all(self):
        """禁用所有表单项"""
        self.form.set_state('disabled')
        self.toast.show("所有表单项已禁用")  # 显示提示
        
    def enable_all(self):
        """启用所有表单项"""
        self.form.set_state('normal')
        self.toast.show("所有表单项已启用")  # 显示提示

    def show_modified(self):
        """使用弹窗显示已修改的表单项"""
        modified_items = self.form.is_modified()
        
        # 构建显示文本
        display_text = ""
        has_modified = False
        
        for name, is_modified in modified_items.items():
            if is_modified:
                has_modified = True
                current_value = self.form.get_values()[name]
                display_text += f"• {name}:当前值: {current_value}\n"
        
        if not has_modified:
            messagebox.showinfo("表单状态", "没有表单项被修改")
        else:
            messagebox.showinfo("已修改的表单项", display_text)

    def handle_submit(self):
        """处理表单提交"""
        if self.form.submit():  # 如果验证通过
            # 获取表单数据
            data = self.form.get_values()
            # 这里可以处理数据，比如发送到服务器
            print("表单数据：", data)
            # 显示成功提示
            self.toast.show("提交成功")

    def handle_reset(self):
        """处理表单重置"""
        self.form.reset()  # 重置表单到默认值
        self.toast.show("表单已重置")  # 显示提示

def main():
    root = tk.Tk()
    app = FormItemDemo(root)
    # 初始时启用表单按钮应该是禁用状态
    root.mainloop()

if __name__ == "__main__":
    main()