import os
import pandas as pd
import json
import lineagesrc.normalize as normalize
import lineagesrc.process as process
import lineagesrc.parser as parser
import lineagesrc.dataclass as dataclass
import lineagesrc.comment as comment
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
            # if "2012年12月新增指标-143.sql" not in save_sql_name:
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



def step3_sql_split_multi_feature(load_dir,output_dir,OVERWRITE=True):
    '''
    直接拆分出多个代码片段，每个代码片段都是一个指标的相关代码，避免输出过多，大模型无法有效处理
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
            for file in filelist:
                if file.endswith(".sql"):
                    if os.path.exists(os.path.join(sub_dir_path,file)) and not OVERWRITE: #文件存在直接跳过
                        continue
                    with open(os.path.join(load_sub_dir,file), 'r', encoding='utf-8') as f:
                        sql_code_str = f.read()
                    new_sql = normalize.split_except_function_multi(sql_code_str)
                    with open(os.path.join(sub_dir_path,file), 'w', encoding='utf-8') as f:
                        f.writelines(new_sql)

if __name__ == "__main__":
    file1 = "F:\\GITClone\\CMCCtest\\dateline\\data\\自助sql代码格式清理-p1.xlsx"
    step1_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step1\\"
    #step1_trans_sql_code(file1, step1_output_dir)
    
    
    step2_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step2\\"
    #step2_sql_postprocess(step1_output_dir, step2_output_dir,OVERWRITE=True, APPEND_JSON=False)
    
    
    step3_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step3\\"
    step3_sql_split_multi_feature(step2_output_dir, step3_output_dir,OVERWRITE=True)