'''
目前看下来8.2,8.3效果比较好，能把事情说清楚，并且输出结果比较确定
使用gnimi1.5 pro 效果最好！
todo1. 使用8.2,8.3版本作为底子
使用9 join，与 3+1 版本作为补充，


'''

version2 = '''
        你是一个SQL代码专家，请你帮我直接从上述SQL代码中提取出所有出现的字段的四元组关系，以及所有出现的表关系( 包括了有命名的表，和没有命名的子查询表,对于子查询临时表，请以subquery_为前缀，根据代码重命名，保证能一一对应）。
        ## 表关系：
        要求任意两个相关的表，应该有source_table, target_table两个字段，描述两张表的名字，以database.table的格式输出，如果没有database就忽略。
        同时有一个list，有若干组关系字段记录。每组结构如下[source_field, target_table, relation_type, description].
        source_field和target_field是相关的具体字段名, 记录的是是两个表之间进行关联的字段。source_field就是source_table里的字段， target_field就是 target_table里的字段。
        relation_type分为如下几个类别。
        1.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
        其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
        2. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
        where, having, limit, offset, distinct 等都算在FILTER其中.
        3.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
        left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
        最后的description记录了relation相关的源sql代码。
        
        ## 四元组关系 
        要求记录所有出现的字段的关系。四元组结构如下[source_field, target_field, relationship, description]。 
        其中source_field和target_field是相关的具体字段名，以database.table.field格式输出,如果没有database,那么就忽略。如果是中间的子查询临时表，请以subquery_为前缀命名，保证和表关系里的子查询名字一一对应。
        relationship表示source_field和target_field的计算关系，有以下几个类别type:
        1.EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
        2.STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3.NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4.CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5.TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
        6.WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
        其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
        7.OTHERS: 其它无法明确分类的请划分在这里.
        description直接记录了两个字段相关的源SQL代码
        请注意四元组与表关系里，description的sql代码，尽可能准确分配，不要遗漏或者重复记录过多。保证能还原会源代码即可。
        最终按顺序分别输出表关系和四元组关系的json结果，且只输出json内容，完成呈现。
        具体代码如下
'''


version3 = '''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
要求任意两个相关的表，应该有source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略，
同时有一个list，记录与两张表形相关的若干个字段的关系。每组关系结构如下{source_field, target_field, relation_type, description}.
source_field和target_field是相关的具体字段名, 记录的是是两个表之间进行关联的字段。source_field就是source_table里的字段， target_field就是 target_table里的字段。
relation_type分为如下几个类别。
1.AGGREGATION:对字段进行了聚合操作，让整个表的行数发生了变化，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1;
其他的如count(),sum(),avg(),min(),max()等函数都算在其中。
2. FILTER: 表示一个表由另几个字段根据某些条件过滤得来。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
where, having, limit, offset, distinct 等都算在FILTER其中.
3.JOIN:两个表通过JOIN操作连接起来，新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
left join， inner join，full join，union，union all 等都算在JOIN。但**注意** 需要JOIN标注出具体是哪种。 比如 JOIN(LEFT) JOIN(UNION).
注意！这里的relation_type只记录了这三种会对target_table的行数，内容多少产生影响的关系。如果有其他字段内容的变换关系，请划分在OTHERS里面。
最后的description记录了relation相关的源sql代码。
内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系。
具体sql代码如下
'''

version4 = '''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
假如入table1 到 table2先进行了子查询，结果与table3 再关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。 
要求任意两个相关的表，应该有source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略，
GROUPBY,FILTER,JOIN,OTHER 四个属性，每个字段都是一种计算关系类别，使用一个list，记录与两张表形相关的若干个字段的计算关系类别。每组计算关系都有相同的结构如下{source_field, target_field, type_name, description}.
以下是四种计算关系的定义:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:记录其他的字段内容的变换关系，或者数值计算，条件映射，区间分段等，核心原则是只改变内容。typename的子分类如下:
    1)EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。
source_field和target_field是相关的具体字段名, 记录的是是两个表之间进行关联的字段。source_field就是source_table里的字段， target_field就是 target_table里的字段。
type_name 根据定义进行调整，最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
具体sql代码如下:
'''

version5='''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
##举例## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。 
任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, groupby:[],filter:[],join:[],other:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个代码逻辑里的执行顺序。如果第一步是两个表关联执行，那么order_num 应该都为1;
GROUPBY,FILTER,JOIN,OTHER 四个，每个字段都是一种[关联关系]，定义如下:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:记录其他的字段内容的变换关系，或者数值计算，条件映射，区间分段等，核心原则是只改变内容。typename的子分类如下:
    1)EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。
这四种[关联关系]每一个都是一个list，记录此计算类型下若干个字段关系。每组字段关系都有相同的结构如下{source_field, target_field, type_name, description}.
source_field和target_field是相关的具体字段名, 记录的是是两个表之间进行关联的字段。source_field就是source_table里的字段， target_field就是 target_table里的字段。
type_name 根据定义选择;
最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
具体sql代码如下:
'''
# VERSION5比较细致，但是会导致1. 很多中间字段没有识别到。2 可能过长了，冗余太多。尽量减少输出的长度消耗。


version6='''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。先执行的order_num应该比较低。如果第一步是两个表关联执行，那么order_num 应该都为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=2, table2->subquery_23 order_num=1, table3->subquery_23 order_num=1, subquery_23->table4 order_num=2 这四个关系。

relation是一个列表list,记录这两个表中使用的所有字段关系。每组字段关系都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。
type根据定义选择:GROUPBY,FILTER,JOIN,OTHER 四个,定义如下:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:前面三种都是对结果表的行数可能产生影响的，Other里只记录字段内容产生影响的关系，比如字符串改动，数值计算，条件映射，区间分段等，核心原则是只改变内容。以下是可能的子分类如下:
    1)EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。

最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
具体sql代码如下:
'''


version7='''
请你从下面提供的SQL代码中，抽取所有不同表之间的关系，包括中间的子查询和关联的临时结果。这些临时结果也视为独立的表，表名以 `subquery_` 为前缀，根据子查询的作用或内容命名，确保能一一对应。
**表关系结构：**
   任意两个表之间的关系应该按照以下结构描述：

   ```json
   {
       "source_table": "source_table_name",
       "target_table": "target_table_name",
       "order_num": execution_order_number,
       "relation": [
           {
               "source": "source_field",
               "target": "target_field",
               "type": "relation_type",
               "description": "relation_description"
           },
           ...
       ]
   }
   ```

   - **`source_table`** 和 **`target_table`**：两张表的名称，格式为 `database.table`，如果没有 `database`，就直接使用表名。对于子查询或临时表，用 `subquery_` 前缀，根据代码里的命名进行补充。

   - **`order_num`**：标注这两个表在整个 SQL 代码的执行顺序。越是最后执行的计算，Order_num的数值越小，如果是并行执行的操作，它们的 `order_num` 相同。
   ##举例## 对最终目标表target_table, 会有多个join操作，如left join a.name=b.name left join a.name=c.name left join a.name=d.name, 那么这些最终子查询到target_table的order_num = 1

   - **`relation`**：是一个列表，记录这两个表之间的所有代码里涉及到的字段关系。每个字段关系的结构如下：

     - **`source`**：某个字段在源表中的字段名。
     - **`target`**：某个字段在目标表中的字段名。
     - **`type`**：字段关系的类型，详见下面的定义。
     - **`description`**：记录了relation相关的源sql代码。

2. **字段关系类型定义：**

   - **`JOIN`**：记录表之间通过哪些字段进行了连接操作，如 `JOIN ON` 条件。

   - **`FILTER`**：记录根据哪些字段进行了筛选操作，如 `WHERE`、`HAVING` 等。
   
   - **`GROUPBY`**：记录使用哪些字段进行了 `GROUP BY` 操作，使得表的行数发生了聚合变化。

   - **`OTHER`**：记录对字段内容的变换，不改变表的行数，包括以下子类型：

     - **`EQUAL`**：字段直接赋值，没有任何变化。
     - **`STRING`**：字符串操作的字段变换。
     - **`NUMERICAL`**：数值计算的字段变换。
     - **`CONDITION`**：根据条件进行映射的字段变换，如 `CASE WHEN`。
     - **`TRANS`**：格式或类型转换的字段变换。
     - **`WINDOW`**：窗口函数的字段变换。
     - **`AGGREGATION`**：聚合函数的字段变换，与 `GROUP BY` 对应。

3. **注意事项：**

   - **全面性**：在提取关系时，要详细记录每一个步骤，包括`JOIN`、`FILTER`  `GROUP BY`、等操作。有些字段可能同时进行了多个操作，每一个都要列举清楚。
   
   - **完整性**：确保每一个字段关系都有明确的类型和描述，特别是JOIN 这个类型, 如果存在两个表关联，一定两个关系中都有字段是JOIN类型的。

   - **子查询处理**：对于 SQL 中的子查询，视为独立的临时表，按照其主要作用命名，例如 `subquery_b`、`subquery_c` 等。

   - **字段关系描述**：`description` 字段应包含具体的SQL代码片段，尽可能完整呈现，保证能从json文件还原sql逻辑关系，但也不要冗余。

   - **JSON 格式输出**：最终的结果应以 JSON 格式输出，保证结构清晰，信息完整。
   
## 示例1：##
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。

## 示例2： ##
table1 与 subquery1, subquery2, subquery3 都进行了join操作，得到了target，那么应该有 table1->target_table, subquery1->target_table, subquery2->target_table, subquery3->target_table 且都有join 字段的记录。
具体SQL代码如下:

'''
#效果很不好，需要重新设计prompt。少了示例，整个模型都变笨了。



version8='''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_23 order_num=2, table3->subquery_23 order_num=2, subquery_23->table4 order_num=1 这四个关系。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用过的字段关系。每组字段关系都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。
type根据定义选择:GROUPBY,FILTER,JOIN,OTHER 四个,定义如下:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:前面三种都是对结果表的行数可能产生影响的，Other里只记录字段内容产生影响的关系，比如字符串改动，数值计算，条件映射，区间分段等，核心原则是只改变内容。以下是可能的子分类如下:
    1)EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。

最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 找到所有sql代码里出现的字段,比如两个表根据phone_no这个字段进行关联，那么两个表到这个关联子查询里都应该出现phone_no, 如果这个phone_no用于不同的作用，应该全部列举清楚。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系
具体sql代码如下:
'''

version8_2='''
你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容命名，保证能一一对应.
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_12, table2_subquery_12, subquery_12->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_23 order_num=2, table3->subquery_23 order_num=2, subquery_23->table4 order_num=1 这四个关系。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用过的字段关系。每组字段关系都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。注意如果某个字段只在source_table里出现了，target_table最终没有使用到,那么就为空。
type根据定义选择:GROUPBY,FILTER,JOIN,OTHER 四个,定义如下:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:前面三种都是对结果表的行数可能产生影响的，Other里只记录字段内容产生影响的关系，比如字符串改动，数值计算，条件映射，区间分段等，核心原则是只改变内容。以下是可能的子分类如下:
    1)EQUAL:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。

最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 找到所有sql代码里出现的字段,比如两个表根据phone_no这个字段进行关联，那么两个表到这个关联子查询里都应该出现phone_no, 如果这个phone_no还用于其他不同的作用，比如group by,where等应该全部列举清楚。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系，根据什么关联很重要，不要忘记。
具体sql代码如下:
'''


## 为了避免那种单表情况，增加一个输出判断。
# 请先帮我判断这段sql代码是否只是简单的建表或者删除表的语句。如果不存在两张表或以上的血缘关系，那么直接输出字符串"META TABLE"。如果需要进行血缘关系分析，那么请继续执行下面的步骤。

version8_3='''
请先帮我判断这段sql代码是否存在两张表或以上的血缘关系，如果没有，那么直接输出字符串"META TABLE"，不要任何其他内容，直接结束。如果需要进行血缘关系分析，那么请继续执行下面的步骤。

你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容与出现顺序命名（由1开始递增），保证能一一对应.
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_1, table2_subquery_1, subquery_1->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_1 order_num=2, table3->subquery_1 order_num=2, subquery_1->table4 order_num=1 这四个关系。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用过的字段关系。每组字段关系都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。注意如果某个字段target_table最终没有使用到,那么就与source_table里的字段同名。
type由{maj_name}-{type_name}组合而成。根据定义，maj_name一共有 GROUP,FILTER,JOIN,OTHER 四个,定义如下:
1.GROUP:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by，partion by关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
4.OTHER:前面三种都是对结果表的行数可能产生影响的，Other里只记录字段内容产生影响的关系，比如字符串改动，数值计算，条件映射，区间分段等，核心原则是只改变内容。以下是可选的type_name:
    1)select:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)string:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)numerical: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)condition:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)trans:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)window: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)aggregation: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。
    8)order: 这个字段用于排序。

最后的description记录了relation相关的源sql代码。
## 注意 ## 内容只以json格式输出，不要其他内容。完整保存原有sql逻辑关系，但尽量不要冗余。
## 注意 ## 要求找到所有sql代码里出现的字段,比如两个表根据phone_no这个字段进行关联，那么两个表到这个关联子查询里都应该出现phone_no, 如果这个phone_no还用于其他不同的作用，比如group by,where等应该全部列举清楚。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系，根据什么字段关联很重要，不要忘记。
具体sql代码如下:
'''

version9_2 = '''
请先帮我判断这段sql代码是否存在两张表或以上的血缘关系，如果没有，那么直接输出字符串"META TABLE"，不要任何其他内容，直接结束。如果需要进行血缘关系分析，那么请继续执行下面的步骤。

你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码内容与出现顺序命名（由1开始递增），保证能一一对应.
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_1, table2_subquery_1, subquery_1->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_1 order_num=2, table3->subquery_1 order_num=2, subquery_1->table4 order_num=1 这四个关系。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用了JOIN关系的字段。每组字段都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。注意如果某个字段target_table最终没有使用到,那么就与source_table里的字段同名。

JOIN的定义如下:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如
INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
再比如有 SELECT ** FROM table1 LEFT JOIN (subquery_1) on table1.id = subquery_1.id LEFT JOIN (subquery_2) on table1.id = subquery_2.id LEFT JOIN (subquery_3) on table1.id = subquery_3.id;
那么subquery_1, subquery_2, subquery_3, table1, table2, table3的关系都应该有JOIN操作，且JOIN操作的字段都是id。一定不要遗漏任何join关系！
type应为: left join，right join, inner join，full join，union，union all等相似功能的关键字进行选择。
如果两张表没有JOIN关系，只有FROM table1, table2这样的，那么relation字段为空。
最后的description记录了relation相关的源sql代码。
## 注意 ## 内容只以json格式输出，不要其他描述。完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系
具体sql代码如下:

'''
version9='''
JOIN

你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码里出现的顺序进行命名。
#注意，如果整段代码只有一个JOIN关联，那么应该不存在需要额外命名的子查询，直接输出结果表即可。如果存在多个，那么从1开始递增命名，保证能一一对应。为保证每次结果都稳定相同，不考虑执行逻辑的顺序，只看子查询关键字出现的顺序。
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_1, table2_subquery_1, subquery_1->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_1 order_num=2, table3->subquery_1 order_num=2, subquery_1->table4 order_num=1。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用了JOIN关系的字段。每组字段都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。注意如果某个字段只在source_table里出现了，target_table最终没有使用到,那么就为空。

JOIN的定义如下:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type应为: left join， inner join，full join，union，union all等相似功能的关键字进行选择。
最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系
具体sql代码如下:


Threetype





你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码里出现的顺序进行命名。
#注意，如果整段代码只有一个JOIN关联，那么应该不存在需要额外命名的子查询，直接输出结果表即可。如果存在多个，那么从1开始递增命名，保证能一一对应。为保证每次结果都稳定相同，不考虑执行逻辑的顺序，只看子查询关键字出现的顺序。
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_1, table2_subquery_1, subquery_1->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_1 order_num=2, table3->subquery_1 order_num=2, subquery_1->table4 order_num=1。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，使用了JOIN关系的字段。每组字段都有相同的结构如下{source, target, type, description}.
source和target是具体每一个字段名, source就是source_table里的字段的名字， target就是这个字段在target_table里叫的名字，一般可能是同名的，有时候会重命名。注意如果某个字段只在source_table里出现了，target_table最终没有使用到,那么就为空。
type有GROUPYB, FILTER, JOIN三种，定义如下:
1.GROUPBY:记录根据哪个字段进行group by等操作，让整个表的行数发生了变化。比如INSERT INTO table2 column1 SELECT SUM(column1) FROM table1 GROUP BY column2;
type_name 应为group by等关键字，
2.FILTER: 记录根据哪几个字段作为过滤条件，对target_table的结果进行筛选。 比如INSERT INTO tbale2 (column1) SELECT * FROM table1 WHERE (column1) > 30;
type_name 应为这些 where, having, limit, offset, distinct等相同功能的关键字。
3.JOIN:记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
type_name 应为 left join， inner join，full join，union，union all等相同功能的关键字。
其它没有提到的关系，如select，或者一些计算，内容字符映射，转换等。都不要记录。
最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 找到所有sql代码里出现的字段,比如两个表根据phone_no这个字段进行关联，那么两个表到这个关联子查询里都应该出现phone_no, 如果这个phone_no用于不同的作用，应该全部列举清楚。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系
具体sql代码如下:




自由发挥版本:#效果很不好，join会被当成where， qwen和gpt4都是


你是一个SQL代码专家，请你帮我从上述SQL代码中抽取出不同表之间的关系，注意，包括了中间的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码里出现的顺序进行命名。
#注意，如果整段代码只有一个JOIN关联，那么应该不存在需要额外命名的子查询，直接输出结果表即可。如果存在多个，那么从1开始递增命名，保证能一一对应。为保证每次结果都稳定相同，不考虑执行逻辑的顺序，只看子查询关键字出现的顺序。
##举例1## 
table1 到 table2先进行了子查询，子查询结果再与table3关联形成了table4， 那么至少应有 table1->subquery_1, table2_subquery_1, subquery_1->table4, table3->table4这四个关系。 

任意两个表之间的关系应该有如下结构。 {source_table, target_table, order_num, relation:[]} 
source_table, target_table,描述两张表的名字，以database.table的格式输出，如果没有database就忽略;
order_num 标注这两个表在整个sql代码的执行顺序。越是最后执行的order_num,应该数值越小。如果是最后多个子查询结果一起关联出结果表，order_num 应该为1;
## 举例2 ##
table1 与 table2和table3 关联的结果，再进行关联得到table4。 那么有 table1->table4 order_num=1, table2->subquery_1 order_num=2, table3->subquery_1 order_num=2, subquery_1->table4 order_num=1。

relation是一个列表list,记录这两个表中所有在sql代码里出现过的，每组字段都有相同的结构如下{source, target, type, description}. 
type的可选范围如下:
    1)SELECT:一个字段直接赋值到另一个字段，没有任何变化， 比如INSERT INTO table2 (column1) SELECT column1 FROM table1; 
    2)STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
    length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
    3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
    还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
    4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
    5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
    其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.  
    6)WINDOW: 一个字段由另一个字段使用窗口函数进行了运算，比如INSERT INTO table2 (column1) SELECT  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num  FROM table1;
    其他的如rank(),lead(),lag(),dense_rank()等也算在其中。
    7)FILTER: 一个字段由另一个字段进行筛选，比如INSERT INTO table2 (column1) SELECT column1 FROM table1 WHERE column1 > 30;
    distinct,where,offset，limit等都算在其中
    8)GROUPBY: 一个字段由另一个字段进行分组，比如INSERT INTO table2 (column1) SELECT SUM(column1) FROM table1 GROUP BY column2;
    9)AGGREGATION: 应该与前面有的GROUP BY 一一对应 
    count(),sum(),avg(),min(),max()等函数都算在其中。
    10) JOIN: 记录根据哪些字段进行JOIN操作连接起来，使得新的表的结果行数发生了一些变化。比如INSERT INTO table2 (column1) SELECT table1.column1 FROM table1 JOIN table2 ON table1.id = table2.id;
    left join， inner join，full join，union，union all等相同功能的关键字。
    11) OTHER: 其他没有提到的关系，order by等等，都算在其中。

最后的description记录了relation相关的源sql代码。
## 注意 ## 内容以json格式输出，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余。
## 注意 ## 找到所有sql代码里出现的字段,比如两个表根据phone_no这个字段进行关联，同时根据phone_no进行group by 操作，最后后还select。那么所有操作应该全部列举清楚。
## 注意 ## 不要遗漏表与表之间的关系，特别是最后多个子查询一起关联到目标表的关系
## 注意 ## 不要relation里不要任何join相关的关系，他们在另一个任务中已经被识别了。
具体sql代码如下:



'''

#v10效果也不好，很容易出现target字段消失了的问题。有个能phone的字段不会出现在最终结果表里了
version10='''
你是一个SQL代码专家，请你帮我从SQL代码中抽取出所有出现的表以及所有他们所使用的字段，记录这些字段使用的方法和流向。定义标准结构如下:{source_table_name,all_used_fields:[]}
其中source_table_name是当前这张表的表名，以database.table的格式输出，如果没有database就忽略。
注意sql代码中的子查询，关联的临时结果，也应该算作是一张表，表名以subquery_为前缀，根据代码里出现的顺序进行命名。
##举例:## 
SELECT * INTO table4  FROM table1 JOIN (SELECT *  FROM table2  JOIN table3 ON table2.key = table3.key) AS subquery_1 ON table1.key = subquery_1.key;
那么应该有table1,table2,table3,subquery_1,table4这5个表，其中table1,table2,table3是原始表，subquery_1是子查询结果表，table4是最终结果表。

其中每张表的all_used_fields是一个列表，记录了这张表里所有出现过的字段，每个字段的结构如下{field_name,target_table_name, target_filed_name,field_use_type, sub_type, direction}]
field_name 为当前表里字段的命名。
target_table_name 为当前字段指向的目标表名
target_filed_name 为当前字段指向的目标字段名
field_use_type 为当前字段的使用类型，可选范围如下:

    1.JOIN:表示多个表根据这个字段进行关联，比如table1 JOIN table2 ON table1.id = table2.id;
    sub_type为 LEFT JOIN, RIGHT JOIN, INNER JOIN, FULL JOIN, UNION, UNION ALL等;
    2.FILTER: 表示结果针对这个字段为条件，筛选过滤，比如SELECT * FROM table1 WHERE table1.id > 10;
    sub_type为 WHERE,HAVING,DISTINCT,WHERE,OFFSET,LIMIT等;
    3.GROUP: 表示对结果根据这个字段分组，比如SELECT * FROM table1 GROUP BY table1.id;
    sub_type为 GROUP BY,PARTION BY;
    4.AGGREGATION: 表示对这个字段进行聚合计算，往往有GROUPBY, 必有AGGREGATION。 比如SELECT SUM(table1.id) FROM table1 GROUP BY table1.key;
    sub_type为 COUNT,SUM,AVG,MIN,MAX等;
    5.WINDOW: 表示这个字段是有窗口函数计算得来的结果，比如SELECT id, department RANK() OVER (PARTITION BY department ORDER BY age DESC) AS age_rank FROM table1;
    age_rank的 sub_type就是RANK,其它还有LEAD,LAG,ROW_NUMBER等;
    6.ORDER: 表示这个字段被排序，比如SELECT * FROM table1 ORDER BY table1.id;
    7.SELECT: 表示这个字段被选择出来，作为结果的一部分，比如SELECT table1.id FROM table1; 
    sub_type有 EQUAL,STRING,NUMERICAL,CONDITION,TRANS,OTHER六种：
        1) EQUAL: 当这个字段被选择出来，没有变动，或者只改变了命名时，比如SELECT field1 as column1 FROM table1;
        2) STRING:一个字段经过了某种简单映射，变成了另一个字段 比如INSERT INTO table2 (column1) SELECT UPPER(column1) FROM table1;
        length(),concat(),substring(),upper(),lower(),replace(),trim()等字符计算都是STRING.
        3)NUMERICAL: 一个字段由另一个字段进行一些基础运算，比如INSERT INTO table2 (column1) SELECT column2 * 2 FROM table1;
        还有很多其他的比如 +,-,*,/,% 基本数学运算,abs(),ceil(),round(),power()等等数值计算的函数，都算在NUMERICAL.
        4)CONDITION:根据一些条件，进行比较复杂的映射，比如INSERT INTO table2 (column1) SELECT CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Non-Positive' END FROM table1;
        5)TRANS:一个字段由另一个字段进行了格式转换或者日期转化而来。比如INTO table2 (column1) SELECT  CONVERT('2023-10-01', DATE); FROM table1;
        其他如curtime()，curdate()等等日期操作，cast(),convert()等都算在TRANS里.
        6)OTHER: 上述中没有任何一种情况合适，没有考虑到的，记录为OTHER。
        
direction: 记录这个字段相关的源sql代码，完整呈现，保证能从json文件还原回sql逻辑关系，但尽量不要冗余
## 注意 ## 
    1. 内容以json格式输出，不需要其他分析。
    2. 不要遗漏子查询表的关系，避免出现子查询表没有出现在json文件中。
    3. 一个字段可能有多种field_use_type,或者指向多个字段，不要遗漏，要尽可能的全面。
具体SQL代码如下:  

'''



only_table_1='''
你是一个SQL代码专家，请你帮我分析下面这段sql代码是否具有血缘分析的必要。如果这段sql代码，只有一些基础的建表语句，或者drop，insert等，没有两张表之间的关系，那么请帮我返回这一张表的元数据结构
具体结果以json格式为例输出。格式如下:


'''