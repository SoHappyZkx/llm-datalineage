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
def load_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_code_str = f.read()
    return sql_code_str


'''
第一步主要目的是excel内的sql代码从json中提取出来。进行基础的格式化，对\\n,\\t等内容进行标准替换。
存在部分格式化错误的问题，目前难以结局
todo： 解决 tab 制表符缺失，格式比较混乱的问题。
'''
def step1_trans_sql_code(file_path, output_dir,save_path,OVERWRITE=False):

    error_count = 0
    update_count = 0
    loaded_count = 0
    unsql_count = 0
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)

    df1 = pd.read_excel(file_path)
    new_sql_list = []
    for i in tqdm(df1.itertuples(),total=len(df1)):
    #for i in df1.itertuples():
        try:
            #print(f"{i[0]}/{len(df1)}") # debug
            load_sub_dir = os.path.join(output_dir,str(i[1]))
            load_file_name = f"{i[1]}-{int(i[7])}.sql"
            load_file_path = os.path.join(load_sub_dir,load_file_name)
                
            if not process.check_has_json(i[10]):# 不存在json内容直接跳过
                unsql_count+=1
                new_sql_list.append('')
                continue
            
            result_sql = process.get_sql_str_from_column(i[10])
            if result_sql == "":  #sql里没有双引号" 直接走标准sql解析
                json_obj = json.loads(i[10])
            else: #sql里存在双引号,先做预处理和替换
                json_obj = process.format_sql_line(i[10],result_sql)
            
            
            sql_node = dataclass.SQLNodes(json_obj, i[7], i[8], i[9], i[1])
            if sql_node.is_sql_node:
                
                sql_code = load_sql_file(load_file_path)
                json_obj['sql'] = sql_code
                new_sql_list.append(json.dumps(json_obj,ensure_ascii=False))
                update_count+=1
            else:
                new_sql_list.append(json.dumps(json_obj,ensure_ascii=False))
                unsql_count+=1
            
        except Exception as e:
            error_count+=1
            logger.error(f"[{error_count}]-[index:{i[0]}]-[{i[1]}]-[{i[7]}]-[{e}]:{i[10]} ")
    nqdf= pd.DataFrame(new_sql_list)
    assert(len(nqdf) == len(df1['步骤配置信息']))
    df1['步骤配置信息'] = nqdf
    df1.to_excel(save_path,index=False)
    logger.info(f"unsql/total:{unsql_count}/{len(df1)} | loaded:{loaded_count}-update:{update_count}-error:{error_count}")


def select_table(sql_code_file, all_excel_file, select_list):
    select_list = ['订单视图月表','宽带信息月视图','个人日视图数据','产品订购日程序']
    df_all = pd.read_excel(all_excel_file)
    df_sql = pd.read_excel(sql_code_file)
    
    
    table_list = parser.get_table_list(sql_code_str)
    return table_list

if __name__ == "__main__":
    file1 = "F:\\GITClone\\CMCCtest\\dateline\\data\\自助sql代码格式清理-p1.xlsx"
    step1_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step1\\"
    step2_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step2\\"
    save_path = "F:\\GITClone\\CMCCtest\\dateline\\data\\自助sql代码格式清理-去注释.xlsx"
    step1_trans_sql_code(file1, step2_output_dir,save_path)
    #step2_sql_postprocess(step1_output_dir, step2_output_dir,OVERWRITE=True, APPEND_JSON=False)
    
    
    # step3_output_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step3\\"
    # step3_sql_split_multi_feature(step2_output_dir, step3_output_dir,OVERWRITE=True)