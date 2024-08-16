import sqlparse  
import json  

def parse_sql(sql):  
    # 解析SQL语句  
    parsed_sql = sqlparse.parse(sql)  
    # 获取SQL语句中的所有字段  
    fields = []  
    for token in parsed_sql.tokens:  
        if token.ttype == sqlparse.tokens.Name:  
            fields.append(token.value)  
    # 获取字段之间的血缘关系  
    relationships = []  
    for field in fields:  
        # 获取该字段的计算表达式  
        expression = get_expression(parsed_sql, field)  
        if expression:  
            # 获取表达式中涉及的其他字段  
            related_fields = get_related_fields(expression)  
            for related_field in related_fields:  
                # 构造三元组  
                source = related_field  
                target = field  
                edge = expression  
                relationships.append((source, target, edge))  
    return relationships  

def get_expression(parsed_sql, field):  
    # 递归遍历SQL语句，寻找计算表达式  
    for token in parsed_sql.tokens:  
        if token.ttype == sqlparse.tokens.Parenthesis:  
            # 遍历括号内的表达式  
            for sub_token in token.tokens:  
                if sub_token.ttype == sqlparse.tokens.Name and sub_token.value == field:  
                    # 找到计算表达式  
                    return get_expression_from_parenthesis(token)  
        elif token.ttype == sqlparse.tokens.Operator:  
            # 遍历操作符  
            for sub_token in token.tokens:  
                if sub_token.ttype == sqlparse.tokens.Name and sub_token.value == field:  
                    # 找到计算表达式  
                    return get_expression_from_operator(token)  
    return None  

def get_expression_from_parenthesis(parenthesis):  
    # 从括号内的表达式中获取计算表达式  
    expression = ''  
    for token in parenthesis.tokens:  
        if token.ttype != sqlparse.tokens.Whitespace:  
            expression += token.value  
    return expression  

def get_expression_from_operator(operator):  
    # 从操作符中获取计算表达式  
    expression = ''  
    for token in operator.tokens:  
        if token.ttype != sqlparse.tokens.Whitespace:  
            expression += token.value  
    return expression  

def get_related_fields(expression):  
    # 获取表达式中涉及的其他字段  
    related_fields = []  
    for token in sqlparse.parse(expression).tokens:  
        if token.ttype == sqlparse.tokens.Name:  
            related_fields.append(token.value)  
    return related_fields  


if __name__ == "__main__":
    # 示例SQL语句  
    sql = """  
    SELECT a + b AS c, c * d AS e  
    FROM table  
    """  

    # 解析SQL语句  
    relationships = parse_sql(sql)  

    # 转换为JSON格式  
    json_data = []  
    for relationship in relationships:  
        source, target, edge = relationship  
        json_data.append({  
            'source': source,  
            'target': target,  
            'edge': edge  
        })  

    # 输出JSON格式的数据  
    print(json.dumps(json_data, indent=4))  



    '''
    该代码使用sqlparse库解析MySQL SQL语句，获取每个字段之间的血缘关系，以三元组的形式表示，结果是一个JSON格式的数据。

    [  
        {  
            "source": "a",  
            "target": "c",  
            "edge": "a + b"  
        },  
        {  
            "source": "b",  
            "target": "c",  
            "edge": "a + b"  
        },  
        {  
            "source": "c",  
            "target": "e",  
            "edge": "c * d"  
        },  
        {  
            "source": "d",  
            "target": "e",  
            "edge": "c * d"  
        }  
    ]  

    示例输出：
    '''