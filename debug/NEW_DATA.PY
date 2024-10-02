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
            
            if str(i[1])!="2015年5月新增日累计指标" or int(i[7])!=206:
                continue
            
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