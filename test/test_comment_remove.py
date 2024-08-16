import re

def fix_sql_comments(sql):  
    # Regular expressions to match SQL comments  
    comment_patterns = [  
        r'(#.*?$)',   # Match # comments till the end of line  
        r'(--.*?$)',  # Match -- comments till the end of line  
    ]  
    
    # Combine regular expressions into one pattern using alternation  
    combined_pattern = '|'.join(comment_patterns)  
    
    # Split the SQL into lines  
    sql_lines = sql.splitlines()  
    
    processed_lines = []  

    for line in sql_lines:  
        # Search for comment patterns in the line  
        match = re.search(combined_pattern, line)  
        
        if match:  
            start, end = match.span()  
            comment = match.group()  
            
            # Separate the code and comment  
            code_part = line[:start].strip()  
            comment_part = comment.strip()  
            
            if code_part:  
                processed_lines.append(f"{code_part} ")  
                processed_lines.append(f"{comment_part}\n")  
            else:  
                processed_lines.append(f"{comment_part}\n")  
        else:  
            processed_lines.append(f"{line}\n")  
    
    # Recombine the lines into a single SQL script  
    processed_sql = ''.join(processed_lines)  
    return processed_sql  


def process_sql_comments(sql):  
    # Regular expressions to match SQL comments  
    comment_patterns = [  
        r'(#+[^\r\n]*)',       # Match # comments  
        r'(--+[^\r\n]*)',      # Match -- comments  
    ]  
    
    # Combine regular expressions into one pattern using alternation  
    combined_pattern = '|'.join(comment_patterns)  
    
    # Split the SQL into lines  
    sql_lines = sql.splitlines()  
        
    processed_lines = []  

    for line in sql_lines:  
        # Process one line multiple times if there are many comments  
        while line:  
            match = re.search(combined_pattern, line)  
            
            if match:  
                start, end = match.span()  
                comment = match.group()  
                
                # Separate the code and comment  
                code_part = line[:start].strip()  
                comment_part = comment.strip()  
                
                if code_part:  
                    processed_lines.append(f"{code_part}\n")  
                processed_lines.append(f"{comment_part}\n")  
                
                # Continue processing the remainder of the line  
                line = line[end:].strip()  
            else:  
                processed_lines.append(f"{line.strip()}\n")  
                break  
    
    # Recombine the lines into a single SQL script  
    processed_sql = ''.join(processed_lines)  
    return processed_sql  



def split_code_comments(sql_line):  
    """  
    Splits a SQL line into code and comments based on the given rules:  
    1) Comments start with -- or #.  
    2) Comments are usually in Chinese, SQL code is in English.  
    3) There is usually at least one space between code and comments.  
    """  
    parts = []  
    comment_patterns = [r'--', r'#']  
    regex = re.compile(r"({})\s*(.*)".format("|".join(comment_patterns)))  

    # Iterate over the line to split code and comments  
    while sql_line:  
        # Search for the first occurrence of a comment pattern  
        match = regex.search(sql_line)  

        if match:  
            # Positions of comment start  
            start = match.start()  
            comment_start = match.group(1)  
            comment_text = match.group(2).strip()  
            
            if start > 0:  
                # Add the SQL code part before the comment as a separate part  
                code_part = sql_line[:start].rstrip()  
                if code_part:  
                    parts.append((code_part, 'code'))  
            # Add the comment part  
            if comment_text:  
                parts.append((f"{comment_start} {comment_text}", 'comment'))  
            
            # Move to the next part of the string  
            sql_line = sql_line[match.end():].strip()  
        else:  
            # If no more comments are found, add the remaining part as code  
            if sql_line.strip():  
                parts.append((sql_line.strip(), 'code'))  
            break  
    
    return parts  


def find_comments_and_fields(sql):  
    # 定义匹配注释的正则表达式模式（-- 注释或 # 注释）  
    pattern = r"(--|#)\s*(.*)"  
    
    # 定义匹配字段名的正则表达式模式  
    field_pattern = r"(\w+)\s*"  
    
    matches = re.finditer(pattern, sql)  
    
    result = []  
    for match in matches:  
        # 获取注释  
        comment = match.group(2)  
        
        # 获取注释前的代码  
        code = sql[:match.start()]  
        
        # 找到最近的字段名  
        field_match = re.search(field_pattern, code[::-1])  # 反转查找  
        if field_match:  
            field = field_match.group(1)[::-1]  # 反转回来  
            result.append((field, comment))  
    
    return result  




def test():
    sql_string1 = """  
    INSERT INTO dm.dm_pub_imei_info_${dayid}  
    SELECT DISTINCT a.OP_TIME , -- 数据日期 a.IMEI , -- 14位imei a.IMEI8 , -- TAC码 a.TERM_BRAND , -- 终端品牌 a.TERM_MODEL , -- 终端型号 a.REMAIN_TYPE , -- 终端类型 nvl(b.SALE_type, a.SALE_STUS) AS SALE_STUS , -- 销售状态_新 b.SALE_DATE AS SALE_TIME , -- 销售日期_新 a.chl_class , -- 销售渠道 b.SALE_dept_id COUNTY_ID , -- 销售分公司_新 b.SALE_dept_name dept_COUNTY_ID , -- 销售分公司id_新 a.SP_NAME , -- 销售SP (前台下线) a.SALE_DEPT_NAME , -- 销售部门 b.A_BSNAME AS SVC_NAME , -- 销售方案_新 b.A_BS_PACKGE_NAME AS SALE_PLAN , -- 销售方案类型_新 a.SPECIAL_LOAD_FLAG , -- 是否特殊货源 a.PRODUCT_NO_PLAN , -- 合约机号码 a.IS_CELL , -- 是否SCM销售 (前台下线) a.FIRST_TIME , -- imei首次通信日期 a.LAST_TIME , -- imei末次通信日期 a.FIRST_BILL_PRODUCT_NO , -- imei首次计费号码 a.FIRST_BILL_TIME , -- imei首次计费号码时间 a.IS_PLAN_IMEI , -- 合约机号码是否与使用号码一致 a.IMEI_CELL_COUNT , -- imei当月对应基站数 a.IMEI_PRODUCT_COUNT , -- imei当月通信手机号码个数 a.IMEI_MAX_PRODUCT , -- 当月使用最多手机号 a.IMEI_MAX_PRODUCT_STATUS , -- 当月使用最多手机号的状态 a.IMEI_MAX_PRODUCT_COUNTY , -- 前台不展示 a.IS_IMEI , -- 是否稳定终端 a.CALL_MARK , -- 当月通信天数 a.CALL_COUNTS , -- 当月通话次数 a.CALL_DURATION_M , -- 当月T网通话时长（分钟） a.G2_FLOWS , -- 当月使用2G流量 a.G3_FLOWS , -- 当月使用3G流量 a.G4_FLOWS , -- 当月使用4G流量 a.G3_FLOWS_YEAR , -- 当年累计3G流量 a.G3_FLOWS_YEAR_COUNT , -- 当年累计3G使用次数 a.G4_FLOWS_YEAR , -- 当年累计4G流量 a.G4_FLOWS_YEAR_COUNT , -- 当年累计4G使用次数 a.IMEI_THREEFOUR_PRODUCT , -- 3/4G稳定手机号码 a.IMEI_THREEFOUR_PRODUCT_COUNTY , -- 3/4G稳定手机号码的归属分公司 a.LAST_PRODUCT_NO , -- imei当月末次通信手机号码 b.prod_lvl AS PROD_LEVEL , -- 产品等级_新 a.call_dur , -- 当月通话时长（分钟） a.is_5g_imei , -- 是否5Gimei a.standard , -- 制式 a.terminal_type , -- 是否手机 a.rj_SA , -- 软件是否支持SA a.YJ_SA , -- 硬件是否支持SA a.rj_700 , -- 软件是否支持700M a.yj_700 , -- 硬件是否支持700M b.imei AS imei_15 , -- IMEI（15位）_新 b.ITEM_VAL_VALUE , -- 设备类别_新 b.B_PROD_CODE_ID , -- 机型编码_新 b.B_PROD_NAME , -- 机型名称_新 b.B_RSRV_STR2 , -- 通俗名称_新 b.YANSE , -- 颜色_新 b.SUPPLY_PRICE , -- 供货价_新 b.IS_PUBLIC , -- 是否公开版_新 b.PROD_LVL2 , -- 产品等级二级_新 b.BA_ORG_NAME , -- 销售组织名称_新 b.BA_ORG_CODE , -- 销售组织编码_新 b.BA_ORG_SX , -- 销售渠道属性_新 b.OFFER_ID , -- 策划ID_新 b.PLAN_NAME , -- 业务方案_新 b.STATUS , -- 结算状态_新 b.OPER_date AS OPER_TIME , -- 结算日期_新 b.FLOWNUM , -- CRM交易号_新 b.WORK_NUM , -- CRM工号_新 b.SALER_NAME , -- 促销员名称_新 b.SALER_ID , -- 促销员编码_新 b.B_IS_ECOMMERCE -- 是否电商_新  
    FROM  
    (SELECT DISTINCT *  
    FROM dm.tmp01_dm_pub_imei_info_ds_${dayid}) a  
    LEFT JOIN  
    (SELECT DISTINCT *  
    FROM dm.tmp05_dm_pub_imei_info_ds_${dayid}) b ON a.IMEI=substr(b.IMEI, 1, 14) ;  
    """  

    processed_sql1 = fix_sql_comments(sql_string1)  
    print(processed_sql1)  


    sql_string2 = """  
    CREATE TABLE test_table (  
        id INT,  
        bxl_gprs_resource_bhd decimal(10, 4), #饱和度-不限量产品  isbxl_arriveuse bigint, -- 是否不限量套餐到达用户  ##以下20181130日添加  
    );  
    """  

    processed_sql2 = process_sql_comments(sql_string2)  
    print(processed_sql2)  
    
def find_comment_positions(sql_string):  
    # Define the regex pattern to find -- or # in the string  
    pattern = re.compile(r'--|#')  
    
    # Find all matches of the pattern  
    matches = pattern.finditer(sql_string)  

    # Extract the starting position of each match  
    positions = [match.start() for match in matches]  
    
    return positions  


def test2():
    # Test the function  
    # sql_line = "SELECT DISTINCT a.OP_TIME , -- 数据日期 a.IMEI , -- 14位imei a.IMEI8 , -- TAC码 a.TERM_BRAND "  
    # split_parts = split_code_comments(sql_line)  
    # for part, ptype in split_parts:  
    #     print(f"{ptype}: {part}")  

    # Integration within the function  
    def process_sql(sql):  
        sql_lines = sql.splitlines()  
        processed_lines = []  

        for line in sql_lines:  
            parts = split_code_comments(line)  
            for part, ptype in parts:  
                processed_lines.append(part + '\n')  

        return ''.join(processed_lines)  

    # Example SQL string  
    sql_string = """  
    INSERT INTO dm.dm_pub_imei_info_${dayid}  
    SELECT DISTINCT a.OP_TIME , -- 数据日期 a.IMEI , -- 14位imei a.IMEI8 , -- TAC码 a.TERM_BRAND , -- 终端品牌 a.TERM_MODEL , -- 终端型号  
    """  
    find_comment_positions(sql_string)
    processed_sql = process_sql(sql_string)  
    print(processed_sql)  



def test3():
    # 示例 SQL 代码  
    sql_code = """  
    SELECT id, name, age  -- 这是一个注释  
    FROM users  
    WHERE age > 20  # 年龄大于20的用户  
    ;  
    """  

    results = find_comments_and_fields(sql_code)  
    for field, comment in results:  
        print(f"字段: {field}, 注释: {comment}")
    
test2()