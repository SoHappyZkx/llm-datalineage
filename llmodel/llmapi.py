from http import HTTPStatus
import dashscope
from typing import Tuple  
#multi round conversation
from openai import OpenAI
import os
from typing import Union, List  


#sk-fbd56500a79e44a79ceaae02d567f25e

def get_messages_dict(system_prompt:Union[str,list], question:Union[str,list]) -> list:
    messages_list = []
    if isinstance(system_prompt, str):
        messages_list.append(dict({'role': 'system', 'content': f"{system_prompt}"}))
    else:
        for prompt in system_prompt:
            messages_list.append(dict({'role': 'system', 'content': f"{prompt}"}))
    if isinstance(question, str):
        messages_list.append(dict({'role': 'user', 'content': f"{question}"}))
    else:
        for q in question:
            messages_list.append(dict({'role': 'user', 'content': f"{q}"}))
    return messages_list


def get_response(client:OpenAI, model_name:str, system_prompt:str, question:str, stream:bool=True) -> Tuple[str, str, int, int, int]:
    messages_list = get_messages_dict(system_prompt, question)
    return get_response_template(client, model_name, messages_list,stream)
    


def get_response_template(client:OpenAI, model_name:str, messages_list:list, stream:bool=True) -> Tuple[str, str, int, int, int]:
    
    if stream:
        completion = client.chat.completions.create(
        model=model_name,
        messages=messages_list,
        stream=True,
        stream_options={"include_usage": True},
        temperature=0.8,
        top_p=0.8
        )
    
        content_str = ""
        finish_reason_ = None
        Finish_flag=False
        for chunk in completion:
            # print(chunk.model_dump_json)
            if  not Finish_flag:
                content_ = chunk.choices[0].delta.content
                content_str+=content_
                print(content_,end='')
                if  chunk.choices[0].finish_reason:
                    finish_reason_ = chunk.choices[0].finish_reason  
                    Finish_flag=True

        #9230 - >3695
        return content_str, finish_reason_, chunk.usage.prompt_tokens,  chunk.usage.completion_tokens,  chunk.usage.total_tokens
    else:
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages_list,
            temperature=0.8,
            top_p=0.8
            )
        answer_content = completion.choices[0].message.content
        finish_reason = completion.choices[0].finish_reason  # 长度过长: length, 正常结束: stop
        tokens_dict = completion.usage
        return answer_content, finish_reason,  tokens_dict.prompt_tokens,  tokens_dict.completion_tokens,  tokens_dict.total_tokens
#depracated
def get_response_normal(client:OpenAI, model_name:str, system_prompt:str, question:str, stream:bool=True) -> Tuple[str, str, int, int, int]:
    '''
    暂时废弃，使用get_response_template， 这种用法不适用于多轮对话，多问题，多系统设定的场景
    '''
    if stream:
        completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': f"{system_prompt}"},
            {'role': 'user', 'content': f"{question}"}],
        stream=True,
        stream_options={"include_usage": True},
        temperature=0.8,
        top_p=0.8
        )
    
        content_str = ""
        finish_reason_ = None
        Finish_flag=False
        for chunk in completion:
            # print(chunk.model_dump_json)
            if  not Finish_flag:
                content_ = chunk.choices[0].delta.content
                content_str+=content_
                print(content_,end='')
                if  chunk.choices[0].finish_reason:
                    finish_reason_ = chunk.choices[0].finish_reason
                    Finish_flag=True

            
        return content_str, finish_reason_, chunk.usage.prompt_tokens,  chunk.usage.completion_tokens,  chunk.usage.total_tokens
    else:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': f"{system_prompt}"},
                {'role': 'user', 'content': f"{question}"}],
            temperature=0.8,
            top_p=0.8
            )
        answer_content = completion.choices[0].message.content
        finish_reason = completion.choices[0].finish_reason
        tokens_dict = completion.usage
        return answer_content, finish_reason,  tokens_dict.prompt_tokens,  tokens_dict.completion_tokens,  tokens_dict.total_tokens
        
   

def init_client(API_KEY:str,PLATFORM:str) -> OpenAI:
    
    if PLATFORM == 'qwen'.upper() or PLATFORM == "ali".upper():
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    client = OpenAI(
        api_key = API_KEY, # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url = base_url
    )
    
    return client


def test_get_sql_code(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_code_str = f.read()
    return sql_code_str


def test1():
    filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
    API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
    PLATFORM = "qwen".upper()
    model_name = "qwen-turbo"
    system_prompt = "You are a helpful assistant."
    #question = "能否帮我介绍一些机器学习算法？"
    
    
    sql_file = "F:\\GITClone\\CMCCtest\\sql-lineage\\llm-datalineage\\data_trans\\step2\\客服表--DM_AUTORPT_CS_YYYYMM\\客服表--DM_AUTORPT_CS_YYYYMM-10.sql"
    sql_code = test_get_sql_code(sql_file)
    question = f"下面这段sql讲的是什么?{sql_code}"
    client = init_client(API_KEY,PLATFORM)
    answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = get_response(client, model_name, system_prompt, question)
    print(answer_content)
    print(finish_reason)
    print(prompt_tokens, completion_tokens, total_tokens)


def test2():
    filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
    API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
    PLATFORM = "qwen".upper()
    model_name = "qwen-long"
    system_prompt = "You are a helpful assistant."
    #question = "能否帮我介绍一些机器学习算法？"
    
    
    sql_file = "F:\\GITClone\\CMCCtest\\sql-lineage\\llm-datalineage\\data_trans\\step2\\服务使用表（语音）--AUTORPT\\服务使用表（语音）--AUTORPT-17.sql"
    sql_code = test_get_sql_code(sql_file)
    system_prompt_list = [system_prompt, sql_code]
    question = """ 请把这段sql代码中所有的表名和字段名输出，使用json格式，格式如下：'{"表名1":["字段名1","字段名2","字段名3], "表名2":["字段名4","字段名5"]}' 注意不要其他任何描述和结论，只要输出json内容"""
    client = init_client(API_KEY,PLATFORM)
    answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = get_response(client, model_name, system_prompt_list, question,stream=False)
    
    print(answer_content)
    print(finish_reason)
    print(prompt_tokens, completion_tokens, total_tokens)

if __name__ == "__main__":
    print("")
    #test1()
    #test2()
    