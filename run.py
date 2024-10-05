import os
import pandas as pd
import json
import lineagesrc.normalize as normalize
import lineagesrc.process as process
import lineagesrc.parser as parser
import lineagesrc.dataclass as dataclass
import lineagesrc.comment as comment
import lineagesrc.utils as utils
import llmodel.llmapi as llmapi
import llmodel.llmprompt as llmpmt
from tqdm import tqdm
import loginfo.mylogger as logger

logger = logger.MyLogger("aisqlline")
tqdm.pandas()

'''
step0 手动删除导出的excel中乱码，格式错乱的部分。目前比较难自动化，mysql的导出识别有问题。
'''

'''
第一步主要目的是excel内的sql代码从json中提取出来。进行基础的格式化，对\\n,\\t等内容进行标准替换。
存在部分格式化错误的问题，目前难以结局
todo： 解决 tab 制表符缺失，格式比较混乱的问题。
'''

def step1_trans_sql_code(file_path, output_dir,OVERWRITE=False):

    error_count = 0
    update_count = 0
    loaded_count = 0
    unsql_count = 0
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)

    df1 = pd.read_excel(file_path)
    for i in tqdm(df1.itertuples(),total=len(df1)):
    #for i in df1.itertuples():
        try:
            #print(f"{i[0]}/{len(df1)}") # debug
            save_sub_dir = os.path.join(output_dir,str(i[1]))
            if os.path.exists(save_sub_dir) == False:
                os.makedirs(save_sub_dir)

            save_sql_name = f"{i[1]}-{int(i[7])}.sql"
            # if "2015年5月新增日累计指标-206.sql" not in save_sql_name:
            #     continue 
            if os.path.exists(os.path.join(save_sub_dir,save_sql_name)) and not OVERWRITE: #文件存在直接跳过
                loaded_count+=1
                continue
                
            if not process.check_has_json(i[10]):# 不存在json内容直接跳过
                unsql_count+=1
                continue
            
            result_sql = process.get_sql_str_from_column(i[10])
            if result_sql == "":  #sql里没有双引号" 直接走标准sql解析
                json_obj = json.loads(i[10])
            else: #sql里存在双引号,先做预处理和替换
                json_obj = process.format_sql_line(i[10],result_sql)
            
            
            sql_node = dataclass.SQLNodes(json_obj, i[7], i[8], i[9], i[1])
            if sql_node.is_sql_node:
                sql_code_str = sql_node.sql                
                process.get_sql_format(sql_code_str,save_sql_name,save_sub_dir)
                update_count+=1
            else:
                unsql_count+=1
            
        except Exception as e:
            error_count+=1
            logger.error(f"[{error_count}]-[index:{i[0]}]-[{i[1]}]-[{i[7]}]-[{e}]:{i[10]} ")
    logger.info(f"unsql/total:{unsql_count}/{len(df1)} | loaded:{loaded_count}-update:{update_count}-error:{error_count}")

'''
这一步主要为了把不同表的注释内容取消，避免后续格式化处理，代码和注释混淆，同时避免部分大模型对中文识别差
'''
def step2_sql_postprocess(load_dir,output_dir,OVERWRITE=True,APPEND_JSON=True):
    '''
    todo: 2012年12月新增指标-25.sql 里面有的/**/是代码注释，有的是字段注释，很难全部弄清楚。
    APPEND_JSON 是否将注释内容追击到存在的文件里。True表示试图里存一个！
    '''
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)
    for root, dirs, files in os.walk(load_dir):
        for sub_dir in tqdm(dirs):
            sub_dir_path = os.path.join(output_dir,sub_dir)
            load_sub_dir = os.path.join(load_dir,sub_dir)
            if os.path.exists(sub_dir_path) == False:
                os.makedirs(sub_dir_path)
            filelist = os.listdir(load_sub_dir)
            comment_file_path = os.path.join(sub_dir_path,f"{sub_dir}.json")
            if os.path.exists(comment_file_path) == False or APPEND_JSON == False:
                comment_dict = {"delete_comment":{},"feature_comment":{}}
                
            else:
                comment_dict = comment.load_comment_file(comment_file_path)
            
            for file in filelist:
                # if "2021年7月新增个人日累计指标-140.sql" not in file:
                #     continue

                if file.endswith(".sql"):
                    if os.path.exists(os.path.join(sub_dir_path,file)) and not OVERWRITE: #文件存在直接跳过
                        continue
                    with open(os.path.join(load_sub_dir,file), 'r', encoding='utf-8') as f:
                        sql_code_str = f.read()

                    result,delete_comments,new_sql = comment.extract_name_and_comment_from_sql(sql_code_str)
                    comment_dict = comment.update_comment(comment_dict,result,delete_comments)
                    #new_sql = comment.delete_comment(sql_code_str,result,delete_comments)
                    with open(os.path.join(sub_dir_path,file), 'w', encoding='utf-8') as f:
                        f.writelines(new_sql)
            comment.save_comment_dict_file(comment_dict,comment_file_path)


@utils.deprecated
def step3_sql_split_multi_feature_v1(load_dir,output_dir,excel_file,OVERWRITE=True):
    '''
    直接拆分出多个代码片段，每个代码片段都是一个指标的相关代码，避免输出过多，大模型无法有效处理
    可以直接从excel表中获取关键excel里的每个表的字段，逐渐找
    '''
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)
        
    df = pd.read_excel(excel_file,sheet_name='模型信息')
    for root, dirs, files in os.walk(load_dir):
        for sub_dir in tqdm(dirs):
            sub_dir_path = os.path.join(output_dir,sub_dir)
            load_sub_dir = os.path.join(load_dir,sub_dir)
            if os.path.exists(sub_dir_path) == False:
                os.makedirs(sub_dir_path)
            filelist = os.listdir(load_sub_dir)
            for file in filelist:
                if file.endswith(".sql"):
                    if os.path.exists(os.path.join(sub_dir_path,file)) and not OVERWRITE: #文件存在直接跳过
                        continue
                    with open(os.path.join(load_sub_dir,file), 'r', encoding='utf-8') as f:
                        sql_code_str = f.read()
                    new_sql = normalize.split_except_function_multi(sql_code_str)
                    with open(os.path.join(sub_dir_path,file), 'w', encoding='utf-8') as f:
                        f.writelines(new_sql)


def get_client(model_name):
    if "qwen" in model_name:
        API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
        PLATFORM = "qwen".upper()
        model_name = model_name #要求把sql内容放在system里
        client = llmapi.init_client(API_KEY,PLATFORM)
    elif "genimi" in model_name:
        API_KEY = "AIzaSyA1JOXcA0B-sXcMli2926VsgMQfkh6BKtI"
    return client

def step3_sql_json(load_dir,output_dir,model_name='qwen-max-latest',PREFIX_LIST=['stop','META'], PROMPT_TYPE='field',OVERWRITE=True):
    '''
    PROMPT_TYPE: 用于存储文件后缀(suffix)，以及选择不同的提示词模板类别
    PREFIX: 文件前缀，用于记录文件是否为正常完成的内容。stop是默认大模型返回的标准结束结果。也用于检查文件是否存在，是否需要重新生成
    '''
    
    
    sql_client = get_client(model_name)
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)
    all_count = 0
    error_count = 0
    finish_count = 0
    loaded_count = 0
    unfinish_count = 0
    for root, dirs, files in os.walk(load_dir):
        for sub_dir in tqdm(dirs):
            sub_dir_path = os.path.join(output_dir,sub_dir)
            load_sub_dir = os.path.join(load_dir,sub_dir)
            if os.path.exists(sub_dir_path) == False:
                os.makedirs(sub_dir_path)
            filelist = os.listdir(load_sub_dir)
            for file in filelist:
                if not file.endswith(".sql"):
                    continue 
                all_count+=1
                sql_file_name = os.path.splitext(file)[0]
                sql_file = os.path.join(load_sub_dir,file)
                #save_file_name = os.path.join(output_dir, f"[{PREFIX}]_[{sql_file_name}]_[{PROMPT_TYPE}].json")
                if OVERWRITE==False and process.check_llm_answer_json(sub_dir_path, sql_file_name,suffix=PROMPT_TYPE, PREFIX_LIST=PREFIX_LIST):
                    loaded_count+=1
                    continue
                # try:
                json_dict, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmpmt.get_answer_json(sql_client,model_name,sql_file,PROMPT_TYPE='field')

                sql_relation_file_name = os.path.join(sub_dir_path, f"[{finish_reason}]_[{sql_file_name}]_[{PROMPT_TYPE}].json")
                with open(sql_relation_file_name, 'w', encoding='utf-8') as f:
                    json.dump(json_dict, f, ensure_ascii=False, indent=4)
                if finish_reason == "stop":
                    finish_count+=1    
                else:
                    unfinish_count+=1 
                logger.info(f"[{finish_reason}]-[{sql_file_name}<{PROMPT_TYPE}>.json]-[completion_tokens:{completion_tokens},prompt_tokens:{prompt_tokens},total_tokens:{total_tokens}] ")
                # except Exception as e:
                #     error_count+=1
                #     print(f"Error processing file:[{error_count}]- [{sql_file_name}<{PROMPT_TYPE}>.json]: {e}")
    logger.info(f"total:{all_count} | finish_count:{finish_count}, unfinish_count:{unfinish_count}, loaded_count:{loaded_count}, error_count:{error_count}")
if __name__ == "__main__":
    ROOT_PATH = "F:\GITClone\CMCCtest\sql-lineage\llm-datalineage"
    
    file1 = f"{ROOT_PATH}\\data\\自助sql代码格式清理-p1.xlsx"
    step1_output_dir = f"{ROOT_PATH}\\data_trans\\step1\\"
    #step1_trans_sql_code(file1, step1_output_dir,OVERWRITE=True)
    
    
    step2_output_dir = f"{ROOT_PATH}\\data_trans\\step2\\"
    #step2_sql_postprocess(step1_output_dir, step2_output_dir,OVERWRITE=True, APPEND_JSON=True)
    
    
    #excel_file = f"{ROOT_PATH}\\data\\dataos自助相关程序配置信息 (1)(1).xlsx"
    # step3_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step3\\"
    # step3_sql_split_multi_feature(step2_output_dir, step3_output_dir,excel_file, OVERWRITE=True)
    
    
    step3_output_dir = f"{ROOT_PATH}\\data_trans\\step3\\"
    step3_sql_json(step2_output_dir, step3_output_dir,OVERWRITE=False)
    #process.test2()