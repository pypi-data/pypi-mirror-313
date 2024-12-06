import tkinter as tk
from tkinter import messagebox, simpledialog
import json

from ddq_widgets import Form, Card, SplitLayout, ButtonGroup, Text, FilePicker

class FormDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Form 组件全面功能测试")
        self.root.geometry("1200x800")
        
        # 创建左右布局容器
        self.split = SplitLayout(root, left_width=500)
        
        # 创建主表单，测试多列布局
        self.form = Form(self.split.left, columns=2, use_card=True, title="综合表单测试")
        
        # 基本信息分区
        self.basic_section = self.form.section("基本信息", columns=2)
        self.basic_section.input("username", "用户名:")
        self.basic_section.password("password", "密码:")
        self.basic_section.select("type", "类型:", options=["普通用户", "管理员", "游客"])
        
        # 个人信息分区
        self.personal_section = self.form.section("个人信息")
        self.personal_section.radio("gender", "性别:", options=["男", "女", "其他"])
        self.personal_section.checkbox("hobby", "爱好:", options=["阅读", "音乐", "运动", "旅行"])
        
        # 文件信息分区
        self.file_section = self.form.section("文件信息")
        self.file_section.file_picker(
            "avatar", 
            "头像:", 
            mode="file", 
            filetypes=[("图片文件", "*.png;*.jpg"), ("所有文件", "*.*")],
            placeholder="请选择头像"
        )
        
        # 详细信息分区
        self.detail_section = self.form.section("详细信息")
        self.detail_section.textarea("description", "个人简介:", height=5)
        
        # 右侧结果展示区
        self.result_card = Card(
            self.split.right, 
            title="实时表单数据",
            expand=True
        )
        
        # 结果展示文本
        self.result_text = Text(
            self.result_card.content,
            wraplength=500,
            justify=tk.LEFT
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 功能按钮区
        self.button_group = ButtonGroup(
            self.split.right, 
            direction="horizontal"
        )
        
        # 添加功能按钮
        buttons = [
            ("重置", self._reset_form),
            ("保存", self._save_form),
            ("验证", self._validate_form)
        ]
        
        for text, command in buttons:
            self.button_group.add_new(text, command=command)
        
        # 设置初始默认值
        initial_defaults = {
            "username": "test_user",
            "type": "普通用户",
            "gender": "男",
            "hobby": [True, False, True, False],
            "description": "这是一个测试用户的默认描述"
        }
        
        # 先设置变化回调
        self.form.on_change(self._update_result_display)
        
        # 再设置默认值
        self.form.set_defaults(initial_defaults)
        
        # 初始化显示
        self._update_result_display(initial_defaults)
        
    def _update_result_display(self, values):
        """实时更新结果展示"""
        print("Entering _update_result_display...")
        try:
            # 直接使用传入的 values，不要重复触发通知
            print(f"Current form values: {values}")
            
            # 格式化展示
            display_text = "🔍 实时表单数据:\n\n"
            display_text += json.dumps(values, ensure_ascii=False, indent=2)
            
            # 添加额外信息
            modified = self.form.is_modified()
            modified_items = [k for k, v in modified.items() if v]
            
            display_text += f"\n\n✏️ 已修改项目: {modified_items}"
            
            print(f"Updated display text: {display_text}")
            
            # 更新显示
            self.result_text.set_text(display_text)
            self.root.update_idletasks()
            
            print("Interface refreshed.")
            
        except Exception as e:
            print(f"Error in _update_result_display: {str(e)}")
            self.result_text.set_text(f"更新出错: {str(e)}")
    
    def _reset_form(self):
        """重置表单"""
        self.form.reset()
    
    def _save_form(self):
        """保存表单"""
        values = self.form.get_values()
    
    def _validate_form(self):
        """表单验证"""
        values = self.form.get_values()
        errors = []
        
        if not values['username']:
            errors.append("用户名不能为空")
        
        if len(values['password']) < 6:
            errors.append("密码长度必须大于6位")
        
        if not values['hobby'] or not any(values['hobby']):
            errors.append("至少选择一个爱好")
        
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
        else:
            messagebox.showinfo("验证通过", "所有验证通过")

def main():
    root = tk.Tk()
    app = FormDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()