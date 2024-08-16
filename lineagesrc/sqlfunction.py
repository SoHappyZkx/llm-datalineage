import re 
from utils import deprecated

RENAME_FUNCTION_DICT={
    "INT":-1, 
    "BIGINT":-1, #BIGINT(23) 没有列明参数，继续倒序找
    "VARCHAR":-1,
    "DOUBLE":-1,
    "DECIMAL": -1, #DECIMAL(23,2) 没有列明参数，继续倒序找
    
    "CAST": 0, #CAST(a.IMEI_FIRST_COMM_DATE AS date) 需要再函数内部进行搜索。
     
    "NVL":1, #NVL(a.IMEI_FIRST_COMM_DATE, '2020-01-01') 第一个参数
    "TO_CHAR":1,
    "SUB_STR":1,
    "DATE":1,
    "MAX":1,
}


METHOD_DICT ={
    "CAST": lambda s:cast_method(s)
}
SPECIAL_KEYWORD_DICT={
    "END":-1,
}
def cast_method(str_):
    pattern = r'\bAS\s+.*'  
    return re.sub(pattern, '', str_[0], flags=re.IGNORECASE)  


def is_function(str_):
    pattern = r'\b\w+\([^()]*?\)'  
    match = re.search(pattern, str_)
    if match:
        return True
    else:
        return False
    
@deprecated
def split_except_functions(s,delimiter=' '):  
    '''
    保证识别到的函数内部，出现空格，不会被split切割
    如以前name decimal(12, 2) --comment
    会分割为 "name", "decimal(12," , "2)", "--comment"
    现在可以完整的切割为 "name", "decimal(12, 2)", "--comment"
    
    todo: 解决不了函数嵌套的识别问题
    '''
    # 分析段落：括号中的内容直接匹配，其他部分用空格分开  
    #pattern = r'\b\w+\([^()]*?\)'  
    pattern = r'\b(\w+)\s*\([^()]*\)'  
    
    # 将所有模式匹配（例如 function(...) 部分）替换为一个特殊标记  
    temp_placeholder = '\x00'  
    mapped = re.sub(pattern, lambda m: temp_placeholder, s) 
        
    
    # 按空格再次分割整个字符串  
    parts = mapped.split(delimiter)  

    # 恢复替换的标记为实际的 function(...) 值，确保它们完整  
    results = []  
    functions = re.finditer(pattern, s)  
    for part in parts:  
        if part == temp_placeholder:  
            function_match = next(functions)  
            results.append(function_match.group())  
        else:  
            results.append(part)  

    return results 

@deprecated
def extract_functions(input_string,delimiter=','):  
    """
    可以分离所有字符串里的函数名和参数
    input_string =   
    SELECT MAX(sd, 2), AVG(value), custom_function(param1, param2)  
    FROM table_name
    
    output = 
      'MAX': ['sd', '2'], 'AVG': ['value'], 'custom_function': ['param1', 'param2']}
  
    todo: 解决不了函数嵌套的问题 如 sum(max(talk,23), name) 只能识别出 sum， 和 max(talk,23) 后面的name参数丢了
    """
    # 匹配函数名和参数列表的正则表达式  
    pattern = r'(\w+)\s*\((.*?)\)'  

    # 找到所有匹配  
    matches = re.findall(pattern, input_string)  

    # 准备存储结果的字典  
    functions_dict = {}  
    
    for function_name, params in matches:  
        # 将参数按逗号分割并去除空格  
        param_list= split_except_functions(params,delimiter)
        functions_dict[function_name] = param_list  

    return functions_dict  

def get_feature_name_from_function(input_string):
    '''
    用解析后的内容
    '''
    parse_result = parse_function_expression(input_string)[0]
    if isinstance(parse_result, str):
        return parse_result
    
    function_name = parse_result[0]
    if function_name.upper() in RENAME_FUNCTION_DICT.keys():
        id_ = RENAME_FUNCTION_DICT[function_name.upper()]
        
        if id_ == -1:
            return None
        elif id_ > 0:
            return parse_result[1][id_-1]
        elif id_ == 0:
            return  METHOD_DICT[function_name.upper()](parse_result[1])
        return "UNKNOWN"
    return 

def split_except_function_multi(sql_code,list_count=0):
    '''
    [
        'myfeature', 
        'talk.dream', 
        ('decimal', ['12', '3']), 
        ('max', ['2', '3']), 
        ('sum', [('max', ['talk', '23', '23', '323']), '32', 'bb'])
        
        list_count 为了方式某些错误的Tabel建表语句，有太多字段在一行，一直找全部的字段。
    ]
    '''
    parse_result = parse_function_expression(sql_code)
    result_list = []
    for res_ in parse_result:
        if isinstance(res_, tuple):
            # print(res_,sql_code)
            result_list.append(return2str(res_,''))
        elif isinstance(res_, str):
            result_list.append(res_)
    # if list_count == -1:
    #     list_count = len(result_list)
    return result_list[-list_count:]

def parse_function_expression(expression):  
    """
    可以解决函数内嵌套函数的情况
    "decimal(12, 3) , max(2,3), sum(max(talk,23,23,323),32 ,bb) sum(max(a + b, c(d, e)), 123)"
    
    [
        ('decimal', ['12', '3']), 
        ('max', ['2', '3']), 
        ('sum', [('max', ['talk', '23', '23', '323']), '32', 'bb']), 
        ('sum', [('max', ['a+b', ('c', ['d', 'e'])]), '123'])
    ]
    """

    # 正则模式用于匹配函数名和参数部分的起点  
    pattern = r'(\w+)\s*\('  

    def parse(expression, start=0):  
        pos = start  
        result = []  
        current_argument = []  # Store characters of the current argument  

        while pos < len(expression):  
            if expression[pos].isspace():  
                # Skip over spaces  
                pos += 1  
                continue  

            match = re.match(pattern, expression[pos:])  
            if match:  
                # Extract the function name  
                if current_argument:  
                    # If current_argument has content, add it as a completed element before recursing  
                    result.append(''.join(current_argument).strip())  
                    current_argument = []  

                function_name = match.group(1)  
                pos += match.end()  # Move past this function name and opening parenthesis  
                inner_arguments, new_pos = parse(expression, pos)  
                result.append((function_name, inner_arguments))  
                pos = new_pos  
            elif expression[pos] == ',':  
                # Complete the current argument and reset for the next  
                if current_argument:  
                    result.append(''.join(current_argument).strip())  
                    current_argument = []  
                pos += 1  
            elif expression[pos] == ')':  
                # We've reached the end of the current function parameter section  
                if current_argument:  
                    result.append(''.join(current_argument).strip())  
                return result, pos + 1  
            else:  
                # Collect characters into the current argument  
                current_argument.append(expression[pos])  
                pos += 1  

        if current_argument:  
            result.append(''.join(current_argument).strip())  

        return result, pos  

# Start parsing from the beginning of the expression  
    parsed_result, _ = parse(expression)  
    return parsed_result  

def return2str(tuple_, str_):
    '''
    还原之前的tuple的函数解析内容
    '''
    str_ = str_ + tuple_[0] + "("
    for i in range(len(tuple_[1])):
        if isinstance(tuple_[1][i], tuple):
            str_ = return2str(tuple_[1][i], str_)
        else:
            str_ = str_ + tuple_[1][i]
        if i != len(tuple_[1])-1:
            str_ = str_ + ","
    str_ = str_ + ")"
    return str_



def test():
    sql1= "SELECT MAX(sd, 2), AVG(value, small(32,3) ), custom_function(param1, param2) , sum(max(talk,23),32 ,bb) "
    
    sql2 = "#CAST(a.IMEI_FIRST_COMM_DATE AS date)"
    parse_function_expression(sql2)
test()