import json
import yaml
import llmapi as llmapi
import os
import re
import prompt as pmt 

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
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。如果是中间的子查询临时表，请以subquery_{name}命名，其中name应该是sql代码里使用的临时重命名，保证能一一对应。  
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
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。如果是中间的子查询临时表，请根据代码进行命名，保证能一一对应。 
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
        
        QUESTION_ALL_FIELD_PROMPT =pmt.version3
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT ='''%s,具体代码如下:%s'''%(pmt.version3, sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT

def get_table_relation_prompt(sql_str,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_ALL_FIELD_PROMPT =pmt.version9_2
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT ='''%s,具体代码如下:%s'''%(pmt.version9_2, sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT
def get_field_relation_prompt(sql_str,model_name):
    if model_name == 'qwen-long':
        SYSTEM_PROMPT = '''
        现在有一段SQL代码如下:%s
        '''%(sql_str)
        
        QUESTION_ALL_FIELD_PROMPT =pmt.version8_3
        return SYSTEM_PROMPT, QUESTION_ALL_FIELD_PROMPT
    else:
        QUESTION_ALL_FIELD_PROMPT ='''%s,具体代码如下:%s'''%(pmt.version8_3, sql_str)
        return '', QUESTION_ALL_FIELD_PROMPT


#@deprecated
def get_json_v1(client, model_name, sql_str,model_max_input_len=6000,model_max_output_len=2000,ts_rate=2):

    '''
    自动根据input长度和大小输出。但是目前可能不需要了，因为qwen的上下文长度很高！
    '''
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
        

def get_json(client, model_name, sql_str,model_max_input_len=6000,model_max_output_len=2000,ts_rate=2):

    '''
    自动根据input长度和大小输出。但是目前可能不需要了，因为qwen的上下文长度很高！
    '''
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
    
def get_answer_json(client,model_name,sql_file,PROMPT_TYPE='field',system_prompt_init='You are a helpful assistant.'):
    '''
    PROMPT_TYPE: 用于存储文件后缀(suffix)，以及选择不同的提示词模板类别
    PREFIX: 文件前缀，用于记录文件是否为正常完成的内容。stop是默认大模型返回的标准结束结果。也用于检查文件是否存在，是否需要重新生成
    '''

    sql_code = llmapi.get_sql_code(sql_file)
    
    if PROMPT_TYPE=='field':
        system_prompt, question_prompt = get_field_relation_prompt(sql_code,model_name)
    elif PROMPT_TYPE=='table':
        system_prompt, question_prompt = get_table_relation_prompt(sql_code,model_name)

    system_prompt_list = [system_prompt_init, system_prompt]
    answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
    
    
    #分情况
    if answer_content == "META TABLE": #第一种情况，输入内容太少了，只有元数据。
        return {}, "META", completion_tokens,prompt_tokens,total_tokens
    
    json_dict = parse_json(answer_content)
    return json_dict, finish_reason, completion_tokens,prompt_tokens,total_tokens
    
if __name__ == "__main__":
    API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
    PLATFORM = "qwen".upper()
    model_name = "qwen-long" #要求把sql内容放在system里
    client = llmapi.init_client(API_KEY,PLATFORM)
    system_prompt_init = "You are a helpful assistant."
    ROOT_PATH = os.environ['ROOT_PATH']
    sql_file1 = f"{ROOT_PATH}\\data_trans\\step2\\服务使用表（语音）--AUTORPT\\服务使用表（语音）--AUTORPT-17.sql" #(最长)
    sql_file2 = f"{ROOT_PATH}\\data_trans\\step2\\2015年5月新增日累计指标\\2015年5月新增日累计指标-206.sql"
    sql_file3 = f"{ROOT_PATH}\\debug\\special_case\\2012年12月新增指标-109.sql"
    output_dir = f"{ROOT_PATH}\\llmodel\\test_output\\"
    
    
    def test1(client,model_name,sql_file):
        sql_code = llmapi.get_sql_code(sql_file)
        system_prompt, question_prompt = get_table_prompt(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        print(answer_content)
    
    def test2(client, model_name, sql_file):
        sql_code = llmapi.get_sql_code(sql_file)
        #system_prompt, question_prompt = get_all_table_field_json_prompt(sql_code,model_name)
        system_prompt, question_prompt = get_tuple_from_sql_code(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        json_dict = parse_json(answer_content)
        print(json_dict)   
        
    def test3(client, model_name, sql_file,output_dir):
        sql_file_name = os.path.splitext(os.path.split(sql_file)[-1])[0]
        
        sql_code = llmapi.get_sql_code(sql_file)
        system_prompt, question_prompt = get_field_relation_prompt(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        sql_relation_file_name = os.path.join(output_dir, f"{finish_reason}_{sql_file_name}_field.json")
        if answer_content == 'META TABLE':
            pass
        else:
            json_dict = parse_json(answer_content)
            with open(sql_relation_file_name, 'w', encoding='utf-8') as f:
                json.dump(json_dict, f, ensure_ascii=False, indent=4)
        
        
        system_prompt, question_prompt = get_table_relation_prompt(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        sql_table_relation_file_name = os.path.join(output_dir, f"{finish_reason}_{sql_file_name}_table.json")
        if answer_content == 'META TABLE':
            pass
        else:
            json_dict = parse_json(answer_content)
            with open(sql_table_relation_file_name, 'w', encoding='utf-8') as f:
                json.dump(json_dict, f, ensure_ascii=False, indent=4)
        
    
    #测试get_answer_json
    def test4(client, model_name, sql_file):
        sql_code = llmapi.get_sql_code(sql_file)
        system_prompt, question_prompt = get_all_table_field_json_prompt(sql_code,model_name)
        system_prompt_list = [system_prompt_init, system_prompt]
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt_list, question_prompt,stream=True)
        json_dict = parse_json(answer_content)
        print(json_dict)

        ...
    #test1(client,model_name,sql_file1)
    #test2(client,model_name,sql_file2)
    test3(client,model_name,sql_file3,output_dir)