import os
import sys
dirpath = os.path.dirname(os.path.abspath(__file__))  
root_dir = os.path.dirname(dirpath) 

sys.path.append(dirpath)
sys.path.append(root_dir)
sys.path.append(os.path.dirname(root_dir))
import llmodel.llmapi as llmapi


print("dd")