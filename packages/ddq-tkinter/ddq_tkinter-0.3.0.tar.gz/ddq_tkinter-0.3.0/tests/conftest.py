import pytest
import tkinter as tk
from unittest.mock import Mock

@pytest.fixture(scope="session")
def root_window():
    """创建根窗口"""
    try:
        window = tk.Tk()
        window.withdraw()  # 隐藏窗口
        yield window
    finally:
        window.destroy()

@pytest.fixture(autouse=True)
def mock_messagebox(monkeypatch):
    """自动模拟所有消息框"""
    mock = Mock()
    mock.showwarning = Mock(return_value='ok')
    mock.showerror = Mock(return_value='ok')
    mock.showinfo = Mock(return_value='ok')
    mock.askyesno = Mock(return_value=True)
    monkeypatch.setattr('tkinter.messagebox', mock) 