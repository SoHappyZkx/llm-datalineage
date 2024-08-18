from http import HTTPStatus
import dashscope
from typing import Tuple  
#multi round conversation
from openai import OpenAI
import os


#sk-fbd56500a79e44a79ceaae02d567f25e


def get_response(client:OpenAI, model_name:str, system_prompt:str, question:str, stream:bool=True) -> Tuple[str, str, int, int, int]:
    
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

            
        return content_str, finish_reason_, chunk.usage.completion_tokens,chunk.usage.prompt_tokens,chunk.usage.total_tokens
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
        return answer_content, finish_reason,  tokens_dict.completion_tokens, tokens_dict.prompt_tokens, tokens_dict.total_tokens

#depracated
def get_response_stream(client:OpenAI, model_name:str, system_prompt:str, question:str) -> Tuple[str, str, int, int, int]:
    
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
    for chunk in completion:
        content_ = chunk.choices[0].delta.content
        content_str+=content_
        print(content_,end='')
        if chunk.choices[0].finish_reason:
            finish_reason_ = chunk.choices[0].finish_reason
    return content_str, finish_reason_, chunk.usage.completion_tokens,chunk.usage.prompt_tokens,chunk.usage.total_tokens
        
   

def init_client(API_KEY:str,PLATFORM:str) -> OpenAI:
    
    if PLATFORM == 'qwen'.upper() or PLATFORM == "ali".upper():
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    client = OpenAI(
        api_key = API_KEY, # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url = base_url
    )
    
    return client

if __name__ == "__main__":
        
        filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
        API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
        PLATFORM = "qwen".upper()
        model_name = "qwen-turbo"
        system_prompt = "You are a helpful assistant."
        question = "能否帮我介绍一些机器学习算法？"
        client = init_client(API_KEY,PLATFORM)
        answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = get_response(client, model_name, system_prompt, question)
        #answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = get_response_stream(client, model_name, system_prompt, question)
        print(answer_content)
        print(finish_reason)
        print(completion_tokens)
        #test_multi()
        #