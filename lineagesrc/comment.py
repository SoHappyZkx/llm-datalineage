
import re
import json
from .sqlfunction import * 
from typing import Tuple
def extract_name_and_comment_from_sql(sql:str) -> Tuple[list[str,str],list[str]] :  
    """  
    从SQL字符串中提取每行注释以及注释前的列名字。  
    注意 DROP TABLE tmp_dm_20130916_06; \
        这里的换行符会被识别成 \\ 所以可以增加一步replace \\ -》 \n
    
    """  
    def new_sql_line(new_sql_list, str_):
        if str_.strip() == "":
            pass
        elif str_.strip() == ",": #只有一个逗号就拼回去
            new_sql_list[-1] += ","
        else:
            new_sql_list.append(str_)
        return new_sql_list
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
    new_sql = []
    for line in lines:
        # if "当月ARPU（" not in line:
        #     continue
        # 处理行注释  
        comment_match = line_comment_pattern.search(line)  
        if comment_match:  
            comment = comment_match.group(0).strip()  
            pre_comment_line = line[:comment_match.start()]
            pre_comment_part = pre_comment_line.rstrip(', ')
            new_sql_line(new_sql,pre_comment_line)
            words = split_except_function_multi(pre_comment_part,3)  
            if words:  
                # 处理针对 AS 的情况  
                name = 'UNKNOWN'  
                for word in reversed(words):  
                    res_ = get_feature_name_from_function(word)
                    if not res_ : #继续往前找
                        continue
                    elif res_ == "UNKNOWN":
                        print(f"[WARNING]@<Comment-function>: unknown renamed function: {word} ")
                        break
                    else:  
                        name = res_  
                        break
            else:  
                name = ''  
            results.append((name, comment))  
        else:
            new_sql_line(new_sql,line)
    new_sql_all = '\n'.join(new_sql)
    return results,comments,new_sql_all

def __extract_block_comment(match, comments):  
    """  
    从块中提取注释内容  
    """  
    comment = match.group(0)  
    comments.append(comment)  
    return ''  # 以便块注释被整个去除  


def load_comment_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:  
        comment_dict = json.load(file) 
    for k in comment_dict['feature_comment'].keys():
        comment_dict['feature_comment'][k] = set(comment_dict['feature_comment'][k])
    return comment_dict

def update_comment(comment_dict,comment_result,delete_comment):
    for comment_ in delete_comment:
        if comment_ not in comment_dict['delete_comment'].keys():
            comment_dict['delete_comment'][comment_]=0
        comment_dict['delete_comment'][comment_]+=1
        
    for name, comment in comment_result:
        comment_ = comment.replace("-",'').replace("#",'').lower().strip()
        if comment_ not in comment_dict['feature_comment'].keys():
            comment_dict['feature_comment'][comment_]=set()
        comment_dict['feature_comment'][comment_].add(name)
    return comment_dict

def delete_comment(sql_str, comment_result,delete_comment):
    for k in delete_comment:
        sql_str = sql_str.replace(k,'')
        
    for name, comment in comment_result:
        sql_str = sql_str.replace(comment,'')
    return sql_str
    
def save_comment_dict_file(comment_dict,filepath):
    for k in comment_dict['feature_comment'].keys():
        comment_dict['feature_comment'][k] = list(comment_dict['feature_comment'][k])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(comment_dict,ensure_ascii=False))

# def test1():
#     sql = "updare sar, asdas, asdad --tessrasd asdasdasdasda  asdasd,  --adasdasdasd, #asdasdasda "
#     extract_name_and_comment_from_sql(sql)
# test1()