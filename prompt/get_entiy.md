你是一个资深数据开发工程师，非常擅长sql代码的分析与理解。现在需要你帮我解析一段sql，将其中所有sql中涉及到的表与字段，用图谱三元体的形式展现出来。
输出json字符串，每一组元素他们应该包含三个字段， "source_entity", "usage","target_entity", "relation",
其中source_entity 需要有由<表名>.<字段名>的格式表示这个字段所在的表。
- * : 如果一个表的字段是直接引用了*,那么
usage 表示的是这个字段是否还被用于做其他使用方法，可以是一个list。包含的方法有
- value: 表示这个字段被用于赋值，不管是否有其他计算都是有赋值的作用
- filter: 表示这个字段被用于过滤,同时应该加入他的语法。 
- join: 表示这个字段被用于join on 的操作，可以细分left join,right join, inner join, union join等 比如"join: left join on"
- group: 表示这个字段被用于group by 的操作 可细分聚合计算的结果: 比如:"group"
- order: 表示这个字段被用于排序的操作。
- case: 表示这个字段被用于条件分支
target_entity 也是由<表名>.<字段名>的格式表示这个目标字段所在的表。
relation这个字段里应该写出的是这个source_entity进行的计算。 包括了所有的计算逻辑，也是一个list。可能包含的内容有
比如: "filter: where source_entity >= 15"
比如："

#特殊情况示例1
输入：
select * from dm.dm_pub_5g_sa_open_dm_${monthid}


输出：
{
    "source_entity": "dm.dm_pub_5g_sa_open_dm_${monthid}.*"
    "target_entity": "TARGETTABLE.*"
    "relation": "pass"
}
由于没有说字段的名字，所以表示这个表所有的字段* 都被选中，没有目标表就用TARGETTABLE表示。最后的*也是同名
应为直接进行引用，所以他们的关系就是pass




# 第二个是从一长段代码里抽出来某一个字段本身相关的代码