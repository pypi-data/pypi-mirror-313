import pytest
from ddq_widgets import Card
import tkinter as tk

@pytest.fixture
def card(root_window):
    """创建卡片实例"""
    card = Card(root_window, title="测试卡片")
    card.pack()
    root_window.update()
    return card

def test_card_initialization(card):
    """测试卡片初始化"""
    assert isinstance(card, Card)
    assert card.cget("text") == "测试卡片"  # 验证标题
    assert isinstance(card.content, tk.Widget)  # 验证内容区域存在

def test_card_content_widgets(card):
    """测试向内容区域添加组件"""
    # 添加一个标签
    label = tk.Label(card.content, text="测试内容")
    label.pack()
    
    # 验证标签被添加到内容区域
    assert label in card.content.winfo_children()
    assert label.master == card.content

def test_card_layout(card):
    """测试卡片布局"""
    # 验证内容区域的布局
    pack_info = card.content.pack_info()
    assert pack_info["fill"] == "both"
    assert pack_info["expand"]

def test_card_title_update(card):
    """测试更新标题"""
    new_title = "新标题"
    card.configure(text=new_title)
    assert card.cget("text") == new_title

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 