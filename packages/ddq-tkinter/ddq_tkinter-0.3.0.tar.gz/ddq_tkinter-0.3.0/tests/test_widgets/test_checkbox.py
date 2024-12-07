import pytest
from ddq_widgets import Checkbox

@pytest.fixture
def checkbox(root_window):
    """创建复选框实例"""
    options = ["选项1", "选项2", "选项3"]
    checkbox = Checkbox(root_window, options=options)
    checkbox.pack()
    root_window.update()
    return checkbox

def test_checkbox_initialization(checkbox):
    """测试复选框初始化"""
    assert isinstance(checkbox, Checkbox)
    assert len(checkbox.vars) == 3  # 验证选项数量
    assert not checkbox.value  # 默认无选中项

def test_checkbox_default_values(root_window):
    """测试默认值设置"""
    options = ["选项1", "选项2", "选项3"]
    checkbox = Checkbox(
        root_window,
        options=options,
        default_values=["选项1", "选项3"]
    )
    assert checkbox.value == ["选项1", "选项3"]

def test_checkbox_layout(root_window):
    """测试布局方式"""
    options = ["选项1", "选项2"]
    # 测试水平布局
    h_checkbox = Checkbox(root_window, options=options, layout="horizontal")
    # 测试垂直布局
    v_checkbox = Checkbox(root_window, options=options, layout="vertical")

def test_checkbox_value_property(checkbox):
    """测试值属性的获取和设置"""
    # 设置选中项
    checkbox.value = ["选项1", "选项3"]
    assert checkbox.value == ["选项1", "选项3"]

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 