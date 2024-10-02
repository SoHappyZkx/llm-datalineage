import os
import json
#from . import normalize
import pandas as pd
#from . import dataclass
import normalize
import dataclass
import pickle
'''
检查是否为空的，无字符的，没有key的内容
'''
def check_has_json(str_):
    if pd.isna(str_):
        return False
    if len(str_) == 0:
        return False
    if str_ == "\{\}":
        return False
    return True

def get_sql_format(sql_code_str,sql_name,output_dir):
    new_sql = normalize.format_sql(sql_code_str)
    with open(os.path.join(output_dir,sql_name), 'w', encoding='utf-8') as f:  
        f.writelines(new_sql)
 
def format_sql_line(all_str,sql_result):
    rest_str = all_str.replace(sql_result,'')
    new_sql_result = sql_result.replace('\\"','')
    new_sql_result = new_sql_result.replace("\\\\n","\n")
    new_sql_result = new_sql_result.replace("\\\\t","\t")
    json_res = json.loads(rest_str)
    json_res['sql'] = new_sql_result
    return json_res
       
'''
部分场景sql代码里也存在""双引号，导致json解析出错，所以需要找到sql代码的位置
'''
def get_sql_str_from_column(all_str):
    '''
    可能存在最后一个不是sql字段，是别的字段。需要处理一下。
    '''
    #找到第一个带有 \"sql\":\" 这个字符串的的位置，然后找到最后出现 \" 的位置
    start = all_str.find('\"sql\":\"')
    end = all_str.rfind('\"parentDsName\":')
    
    if start>0: #存在 "sql":"
        if end >0 and end > start:
            sql_str = all_str[start+7:end-2]
        else:
            end = all_str.rfind('\"')
            sql_str = all_str[start+7:end]
    else:
        sql_str = ''
    return sql_str
    

def get_table_schema(df2):
    '''
    sheet2的内容优先注册，此部门不存在其他无意义调度，都是实际使用字段，
    sheet2都是schema数据，所以found_schema = True
    tablename是最段纯净名
    prodname可能有冗余
    '''
    table_obj_dict = {}
    for row in df2.itertuples():
        if row[2] not in table_obj_dict.keys():
            table_obj = dataclass.SQLTables(row[1].upper(),row[2])
            table_obj.FOUND_SCHEMA=True
            table_obj_dict[row[2]] = table_obj
        else:
            table_obj_dict[row[2]].add(row[4].upper(),row[5])
    return table_obj_dict

def get_paired_table(df1,table_obj_dict):
    def _get_all_table_name_dict(table_obj_dict):
        '''获取程序英文名为key的字典'''
        table_name_dict = {}
        for key in table_obj_dict.keys():
            table_obj = table_obj_dict[key]
            if table_obj.table_name not in table_name_dict.keys():
                table_name_dict[table_obj.table_name] = table_obj
        return table_name_dict 
    def _check_in_table_name_dict(key_list,str_):
        '''
        检查str_是哪个key的全集，主要看的是sheet2的英文表名是否是sheet1的英文表名的子字符串
        但注意，不能用in 要用endwith，存在两个特殊情况
        sheet2: 
        对端号码视图, dm_pub_call_info_yyyymm
        sheet1:
        对端号码视图 : SA_M_DM_PUB_CALL_INFO_YYYYMM
        对端号码日视图 : SA_M_DM_PUB_CALL_INFO_YYYYMMDD
        
        
        sheet2:
        出账信息月视图：DM_PUB_ACCT_SHOULDITEM_YYYYMM
        
        sheet1:
        出账信息日视图  SA_M_DM_PUB_ACCT_SHOULDITEM_YYYYMMDD
        出账信息月视图  SA_M_DM_PUB_ACCT_SHOULDITEM_YYYYMM
        
        这个如果使用in逻辑判断，那么也会在对端号码日视图里，这样的逻辑是错误的。
        
        '''
        for key in key_list:
            if str_.endswith(key):
                return key
        return None
    def _check_in_prod_name_dict(key_list,str_):
        '''
        主要检查sheet1的中文名是否是在sheet2的中文名里的子字符串：
        如 反诈基础信息日视图  in 反诈基础信息日视图-结果表
        但 SA_D_DM_PUB_FANZHA_USER_YYYYMMDD   not   in DM_PUB_FANZHA_USER_DS_YYYYMMDD
        '''
        for key in key_list:
            if str_ in key:
                return key
        return None

    def _check_is_diao(sql_table_name,sql_prod_name):
        if "调度" not in sql_prod_name and "DIAO" not in sql_table_name:
            return False
        else:
            return True
    def _update_obj(table_obj, row, STATE_CODE):
        '''
        row是sheet1的内容，sql表
        '''
        #匹配到了正确的结果,AB都有
        if STATE_CODE==1: 
            table_obj.parse(row[4].upper())
            table_obj.STATE = row[3].upper()
            table_obj.FOUND_SQL = True
            table_obj.sql_table_name = row[4].upper()
            table_obj.sql_prod_name = row[1]
        #直接从头新建个进行修改:A独有
        elif STATE_CODE==2:
            table_obj.parse(row[4].upper())
            table_obj.sql_table_name = row[4].upper()
            table_obj.sql_prod_name = row[1]
            table_obj.table_name = ''
            table_obj.prod_name = ''
            table_obj.STATE = row[3].upper()
            table_obj.FOUND_SQL = True
            table_obj.FOUND_SCHEMA=False

        # B独有的内容，不需要更新其他的 比如：DM_PUB_PESN_REALNAME_BASE_DM_YYYMMDD，DM_PRODUCT_OFFER_DS_YYYYMMDD,
        # !SHEET1: SA_D_DM_PUB_FANZHA_USER_YYYYMMDD   SHEET2: DM_PUB_FANZHA_USER_DS_YYYYMMDD, 
        else: 
            return 
           
    _processed_dict = {}    
    begin_prod_name_key_list = list(table_obj_dict.keys())
    table_name_dict = _get_all_table_name_dict(table_obj_dict)
    table_name_key_list = list(table_name_dict.keys())
    
    for row in df1.itertuples():
        if row[1] in _processed_dict.keys():
            continue
        '''
        1.中文直接匹配的
        2.英文表2是表1的子字符串的
            1）看表1里的
            2）表1里的是带DIAO的
        '''
        if row[1] in table_obj_dict.keys():
            ''' 一般场景，中文表名可以直接匹配上的'''
            # if not table_obj_dict[row[1]].FOUND_SQL: 
            _update_obj(table_obj_dict[row[1]],row,STATE_CODE=1)
            _processed_dict[row[1]] = True

        elif  _check_is_diao(row[4].upper(),row[1]):
            '''
            如果带DIAO，一定是sheet1独有的，直接新建就行了
            
            '''
            table_obj_dict[row[1]] = dataclass.SQLTables(row[4].upper(),row[1])
            _update_obj(table_obj_dict[row[1]],row,STATE_CODE=2)
            _processed_dict[row[1]] = True
        else:
            '''
                中文有时候匹配不上，可以尝试应为名，sheet2里的应为名为子字符串，
                匹配是否在sheet1里的英文表keys_list
            '''
            res_en_name = _check_in_table_name_dict(table_name_key_list,row[4].upper()) # 把sheet1的英文程序名和所有sheet2英文表明匹配
            
            if res_en_name: #匹配上了，且不是调度程序，因为diao已经在前面被过滤了，剩下的sa_table_name 如果能匹配上，一定没问题
                _update_obj(table_name_dict[res_en_name],row,STATE_CODE=1)  #更新被找到的obj
            else:
                res_cn_name = _check_in_prod_name_dict(begin_prod_name_key_list,row[1]) # 把sheet1的中文程序名和所有sheet2中文表明匹配
                if res_cn_name: #匹配上了部分中文的内容
                    _update_obj(table_obj_dict[res_cn_name],row,STATE_CODE=1)
                else: #什么都没匹配上是新的。
                    table_obj_dict[row[1]] = dataclass.SQLTables(row[4].upper(),row[1])
                    _update_obj(table_obj_dict[row[1]],row,STATE_CODE=2)
            _processed_dict[row[1]] = True    
    return 

def save_obj_dicts(filepath, obj_dict):
    with open(filepath, 'wb') as f:
        pickle.dump(obj_dict, f)  
def load_obj_dicts(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def _debug_get_paired_table(df1,table_obj_dict):
    def _get_all_table_name_dict(table_obj_dict):
        '''获取程序英文名为key的字典'''
        table_name_dict = {}
        for key in table_obj_dict.keys():
            table_obj = table_obj_dict[key]
            if table_obj.table_name not in table_name_dict.keys():
                table_name_dict[table_obj.table_name] = table_obj
        return table_name_dict 
    def _check_in_table_name_dict(key_list,str_):
        '''
        检查str_是哪个key的全集，主要看的是sheet2的英文表名是否是sheet1的英文表名的子字符串
        但注意，不能用in 要用endwith，存在两个特殊情况
        sheet2: 
        对端号码视图, dm_pub_call_info_yyyymm
        sheet1:
        对端号码视图 : SA_M_DM_PUB_CALL_INFO_YYYYMM
        对端号码日视图 : SA_M_DM_PUB_CALL_INFO_YYYYMMDD
        
        
        sheet2:
        出账信息月视图：DM_PUB_ACCT_SHOULDITEM_YYYYMM
        
        sheet1:
        出账信息日视图  SA_M_DM_PUB_ACCT_SHOULDITEM_YYYYMMDD
        出账信息月视图  SA_M_DM_PUB_ACCT_SHOULDITEM_YYYYMM
        
        这个如果使用in逻辑判断，那么也会在对端号码日视图里，这样的逻辑是错误的。
        
        '''
        for key in key_list:
            if str_.endswith(key):
                return key
        return None
    def _check_in_prod_name_dict(key_list,str_):
        '''
        主要检查sheet1的中文名是否是在sheet2的中文名里的子字符串：
        如 反诈基础信息日视图  in 反诈基础信息日视图-结果表
        但 SA_D_DM_PUB_FANZHA_USER_YYYYMMDD   not   in DM_PUB_FANZHA_USER_DS_YYYYMMDD
        '''
        for key in key_list:
            if str_ in key:
                return key
        return None

    def _check_is_diao(sql_table_name,sql_prod_name):
        if "调度" not in sql_prod_name and "DIAO" not in sql_table_name:
            return False
        else:
            return True
    def _update_obj(table_obj, row, STATE_CODE):
        '''
        row是sheet1的内容，sql表
        '''
        #匹配到了正确的结果,AB都有
        if STATE_CODE==1: 
            table_obj.parse(row[4].upper())
            table_obj.STATE = row[3].upper()
            table_obj.FOUND_SQL = True
            table_obj.sql_table_name = row[4].upper()
            table_obj.sql_prod_name = row[1]
        #直接从头新建个进行修改:A独有
        elif STATE_CODE==2:
            table_obj.parse(row[4].upper())
            table_obj.sql_table_name = row[4].upper()
            table_obj.sql_prod_name = row[1]
            table_obj.table_name = ''
            table_obj.prod_name = ''
            table_obj.STATE = row[3].upper()
            table_obj.FOUND_SQL = True
            table_obj.FOUND_SCHEMA=False

        # B独有的内容，不需要更新其他的 比如：DM_PUB_PESN_REALNAME_BASE_DM_YYYMMDD，DM_PRODUCT_OFFER_DS_YYYYMMDD,
        # !SHEET1: SA_D_DM_PUB_FANZHA_USER_YYYYMMDD   SHEET2: DM_PUB_FANZHA_USER_DS_YYYYMMDD, 
        else: 
            return 
           
    _processed_dict = {}    
    begin_prod_name_key_list = list(table_obj_dict.keys())
    table_name_dict = _get_all_table_name_dict(table_obj_dict)
    table_name_key_list = list(table_name_dict.keys())
    
    _pair_count = 0
    _diao_new_count = 0
    _mh_table_name_pair_count = 0
    _mh_prod_name_pair_count = 0
    _unpair_count = 0 
    _paired_list = []
    for row in df1.itertuples():
        if "对端号码视图" in row[1]:
           print('stop') 
        if row[1] in _processed_dict.keys():
            continue
        '''
        1.中文直接匹配的
        2.英文表2是表1的子字符串的
            1）看表1里的
            2）表1里的是带DIAO的
        '''
        if row[1] in table_obj_dict.keys():
            ''' 一般场景，中文表名可以直接匹配上的'''
            # if not table_obj_dict[row[1]].FOUND_SQL: 
            _update_obj(table_obj_dict[row[1]],row,STATE_CODE=1)
            _processed_dict[row[1]] = True
            _pair_count += 1
            _paired_list.append(row[1])
        elif  _check_is_diao(row[4].upper(),row[1]):
            '''
            如果带DIAO，一定是sheet1独有的，直接新建就行了
            
            '''
            table_obj_dict[row[1]] = dataclass.SQLTables(row[4].upper(),row[1])
            _update_obj(table_obj_dict[row[1]],row,STATE_CODE=2)
            _processed_dict[row[1]] = True
            _diao_new_count+=1
        else:
            '''
                中文有时候匹配不上，可以尝试应为名，sheet2里的应为名为子字符串，
                匹配是否在sheet1里的英文表keys_list
            '''
            res_en_name = _check_in_table_name_dict(table_name_key_list,row[4].upper()) # 把sheet1的英文程序名和所有sheet2英文表明匹配
            
            if res_en_name: #匹配上了，且不是调度程序，因为diao已经在前面被过滤了，剩下的sa_table_name 如果能匹配上，一定没问题
                _update_obj(table_name_dict[res_en_name],row,STATE_CODE=1)  #更新被找到的obj
                _mh_table_name_pair_count+=1
                _paired_list.append(table_name_dict[res_en_name].prod_name)
            else:
                res_cn_name = _check_in_prod_name_dict(begin_prod_name_key_list,row[1]) # 把sheet1的中文程序名和所有sheet2中文表明匹配
                if res_cn_name: #匹配上了部分中文的内容
                    _update_obj(table_obj_dict[res_cn_name],row,STATE_CODE=1)
                    _mh_prod_name_pair_count+=1
                    _paired_list.append(res_cn_name)
                else: #什么都没匹配上是新的。
                    table_obj_dict[row[1]] = dataclass.SQLTables(row[4].upper(),row[1])
                    _update_obj(table_obj_dict[row[1]],row,STATE_CODE=2)
                    _unpair_count+=1
            _processed_dict[row[1]] = True    
    print(len(_processed_dict.keys()))
    print(_pair_count,_diao_new_count,_mh_table_name_pair_count,_mh_prod_name_pair_count,_unpair_count)
    return _paired_list

def _debug_static_tables(table_obj_dict):
    M_table_count = 0
    D_table_count = 0
    unknown_count = 0
    DIAODU_table_count = 0
    ONLY_FOUND_SQL_COUNT = 0
    ONLY_FOUND_SCHEMA_COUNT = 0 
    BOTH_FOUND_COUNT = 0 
    BOTH_NOT_FOUND_COUNT=0
    all_count = len(table_obj_dict.keys())
    _both_paired_list = []
    for key in table_obj_dict.keys():
        table_obj = table_obj_dict[key]
        if table_obj.PERIODIC=='M':
            M_table_count+=1
        elif table_obj.PERIODIC=='D':
            D_table_count+=1
        else: #可能没匹配上，也没有DIAO这个调度关键字
            unknown_count+=1
    
        if table_obj.SCHEDULE_TABLE:
            DIAODU_table_count+=1
        
        if table_obj.FOUND_SQL and table_obj.FOUND_SCHEMA:
            BOTH_FOUND_COUNT+=1
            _both_paired_list.append(key)
        elif table_obj.FOUND_SQL and not table_obj.FOUND_SCHEMA:
            ONLY_FOUND_SQL_COUNT+=1
        elif not table_obj.FOUND_SQL and table_obj.FOUND_SCHEMA:
            ONLY_FOUND_SCHEMA_COUNT+=1
        else:
            BOTH_NOT_FOUND_COUNT+=1
            print(f"[NOT FOUND SQL] for {key}")
    print(f"M_table_count:{M_table_count}, D_table_count：{D_table_count}，DIAODU_table_count：{DIAODU_table_count}，")
    print(f"ONLY_FOUND_SQL_COUNT:{ONLY_FOUND_SQL_COUNT}， \
          ONLY_FOUND_SCHEMA_COUNT:{ONLY_FOUND_SCHEMA_COUNT}, \
          BOTH_FOUND_COUNT:{BOTH_FOUND_COUNT}, \
          BOTH_NOT_FOUND_COUNT:{BOTH_NOT_FOUND_COUNT}, \
          all_count：{all_count} ")
    return _both_paired_list
def test1():
    file1 = "F:\\GITClone\\CMCCtest\\dateline\\data\\dataos自助相关程序配置信息 (1)(1).xlsx"
    file2 = "F:\\GITClone\\CMCCtest\\dateline\\data\\自助数据字典(2).xlsx"
    test1 = "F:\\GITClone\\CMCCtest\\dateline\\test\\7.json"
    test1_trans = "F:\\GITClone\\CMCCtest\\dateline\\test\\7trans.sql"
    #df1 = pd.read_excel(file1)
    #df2 = pd.read_excel(file2)
    # with open(test1, 'r', encoding='utf-8') as file:  
    #     data = json.load(file)  
    # print(data)
    # new_sql = normalize.format_sql(data['sql'])
    # print(new_sql)
    # with open(test1_trans, 'w', encoding='utf-8') as f:  
    #     f.writelines(new_sql)

def test2():
    filepath = "F:\\GITClone\\CMCCtest\\sql-lineage\\llm-datalineage\\data\\自助sql代码格式清理-p1.xlsx"
    df1 = pd.read_excel(filepath,sheet_name='Sheet1')
    df2 = pd.read_excel(filepath,sheet_name='Sheet2')
    table_obj_dict = get_table_schema(df2)
    sheet2_count = len(table_obj_dict.keys())
    df1_dict = {}
    for row in df1.itertuples():
        if row[1] not in df1_dict:
            df1_dict[row[1]] = 0
        df1_dict[row[1]]+=1
    _paired_list = _debug_get_paired_table(df1, table_obj_dict)
    sheet1_count = len(table_obj_dict.keys()) - sheet2_count
    _both_paired_list = _debug_static_tables(table_obj_dict)
    print(f"sheet1 新增:{sheet1_count}, sheet2 共有：{sheet2_count}， sheet1本身:{len(df1_dict.keys())} -> sheet1和sheet2匹配:{len(df1_dict.keys()) - sheet1_count}")
    print(f"paired_list:{len(_paired_list)}, both_paired_list:{len(_both_paired_list)} | diff: {set(_paired_list).difference(set(_both_paired_list))}")

def test3():
    filepath = "F:\\GITClone\\CMCCtest\\sql-lineage\\llm-datalineage\\data\\自助sql代码格式清理-p1.xlsx"
    save_obj_path = "F:\\GITClone\\CMCCtest\\sql-lineage\\llm-datalineage\\data\\obj_test.pkl"
    df1 = pd.read_excel(filepath,sheet_name='Sheet1')
    df2 = pd.read_excel(filepath,sheet_name='Sheet2')
    table_obj_dict = get_table_schema(df2)
    get_paired_table(df1, table_obj_dict)
    save_obj_dicts(save_obj_path, table_obj_dict)
    new_dict = load_obj_dicts(save_obj_path)
    print(len(new_dict.keys()))
