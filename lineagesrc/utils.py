import yaml

import warnings  
from functools import wraps  
def deprecated(func):  
    """This is a decorator to mark functions as deprecated."""  
    @wraps(func)  
    def wrapped_function(*args, **kwargs):  
        warnings.warn(  
            f"{func.__name__} is deprecated and may be removed in future versions.",  
            category=DeprecationWarning,  
            stacklevel=2  
        )  
        return func(*args, **kwargs)  
    
    return wrapped_function 

class DictToObject:  
    def __init__(self, dictionary):  
        for key, value in dictionary.items():  
            if isinstance(value, dict):  
                # 递归地把子字典转换为对象  
                setattr(self, key, DictToObject(value))  
            else:  
                setattr(self, key, value)  
    
    def __getitem__(self, item):  
        return getattr(self, item)  

# 读取 YAML 文件并使用 DictToObject  
def read_yaml_as_object(file_path):  
    with open(file_path, 'r') as file:  
        try:  
            config_dict = yaml.safe_load(file)  
            return DictToObject(config_dict)  
        except yaml.YAMLError as exc:  
            print(f"Error reading YAML file: {exc}")  

def read_yaml_file(file_path):  
    with open(file_path, 'r') as file:  
        try:  
            config = yaml.safe_load(file)  
            return config  
        except yaml.YAMLError as exc:  
            print(f"Error reading YAML file: {exc}")  


if __name__ == "__main__":
        print("config_reader")
        # test1
        # filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
        # config = read_yaml_file(filepath)
        # print(config)
        
        
        # test2
        # filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
        # config = read_yaml_as_object(filepath)
        # print(config)