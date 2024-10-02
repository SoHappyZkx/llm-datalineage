import json
import yaml
import llmapi
import re
def parse_json(str_): 
    #pattern = r'```json\n\[\s\S]*?\n```'   
    #matches = [(match.start(), match.end()) for match in re.finditer(pattern, str_)]  
    pattern = r'```json\n(.*?)\n```'
    matches = re.findall(pattern, str_, re.DOTALL) 
    str_json = matches[0].replace('\n','')
    json_dict = json.loads(str_json)
    return json_dict  

# 示例文本  
def get_table_prompt(sql_str,model_name='other'):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_TABLE_PROMPT = '''
        你是一个SQL代码专家，请帮我从上述SQL代码中取出所有相关的table名字，以json的格式输出，比如：{"table1","table2","table3"}。
        '''
        return SYSTEM_PROMPT, QUESTION_TABLE_PROMPT
    else:
        QUESTION_TABLE_PROMPT = '''
        你是一个SQL代码专家，请帮我从下列SQL代码中取出所有相关的table名字，以json的格式输出，比如：{"table1","table2","table3"}。
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        return '', QUESTION_TABLE_PROMPT

def get_field_with_table_prompt(sql_str, sql_table_name,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_FIELD_PROMPT ='''
        你是一个SQL代码专家，请你帮我从上述SQL代码中提取出和%s相关的所有字段名，以json格式输出,具体结构如下:{"table1":["字段名1","字段名2","字段名3"]}
        '''%(sql_table_name)
    
        return SYSTEM_PROMPT, QUESTION_FIELD_PROMPT
    else:
        QUESTION_FIELD_PROMPT ='''
        你是一个SQL代码专家，请你帮我从下列SQL代码中提取出和%s相关的所有字段名，以json格式输出,具体结构如下:{"table1":["字段名1","字段名2","字段名3"]}
        具体SQL代码如下:%s
        '''%(sql_table_name,sql_str)
        return '', QUESTION_FIELD_PROMPT


def get_all_table_field_json_prompt(sql_str,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_ALL_FIELD_PROMPT ='''
        你是一个SQL代码专家，请你帮我从上述SQL代码中提取出和相关的所有字段名，以json格式输出,具体结构如下:{"table1":["字段名1","字段名2","字段名3"]}
        '''
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT = '''
        你是一个SQL代码专家，请帮我从下列SQL代码中取出所有相关的table名字和字段名字。输出的结果使用json格式。具体的结构如下：{"table1":["字段名1","字段名2","字段名3"], "table2":["字段名4","字段名5]}
        具体SQL代码如下:%s
        '''%(sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT

#deprecated
def get_tuple_from_sql_code_v1(sql_str,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_ALL_FIELD_PROMPT ='''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
        1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.TRANSFORM:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        3.AGGREGATION:多个字段进行了聚合操作，如SUM,AVG等等，变成了一个字段，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        4.SPLIT:一个字段被拆分成了不同部分，组成了不同的字段，比如INSERT INTO table2 (column1) SELECT SPLIT_STRING(column1,'-',1) FROM table1;
        5.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        6.JOIN:两个表通过JOIN操作连接起来，比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        7.DERIVE: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        8.OTHERS: 其它无法明确分类的请划分在这里面
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出。
        '''
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT = '''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
        1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.TRANSFORM:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        3.AGGREGATION:多个字段进行了聚合操作，如SUM,AVG等等，变成了一个字段，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        4.SPLIT:一个字段被拆分成了不同部分，组成了不同的字段，比如INSERT INTO table2 (column1) SELECT SPLIT_STRING(column1,'-',1) FROM table1;
        5.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        6.JOIN:两个表通过JOIN操作连接起来，比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        7.DERIVE: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        8.OTHERS: 其它无法明确分类的请划分在这里面
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出。
        具体代码如下:%s
        '''%(sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT


def get_tuple_from_sql_code(sql_str,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_ALL_FIELD_PROMPT ='''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
        1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3.NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5.TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1；
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
        6.WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1；
        其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
        7.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        8.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        9. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        10.OTHERS: 其它无法明确分类的请划分在这里.
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出。
        '''
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT = '''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
         1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3.NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5.TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1；
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
        6.WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1；
        其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
        7.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        8.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        9. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        10.OTHERS: 其它无法明确分类的请划分在这里.
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出。
        具体代码如下:%s
        '''%(sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT


def get_json(client, model_name, sql_str,model_max_input_len=6000,model_max_output_len=2000,ts_rate=2):

    
    if len(sql_str)> ts_rate*model_max_input_len:
        system_session = get_table_prompt(sql_str)
        table_list = parse_json(system_session)     
        for table_name in table_list:
            system_session_table,question_prompt = get_field_with_table_prompt(sql_str,table_name)
            answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(
                client, 
                model_name,
                system_session_table,
                question_prompt,
                stream=False)


                
    else:
        system_prompt, question_prompt = get_all_table_field_json_prompt(sql_str)
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(
                client, 
                model_name, 
                system_prompt, 
                question_prompt,
                stream=False)
        
        
if __name__ == "__main__":
    API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
    PLATFORM = "qwen".upper()
    model_name = "qwen-long" #要求把sql内容放在system里
    client = llmapi.init_client(API_KEY,PLATFORM)
    system_prompt_init = "You are a helpful assistant."
    ROOT_PATH = 'E:\\个人\\工作\\llm-datalineage'
    sql_file1 = f"{ROOT_PATH}\\data_trans\\step2\\服务使用表（语音）--AUTORPT\\服务使用表（语音）--AUTORPT-17.sql" #(最长)
    sql_file2 = f"{ROOT_PATH}\\data_trans\\step2\\2015年5月新增日累计指标\\2015年5月新增日累计指标-206.sql"
    
    
    
    def test1(client,model_name,sql_file):
        sql_code = llmapi.test_get_sql_code(sql_file)
        system_prompt, question_prompt = get_table_prompt(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        print(answer_content)
    
    def test2(client, model_name, sql_file):
        sql_code = llmapi.test_get_sql_code(sql_file)
        #system_prompt, question_prompt = get_all_table_field_json_prompt(sql_code,model_name)
        system_prompt, question_prompt = get_tuple_from_sql_code(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        json_dict = parse_json(answer_content)
        
        print(json_dict)   
    #test1(client,model_name,sql_file1)
    test2(client,model_name,sql_file2)