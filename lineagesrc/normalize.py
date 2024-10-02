import re
import json
import sqlparse
from utils import deprecated
'''
可以剔除各种sql代码中的\n， \t等等错误问题
'''
def is_colume_name(s):  
    """  
    检查字符串是否只包含英文字符、数字和特殊字符'.'  
    """  
    # 使用正则表达式匹配字符串  
    pattern = r'^[a-zA-Z0-9.]+$'  
    return bool(re.match(pattern, s))  


def is_comment(s):  
    """  
    判断字符串是否是注释。  
    注释需满足：  
    1. 以 -- 或 # 开头  
    2. 字符串中可能包含中文  
    """  
    # 检查是否以 -- 或 # 开头  
    if not (s.strip().startswith('--') or s.strip().startswith('#')):  
        return False  

    # 使用正则表达式检查是否存在中文字符  
    contains_chinese = bool(re.search(r'[\u4e00-\u9fff]', s))  
    
    return contains_chinese  

def format_sql(sql_code):
    '''
    step1里的核心方法。去除多余制表符，匹配缩进
    '''
    # 替换 \\n 为换行符
    formatted_sql = sql_code.replace('\\n', '\n').replace('\\t', '    ')
    
    # 进一步优化SQL格式
    # 1. 去除多余的空白字符
    optimized_sql = re.sub(r'[^\S\n]+', ' ', formatted_sql) #匹配一个或者多个制表符，空白符等，替换为一个空格
    formatted_sql = re.sub(r'\n\s*\n', '\n', formatted_sql)  # 匹配两个换行符中的所有制表符等都替换为一个换行符
    formatted_sql = re.sub(r'\n\s+', '\n', formatted_sql) #
    formatted_sql = re.sub(r'([^\n])\n([^\n])', r'\1\n    \2', formatted_sql)  # []是一个捕获组，匹配或有非换行符的字符，匹配后，在保留原有的缩进的情况下爱再添加缩进。
    formatted_sql = re.sub(r'\n    (from|left join|where|and|or|group by|order by)', r'\n\1', formatted_sql)  # 减少关键字前的缩进

    # 加入正则匹配，处理函数结束和字段名中间没有空格的问题
    #formatted_sql = re.sub(r'(\)\s*)([a-zA-Z_]\w*)' , r') \2', formatted_sql)  #会导致一些 )\n 的地方，也匹配到，把\n 用 空格替换了。
    #formatted_sql = re.sub(r'\)(?=[a-zA-Z_](?![nt]))', r') ', formatted_sql) # 加了与检查
    formatted_sql = re.sub(r'\)(?=[a-zA-Z_]\w*)', r') ', formatted_sql) #或者严格一些，直接匹配)后必须是变量名，否则不加空格
    #formatted_sql = re.sub(r'\)(?![\s\\])', r') ', formatted_sql) # 加了反向检查，确保匹配的后面不是任何空白和转义符
    # 2. 在每个SQL关键字前添加换行
    # keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN']
    # for keyword in keywords:
    #     formatted_sql = re.sub(r'\b' + keyword + r'\b', '\n' + keyword, formatted_sql)
    

    #20240810 发现会出现一些奇怪的优化，取消了fomrat优化
    #formatted_sql_trans = sqlparse.format(formatted_sql, reindent=True, keyword_case='upper')

    # 3.组织in内的元素出现换行
    # IN $[^)]+$ 匹配 'IN (' 后跟任意非 ')' 字符，直到 ')' 结束
    # re.DOTALL 使得 '.' 特殊字符可以匹配任何字符包括换行符
    formatted_sql_trans = re.sub(r'IN $([^)]+)$', lambda m: 'IN (' + re.sub(r'\s+', '', m.group(1)) + ')', formatted_sql, flags=re.DOTALL)
    
    return formatted_sql_trans

def find_comment(sql_line_str):
    # 定义匹配注释的正则表达式模式（-- 注释或 # 注释）  
    pattern = r"(--|#)\s*(.*)"  
    
    # 定义匹配字段名的正则表达式模式  
    field_pattern = r"(\w+)\s*"  
    
    matches = re.finditer(pattern, sql_line_str)  
    
    result = []  
    for match in matches:  
        # 获取注释  
        comment = match.group(2)  
        
        # 获取注释前的代码  
        code = sql_line_str[:match.start()]  
        
        # 找到最近的字段名  
        field_match = re.search(field_pattern, code[::-1])  # 反转查找  
        if field_match:  
            field = field_match.group(1)[::-1]  # 反转回来  
            result.append((field, comment))  
    
    return result  




@deprecated
def beautiful_sql(sql_code):
    '''
    解决阶梯型 空格的问题
    SELECT a.phone_no,  
        round(sum(CASE  
                        WHEN b.PERIOD='00' THEN b.TOTAL_FLOW  
                    END)/1024,  
                2) gprs_00,  
                round(sum(CASE  
                            WHEN b.PERIOD='01' THEN b.TOTAL_FLOW  
                        END)/1024,  
                    2) gprs_01,  
                    round(sum(CASE  
                                WHEN b.PERIOD='02' THEN b.TOTAL_FLOW  
                            END)/1024,  
                        2) gprs_02,  
    '''
    pattern = r'\n\s+'  
    replaced_sql = re.sub(pattern, ' ', sql_code)  
    formatted_sql = sqlparse.format(replaced_sql, reindent=True, keyword_case='upper')  
    return formatted_sql  

def convert_to_dict(json_str):
    try:
        # 将JSON字符串转换为字典
        data_dict = json.loads(json_str)
        return data_dict
    except json.JSONDecodeError as e:
        # 如果JSON解析出错，输出错误信息
        print(f"Error decoding JSON: {e}")
        return None
    

def read_sql_file(filename):
    #从文件读取字符串
    with open(filename, 'r', encoding='utf-8') as file:
        str_ = file.read()
    new_dict = convert_to_dict(str_)
    return new_dict 

#获取当前目录的绝对路径


if __name__ == "__main__" :
    print("")