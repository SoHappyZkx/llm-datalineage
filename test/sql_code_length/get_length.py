import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from tqdm import tqdm


def test():
    load_dir = "F:\\GITClone\\CMCCtest\\dateline\\data_trans\\step2"
    file_list = []
    len_list = []

    for root, dirs, files in os.walk(load_dir):
        for sub_dir in tqdm(dirs):
            load_sub_dir = os.path.join(load_dir,sub_dir)
            filelist = os.listdir(load_sub_dir)
            for file in filelist:
                if file.endswith(".sql"):
                    with open(os.path.join(load_sub_dir,file), 'r', encoding='utf-8') as f:
                        sql_code_str = f.read()
                    code_len = len(sql_code_str)
                    line_count = sql_code_str.count('\n')
                    file_list.append(file)
                    len_list.append(code_len)
    #倒序排序
    sorted_index = sorted(range(len(len_list)), key=lambda k: len_list[k], reverse=True)
    for i in sorted_index:
        print(file_list[i],len_list[i])
    with open("./sql_code_length_static.log",'w',encoding='utf-8') as f:
        for i in sorted_index:
            f.write(file_list[i] + " " + str(len_list[i]) + "\n")
        
test()