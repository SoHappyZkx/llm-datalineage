import os
import json
from . import normalize
import pandas as pd

'''
检查是否为空的，无字符的，没有key的内容
'''
def check_has_json(str_):
    if pd.isna(str_):
        return False
    if len(str_) == 0:
        return False
    if str_ == "\{\}":
        return False
    return True

def get_sql_format(sql_code_str,sql_name,output_dir):
    new_sql = normalize.format_sql(sql_code_str)
    with open(os.path.join(output_dir,sql_name), 'w', encoding='utf-8') as f:  
        f.writelines(new_sql)
 
def format_sql_line(all_str,sql_result):
    rest_str = all_str.replace(sql_result,'')
    new_sql_result = sql_result.replace('\\"','')
    new_sql_result = new_sql_result.replace("\\\\n","\n")
    new_sql_result = new_sql_result.replace("\\\\t","\t")
    json_res = json.loads(rest_str)
    json_res['sql'] = new_sql_result
    return json_res
       
'''
部分场景sql代码里也存在""双引号，导致json解析出错，所以需要找到sql代码的位置
'''
def get_sql_str_from_column(all_str):
    '''
    可能存在最后一个不是sql字段，是别的字段。需要处理一下。
    '''
    #找到第一个带有 \"sql\":\" 这个字符串的的位置，然后找到最后出现 \" 的位置
    start = all_str.find('\"sql\":\"')
    end = all_str.rfind('\"parentDsName\":')
    
    if start>0: #存在 "sql":"
        if end >0 and end > start:
            sql_str = all_str[start+7:end-2]
        else:
            end = all_str.rfind('\"')
            sql_str = all_str[start+7:end]
    else:
        sql_str = ''
    return sql_str
    

def test1():
    file1 = "F:\\GITClone\\CMCCtest\\dateline\\data\\dataos自助相关程序配置信息 (1)(1).xlsx"
    file2 = "F:\\GITClone\\CMCCtest\\dateline\\data\\自助数据字典(2).xlsx"
    test1 = "F:\\GITClone\\CMCCtest\\dateline\\test\\7.json"
    test1_trans = "F:\\GITClone\\CMCCtest\\dateline\\test\\7trans.sql"
    #df1 = pd.read_excel(file1)
    #df2 = pd.read_excel(file2)
    with open(test1, 'r', encoding='utf-8') as file:  
        data = json.load(file)  
    print(data)
    new_sql = normalize.format_sql(data['sql'])
    print(new_sql)
    with open(test1_trans, 'w', encoding='utf-8') as f:  
        f.writelines(new_sql)
