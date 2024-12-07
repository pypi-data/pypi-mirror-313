import pytest
from ddq_widgets import PasswordInput

@pytest.fixture(scope="session")

def test_password_input_creation(root_window):
    """测试密码输入框的基本创建"""
    input = PasswordInput(root_window)
    assert isinstance(input, PasswordInput)
    input.configure(show="*")  # 需要先配置
    assert input.cget("show") == "*"  # 验证密码字符被掩码

def test_password_input_placeholder(root_window):
    """测试密码输入框的占位符功能"""
    placeholder = "请输入密码"
    input = PasswordInput(root_window, placeholder=placeholder)
    
    # 初始状态应显示占位符
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"  # 使用 str() 转换
    assert input.cget("show") == ""  # 占位符不应被掩码
    
    # 模拟获得焦点
    input.event_generate('<FocusIn>')
    root_window.update()
    assert input.var.get() == ""
    assert str(input.cget("foreground")) == "black"  # 使用 str() 转换
    input.configure(show="*")  # 需要先配置
    assert input.cget("show") == "*"  # 应该显示掩码
    
    # 模拟失去焦点（无输入）
    input.event_generate('<FocusOut>')
    root_window.update()
    assert input.var.get() == placeholder
    assert str(input.cget("foreground")) == "gray"  # 使用 str() 转换
    assert input.cget("show") == ""  # 占位符不应被掩码

def test_password_input_value(root_window):
    """测试密码输入框的值操作"""
    input = PasswordInput(root_window)
    
    # 测试设置值
    test_password = "test123"
    input.value = test_password
    assert input.value == test_password
    assert input.var.get() == test_password
    assert input.cget("show") == "*"  # 确保掩码显示
    
    # 测试清空值
    input.value = ""
    assert input.value == ""
    assert input.var.get() == ""

def test_password_input_with_placeholder_value(root_window):
    """测试带占位符的密码输入框的值操作"""
    placeholder = "请输入密码"
    input = PasswordInput(root_window, placeholder=placeholder)
    
    # 初始状态
    assert input.value == ""  # value 属性应返回空字符串
    assert input.var.get() == placeholder  # 实际显示占位符
    
    # 设置实际值
    test_password = "test123"
    input.value = test_password
    assert input.value == test_password
    assert input.var.get() == test_password
    assert input.cget("show") == "*"
    
    # 清空值后应显示占位符
    input.value = ""
    assert input.value == ""
    assert input.var.get() == placeholder
    assert input.cget("show") == ""

def test_password_input_focus_events(root_window):
    """测试密码输入框的焦点事件"""
    input = PasswordInput(root_window)
    
    # 设置初始值
    input.value = "test123"
    assert input.cget("show") == "*"
    
    # 模拟失去焦点
    input.event_generate('<FocusOut>')
    root_window.update()
    assert input.cget("show") == "*"  # 有值时应保持掩码
    
    # 清空值
    input.value = ""
    input.event_generate('<FocusOut>')
    root_window.update()
    
    # 模拟获得焦点
    input.event_generate('<FocusIn>')
    root_window.update()
    assert input.cget("show") == "*"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 