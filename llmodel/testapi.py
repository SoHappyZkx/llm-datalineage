from http import HTTPStatus
import dashscope

#multi round conversation
from openai import OpenAI
import os

#sk-fbd56500a79e44a79ceaae02d567f25e
'''
{"id":"chatcmpl-f2341349-a78e-9fe2-96db-bb7593b120d1",
 "choices":[{"finish_reason":"stop",
             "index":0,
             "logprobs":null,
             "message":{"content":"我是阿里云开发的一款超大规模语言模型，我叫通义千问。",
                        "refusal":null,
                        "role":"assistant",
                        "function_call":null,
                        "tool_calls":null
                        }}],
 "created":1723031825,
 "model":"qwen-turbo",
 "object":"chat.completion",
 "service_tier":null,
 "system_fingerprint":null,
 "usage":{"completion_tokens":17,
          "prompt_tokens":22,
          "total_tokens":39}}
'''


def call_with_messages():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '请介绍一下通义千问'}]

    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

def get_response():
    client = OpenAI(
        api_key="sk-fbd56500a79e44a79ceaae02d567f25e", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '你是谁？'}],
        temperature=0.8,
        top_p=0.8
        )
    print(completion.model_dump_json())

def get_response_multi(messages):
    client = OpenAI(
        # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        api_key="sk-fbd56500a79e44a79ceaae02d567f25e", 
        # 填写DashScope服务的base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=messages,
        temperature=0.8,
        top_p=0.8
        )
    return completion

# 您可以自定义设置对话轮数，当前为3
def test_multi():
    
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    for i in range(3):
        user_input = input("请输入：")
        # 将用户问题信息添加到messages列表中
        messages.append({'role': 'user', 'content': user_input})
        assistant_output = get_response_multi(messages).choices[0].message.content
        # 将大模型的回复信息添加到messages列表中
        messages.append({'role': 'assistant', 'content': assistant_output})
        print(f'用户输入：{user_input}')
        print(f'模型输出：{assistant_output}')
        print('\n')
def test_single():
    get_response()

if __name__ == '__main__':
    #call_with_messages()
    test_single()
    #test_multi()
    