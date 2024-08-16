import os
import re 
def extract_name_and_comment_from_sql(sql):  
    """  
    从SQL字符串中提取每行注释以及注释前的列名字。  
    注意 DROP TABLE tmp_dm_20130916_06;\
        这里的换行符会被识别成 \\ 所以可以增加一步replace \\ -》 \n
    
    """  
    def is_decimal(str_):
        pattern = r'^decimal\([^()]*\)$'  
        match = re.search(pattern, str_) 
        if match:
            return True
        else:
            return False
    
    def other_function(str_):
        pattern = r'\b\w+\([^()]*?\)'  
        match = re.search(pattern, str_)
        if match:
            return True
        else:
            return False 
        
    def split_outside_functions(s):  
        # 分析段落：括号中的内容直接匹配，其他部分用空格分开  
        pattern = r'\b\w+\([^()]*?\)'  
        
        # 将所有模式匹配（例如 function(...) 部分）替换为一个特殊标记  
        temp_placeholder = '\x00'  
        mapped = re.sub(pattern, lambda m: temp_placeholder, s) 
            
        
        # 按空格再次分割整个字符串  
        parts = mapped.split()  

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
    # 针对行注释和块注释的正则表达式  
    line_comment_pattern = re.compile(r'(--|#).*$')  
    block_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)  

    # 去除SQL中的块注释（保留注释内容部分）  
    comments = []  
    sql_without_block_comments = block_comment_pattern.sub(lambda m: __extract_block_comment(m, comments), sql)  
    
    sql_without_block_comments = sql_without_block_comments.replace('\\','\n')
    # 准备分隔符来单独处理每行  
    lines = sql_without_block_comments.split('\n')  

    # 存储提取后的名字和注释的结果  
    results = []  

    for line in lines:  
        # 处理行注释  
        comment_match = line_comment_pattern.search(line)  
        if comment_match:  
            comment = comment_match.group(0).strip()  
            pre_comment_part = line[:comment_match.start()].rstrip(', ')  
            words = split_outside_functions(pre_comment_part)  
            if words:  
                # 处理针对 AS 的情况  
                name = ''  
                for word in reversed(words):  
                    if word.upper() == 'AS':  
                        continue  
                    elif is_decimal(word.lower()):
                        continue
                    elif word.upper() == "END":
                        break
                    elif other_function(word):
                        print(f"[WARNING]@<Comment-function>: unknown renamed function: {word} ")
                        break
                    else:  
                        name = word  
                        break  
            results.append((name, comment))  


    return results,comments

def __extract_block_comment(match, comments):  
    """  
    从块中提取注释内容  
    """  
    comment = match.group(0)  
    comments.append(comment)  
    return ''  # 以便块注释被整个去除  




def test1():
    sql_example1 = """  
    SELECT table1.column1, table2.column2 AS col2 -- Line comment here  
    FROM table1  
    JOIN table2 ON table1.id = table2.id /* block comment starts here  
    this is a multi-line  
    block comment */  
    WHERE table1.value > 100 # Another line comment  
    """  

    sql_example2 = """
    DROP TABLE tmp_dm_20130916_06;


    CREATE TABLE tmp_dm_20130916_06\ (product_no varchar(20),\ gprs_monthly_fee decimal(12, 2), -- 流量出账-月租费
    gprs_gasbag_fee decimal(12, 2), -- 流量出账-加油包费 /* eteasa-- s */
    gprs_flow_fee decimal(12, 2), -- 流量出账-流量费\ 
    gprs_wlan_fee decimal(12, 2), -- 流量出账-WLAN \ 
    gprs_yearhalfyear_fee decimal(12, 2), -- 流量出账-年包半年包\ 
    gprs_quarter_fee decimal(12, 2), -- 流量出账-季包\ 
    gprs_payment_fee decimal(12, 2), -- 流量出账-流量统付\ 
    gprs_infinite_fee decimal(12, 2), -- 流量出账-不限量\ 
    gprs_personality_fee decimal(12, 2), -- 流量出账-个性化\ 
    gprs_national_fee decimal(12, 2), -- 流量出账-国漫套餐\ 
    gprs_unified_fee decimal(12, 2), -- 流量出账-统付\ 
    day_fee decimal(12, 2), -- 流量出账\ 
    user_4gnet_flag smallint, offer_bracket bigint , last_offer_bracket bigint\) distributed BY ('product_no');

    ","parentDsName":"GbaseDM
    """
    results = extract_name_and_comment_from_sql(sql_example2)  
    for name, comment in results:  
        print(f"Column name: {name}, Comment: {comment}")  
        
        
def test2():
    sql_query = """
    DELETE
FROM dm.dm_pub_fanzha_tongxin_dd;


INSERT INTO dm.dm_pub_fanzha_tongxin_dd
SELECT '${day_id}' op_time, -- 数据日期
 a.stat_date, -- 统计日期
 a.phone_no product_no, -- 号码
 max(nvl(zhu_call_num, 0))zhu_call_num, -- 主叫次数
 max(nvl(zhu_call_dur, 0))zhu_call_dur, -- 主叫时长
 max(nvl(zhu_call_opp, 0))zhu_call_opp, -- 主叫对端号码个数
 max(nvl(bei_call_num, 0))bei_call_num, -- 被叫次数
 max(nvl(call_rate, 0))call_rate, -- 离散度（主叫次数/对端号码个数）
 max(nvl(call_30, 0))call_30, -- 小于30秒通话次数
 -- max(nvl(dou,0))dou,                             -- 当月dou
 max(imei)imei, -- imei（终端品牌）
 -- max(work_cell_name) work_cell_name,          -- 白天常驻工作地
 max(prov_name)prov_name, -- 漫游地市
 -- max(stay_cell_name) stay_cell_name,          -- 夜间常驻工作地
 max(out_cell_cnt) out_cell_cnt, -- 统计日主叫基站个数
 max(out_imei_cnt) out_imei_cnt, -- 主叫imei个数
 max(in_call_opp_cnt) in_call_opp_cnt, -- 被叫对端号码个数
 max(CELL_ID) AS CELL_ID, -- 当日主叫次数最多的基站ID
 max(cell_name) AS cell_name, -- 当日主叫次数最多的基站名称
 max(begin_time) AS begin_time, -- 首次主叫时间（时分秒）
 max(min_stop_time) AS min_stop_time, -- 最早停机时间（当天根据公共注释-人卡分离)
 max(count_stop_num) AS count_stop_num, -- 停机次数（当天根据公共注释-人卡分离)
 max(min_start_time) AS min_start_time, -- 最早复机时间（当天根据公共注释-人卡分离)
 max(count_start_num) AS count_start_num, -- 复机次数（当天根据公共注释-人卡分离)
 max(count_start_num_xs) AS count_start_num_xs, -- 线上复机次数（当天根据公共注释-人卡分离，操作员是BJCRMCS）
 max(imei_cnt) AS imei_cnt -- 当日使用imei个数（剔重，语音和流量都算）
FROM dm.tmp_dm_pub_fanzha_tongxin_ds_${dayid} a
LEFT JOIN gbasedwi.DWI_USR_PESN_THINGINTER_DS_${dayid} b ON a.phone_no=b.USER_NO
WHERE a.stat_date IS NOT NULL
  AND a.stat_date>='${pre60d}'
  AND b.USER_NO IS NULL
GROUP BY a.stat_date,
         a.phone_no ;
    """
    
    
    pattern = r'(\)\s*)([a-zA-Z_]\w*)'  
    
    # 替换匹配的部分，添加空格  
    updated_query = re.sub(r'(\)\s*)([a-zA-Z_]\w*)' , r') \2', sql_query)  
    print(updated_query)



def test3():
    
    sql_query = "deasd(d,3m5m,,max(2,3)), max()dad, talk(ddasd)"
    pattern = r'(\w+)\s*\((.*?)\)'  
    
    # 找到所有匹配  
    matches = re.findall(pattern, sql_query)
    print(matches)
    
    
def test4():
    sql='''
    
    talk(23,3), sasd  max(2,4), sum(max(talkingnaum,1))
    '''
    
    def return2str(tuple_, str_):
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
    def parse_function_expression(expression):  
        """
        可以解决函数内嵌套函数的情况
        "decimal(12, 3) , max(2,3), sum(max(talk,23,23,323),32 ,bb) sum(max(a + b, c(d, e)), 123) home"
        
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

                    function_name = match.group(1)  #第一个捕获组的内容是函数名字
                    pos += match.end()  # Move past this function name and opening parenthesis  
                    inner_arguments, new_pos = parse(expression, pos)  
                    result.append((function_name, inner_arguments))  
                    pos = new_pos  
                elif expression[pos] == ',':  #一个字符一个字符判断，碰到,的时候知道是函数体内部，所以需要拼接参数，分割。
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

    # 示例测试  
    expression = "sum(max(a + b, c(d, e)), 123)"  
    parsed_output = parse_function_expression(expression)  
    
    sql1 = "myfeature,  talk.dream, decimal(12, 3) , max(2,3), sum(max(talk,23,23,323),32 ,bb) sum(max(a + b, c(d, e)), 123) home, asboy"
    parsed_output = parse_function_expression(sql1)  
    print(sql1)
    print(parsed_output)  
    result_str=''
    for res_ in parsed_output:
        if isinstance(res_, tuple):
            print(res_)
            result_str += return2str(res_,'')
            result_str += ', '
        elif isinstance(res_, str):
            result_str += res_
            result_str += ', '
    print(result_str)

def test5():
    def find_function_positions(expression):  
        # 定义用于匹配外层函数调用的正则表达式  
        # 这里简单匹配函数名和非嵌套参数  
        pattern = r'\b(\w+)\s*\((.*?)\)'  

        # 查找所有匹配项  
        matches = re.finditer(pattern, expression)  

        # 存储结果的位置  
        positions = []  

        for match in matches:  
            start = match.start()  # 获取匹配的起始位置  
            end = match.end()      # 获取匹配的结束位置  
            positions.append((start, end))  

        return positions  

    # 示例测试  
    expression = "function1(param1, function2(param2, param3), param4)   talk(),  sum(max(23,4))"  
    positions = find_function_positions(expression)  
    for start, end in positions:  
        print(expression[start:end])
    print(positions)


def test6():
    import re  

    def clean_sql_whitespace(sql):  
        # 定义一个内部函数来去除括号内的多余空格  
        def remove_spaces_within_parentheses(match):  
            content = match.group(1)  
            # 去除括号内的所有空格  
            cleaned_content = re.sub(r'\s+', '', content)  
            return f"({cleaned_content})"  

        # 去除括号内的多余空格  
        sql = re.sub(r'\(\s*([^)]*?)\s*\)', remove_spaces_within_parentheses, sql)  

        # 保持 SQL 关键字及其前后的空格（可以根据需要扩展关键字）  
        keywords = ['AS', 'JOIN', 'ON', 'WHERE', 'FROM', 'SELECT',  
                    'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE']  
        # 构造保留空格的正则表达式，匹配这些关键字及其前后  
        keywords_pattern = r'\b(?:' + '|'.join(keywords) + r')\b'  

        # 临时替换掉我们不想影响空格位置的地方  
        sql = re.sub(rf'(?i)({keywords_pattern})', r' \1 ', sql)  

        # 去除多余的空格（去除除关键字及其前后空格外的空格）  
        sql = re.sub(r'\s+', ' ', sql).strip()  

        return sql  

    # 示例 SQL 代码  
    sql_examples = [  
        "SELECT column1 , column2 FROM   table_name  WHERE  column3  =  function(  column4 , column5 )  AS result ",  
        "INSERT  INTO  table  VALUES  (  value1 , value2  , value3 )",  
        "UPDATE table_name SET column1 = function ( column2 , column3 ) WHERE column4 = value4"  ,
        "test nvl( a.teas as TEST2, 0)"
    ]  

    # 使用函数去除空格  
    for sql in sql_examples:  
        cleaned_sql = clean_sql_whitespace(sql)  
        print(cleaned_sql)  
        
test6()