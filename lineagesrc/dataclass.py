
'''
用于保存所有sql节点里的属性值，有的可能只是基本变量，有的可能是带有sql代码的处理节点。
每一个SQLNodes都具有前后指向节点的id。
'''
class SQLNodes:  
    def __init__(self, data,cur_node,last_node,next_node,table_name):  
        for key, value in data.items():  
            setattr(self, key, value)
        self.cur = cur_node
        self.last = last_node
        self.next = next_node
        self.table_name = table_name
        
    @property
    def is_sql_node(self):
        return hasattr(self, 'sql')

'''
可以保存tables和内部的所有fileds 这是从excel表格里读出来的，不是直接获取的具体内容
'''
class SQLTables:
    def __init__(self, table_name,prod_name):
        '''
        prod_name 是中文名
        table_name 是英文名
        一般字段内的结果table_name 会比sql代码表里的少一些前缀。 
        比如月调度程序：DM_PUB_CHANNEL_020507_YYYYMM -》 SA_D_DIAO_DM_PUB_CHANNEL_020507_YYYYMM
        比如月表：  DM_PUB_COMPETITOR_YYYYMM  -》 SA_M_DM_PUB_COMPETITOR_YYYYMM  -》
        FOUND_SQL 用于判断是否找到了匹配的sql代码
        SCHEDULE_TABLE 用于判断是否是diaodu类程序，diaodu类理论上不重要？ 自助没有相关字段？
        PERIODIC  是月表还是日表
        '''
        self.table_name = table_name
        self.prod_name = prod_name
        self.sql_table_name = ''
        self.sql_prod_name = ''
        self.PERIODIC = ''
        self.FOUND_SQL = False
        self.FOUND_SCHEMA = False
        self.SCHEDULE_TABLE = False
        self.STATE = ''
        self.field_dict = {}
    
    def add(self,field_name,field_description):
        if field_name not in self.field_dict.keys():
            self.field_dict[field_name] = SQLField(field_name,field_description)
    def parse(self,new_table_name):
        '''
        TODO 还有很多表不是DM_这个结构，需要对应下试试
        但目前看，只有DIAO的才是调度视图，才能保证有M,或者D
        '''
        if "DIAO" in new_table_name:
            self.SCHEDULE_TABLE =True #DIAO是充分必要条件！
            segs = new_table_name.split('_')
            self.PERIODIC = segs[1]
        elif "_D_" in new_table_name:
            self.PERIODIC = 'D'
        elif "_M_" in new_table_name:
            self.PERIODIC = 'M'
    
        
class SQLGraph:
    def __init__(self,data):
        return
    

class SQLField:
    def __init__(self,field_name,field_description):
        self.name = field_name
        self.desc = field_name
        self.lineage = {}
    def __str__(self):
        return f"name:{self.name}, description:{self.desc}"