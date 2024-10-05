
## 第一段
'''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
        1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3.NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5.TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1；
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
        6.WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1；
        其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
        7.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        8.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        9. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        10.OTHERS: 其它无法明确分类的请划分在这里.
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出。求不能有省略，完成呈现。
        '''

## 第二段
'''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出每个字段的四元组。要求有source_field, target_field, relationship, description。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。 
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
         1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3.NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5.TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1；
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
        6.WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1；
        其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
        7.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        8.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        9. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        10.OTHERS: 其它无法明确分类的请划分在这里.
        description直接记录了两个字段相关的源SQL代码
        如果一个source_field和target_field中间有多个关联关系，多个中间子查询或者临时表的结果，请将他们一一拆解开，以中间使用的临时表的名字命名，最终每一个四元组只描述两个直接相关的字段
        内容以json格式输出，要求不能有省略，完成呈现。
        具体代码如下:%s
        '''

## 第三段

你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该是一张表。以json格式输出。要求有source_table, target_table, source_field, target_table, relation_type, description.
        其中source_table和target_table是相关的具体表名，以database.table格式输出,如果没有database,那么就忽略。
        source_field和target_field是相关的具体字段名, 记录的是是两个表之间进行关联的字段。source_field就是source_table里的字段， target_field就是 target_table里的字段。
        relation_type分为如下几个类别。
        1.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        2. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        3.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        最后的description记录了relation相关的源sql代码
        内容以json格式输出，要求不能有省略，完成呈现
        具体sql代码如下