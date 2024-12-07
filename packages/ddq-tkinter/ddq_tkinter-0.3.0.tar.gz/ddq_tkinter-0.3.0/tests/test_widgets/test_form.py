import pytest
from ddq_widgets import Form

@pytest.fixture
def form(root_window):
    """创建表单实例"""
    form = Form(root_window)
    form.pack()
    root_window.update()
    return form

@pytest.fixture
def mock_messagebox(monkeypatch):
    """模拟消息框，自动返回 ok"""
    def mock_showwarning(title, message):
        return "ok"
    monkeypatch.setattr("tkinter.messagebox.showwarning", mock_showwarning)

def test_initial_state(form):
    """测试初始状态"""
    assert len(form._items) == 0
    assert len(form._items_order) == 0
    assert form._change_callback is None

def test_basic_form_items(form):
    """测试基本表单项的创建"""
    # 创建输入框
    input_item = form.input("name", "姓名:", required=True)
    assert "name" in form._items
    assert input_item.label.cget("text") == "姓名:"
    assert str(input_item.label.cget("foreground")) == "red"  # 必填项为红色

def test_form_values(form):
    """测试表单值的获取和设置"""
    # 创建表单项
    form.input("name", "姓名:")
    form.select("type", "类型:", options=["A", "B"])
    
    # 测试设置值
    test_values = {
        "name": "test",
        "type": "A"
    }
    form.set_values(test_values)
    
    # 验证获取的值
    values = form.get_values()
    assert values["name"] == "test"
    assert values["type"] == "A"

def test_form_section(form):
    """测试表单分区"""
    # 创建分区
    basic_section = form.section("基本信息")
    basic_section.input("name", "姓名:")
    basic_section.input("age", "年龄:")
    
    # 验证分区中的表单项
    assert "基本信息" in form._items
    section_values = basic_section.get_values()
    assert "name" in section_values
    assert "age" in section_values

def test_form_change_event(form):
    """测试表单变化事件"""
    changes = []
    
    # 先创建表单项
    form.input("name", "姓名:")
    
    # 再设置回调
    def on_change(values):
        changes.append(values)
    form.on_change(on_change)
    
    # 修改值
    form._items["name"].value = "test"
    
    # 验证回调被触发
    assert len(changes) == 1
    assert changes[0]["name"] == "test"

def test_form_validation(form):
    """测试表单验证"""
    # 创建必填项
    form.input("name", "姓名:", required=True)
    
    # 确保值为空
    form.set_values({"name": ""})
    
    # 测试空值验证
    values = form.get_values()  # 获取当前值
    assert values["name"] == ""  # 确认值为空
    
    # 设置值后再获取
    form.set_values({"name": "test"})
    values = form.get_values()
    assert values["name"] == "test"  # 确认值已设置

def test_form_visibility(form):
    """测试表单显示/隐藏"""
    # 创建表单项
    form.input("name", "姓名:")
    
    # 测试隐藏
    form.hide()
    form.master.update()
    assert form.winfo_manager() == ""  # 隐藏后没有布局管理器
    
    # 测试显示
    form.show()
    form.master.update()
    assert form.winfo_manager() == "pack"  # 显示后使用pack布局

def test_form_reset(form):
    """测试表单重置"""
    # 创建表单项
    form.input("name", "姓名:")
    form.input("age", "年龄:")
    
    # 设置默认值
    defaults = {
        "name": "default",
        "age": "20"
    }
    form.set_defaults(defaults)
    
    # 修改值
    form.set_values({
        "name": "test",
        "age": "30"
    })
    
    # 重置表单
    form.reset()
    
    # 验证值已重置为默认值
    values = form.get_values()
    assert values["name"] == "default"
    assert values["age"] == "20"


if __name__ == "__main__":
    pytest.main(["-v", __file__]) 