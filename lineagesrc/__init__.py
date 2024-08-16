# 在 your_script.py 使用相对导入，假设上层目录为一个包结构  
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/lineagesrc")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
