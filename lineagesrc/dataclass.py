
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

class SQLTables:
    def __init__(self,data):
        return


class SQLGraph:
    def __init__(self,data):
        return