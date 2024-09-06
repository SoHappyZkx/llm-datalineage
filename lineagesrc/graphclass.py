import re
class GraphSQL():
    def __init__(self, key_name, field_list):
        self.key_name = key_name
        self.db_name = ''
        self.var = []
        self.parse_var()
        self.field_list = field_list
    
    def parse_var(self):
        '''
        tmb_tablename
        dbname.${table_name.name1}
        tmpname_${dayid}
        dbname.table_${dayid}
        '''
        segs = self.key_name.split(".")
        if len(segs) == 1:
            _table_name = segs[0]
            self.table_name = _table_name
        else:
            self.db_name = segs[0]
            _table_name = ".".join(segs[1:])
            #debug
            if "${" in self.db_name:
                print("error db_name", self.db_name)
                
            if "${" in _table_name:
                s_ = _table_name.find("${")
                e_ = _table_name.find("}")
                _var = _table_name[s_+2 : e_]
                _segs = _var.split(".")
                self.var.extend(_segs)
                self.table_name = _segs[0]
        
            
 

            
        
        
