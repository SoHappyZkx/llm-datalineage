## 1. 2015年5月新增日累计指标-206.sql
>[2024/10/02]   step0 -> step1

这个例子里的代码注释，可能因为  `normalize.py -> format_sql()` 里的正则表达式而把注释的`\n`替换为空格，导致代码和注释混在一起

``` SQL
CREATE TABLE tmp_20150512_gprs_${dayid}     (     
    phone_no varchar(20) ,
    dg_USE_RES_NUM int , -- 订购定向流量资源使用量(MB)
    dg_TOTAL_RES_NUM bigint , -- 订购定向流量资源总量(MB)
    zs_USE_RES_NUM bigint ,  -- 赠送定向流量资源使用量(MB)
    zs_TOTAL_RES_NUM bigint , -- 赠送定向流量资源总量(MB)
    gprs_USE_RES_NUM bigint ,-- GPRS国内资源使用量(kb)
    is_4G_valid_user bigint(1)      -- 是否为4G有效客户（集团口径）
    ) distributed by ('phone_no');
```

2024.10.2 已经改进。 优化了正则表达式，目前只匹配括号后的变量名，加入空格，其他不动。目前使用如下正则表达式：
``` PYTHON
formatted_sql = re.sub(r'\)(?=[a-zA-Z_]\w*)', r') ', formatted_sql) #或者严格一些，直接匹配)后必须是变量名，否则不加空格
```
-----------------------------------------------------------------------

## 2. 2012年12月新增指标-25.sql
>[2024/10/02] step1->step2

这个例子里有大量不同格式的注释 /**/ 等，很那区分。

-----------------------------------------------------------------------

## 3. 2012年12月新增指标-109.sql
>[2024/10/05] step2->step3
这个例子没什么血缘关系，只有一个简单的表结构,那么就不存在什么所谓表关系。