import os
import sys

# 获取项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# 添加项目根目录到系统路径
if project_root not in sys.path:
    sys.path.append(project_root) 