drop table tmp_20150512_gprs_${dayid};\\\\n
CREATE TABLE tmp_20150512_gprs_${dayid}     \\\\n
(     \\\\n
phone_no varchar(20) ,\\\\n
dg_USE_RES_NUM int , -- 订购定向流量资源使用量(MB)\\\\n
dg_TOTAL_RES_NUM bigint , -- 订购定向流量资源总量(MB)\\\\n
zs_USE_RES_NUM bigint ,  -- 赠送定向流量资源使用量(MB)\\\\n
zs_TOTAL_RES_NUM bigint , -- 赠送定向流量资源总量(MB)\\\\n
gprs_USE_RES_NUM bigint ,-- GPRS国内资源使用量(kb)\\\\n
is_4G_valid_user bigint(1)      -- 是否为4G有效客户（集团口径）\\\\n
) distributed by ('phone_no');\\\\n
insert into tmp_20150512_gprs_${dayid}\\\\n
select a.phone_no,\\\\n
       b.dg_USE_RES_NUM,    -- 订购定向流量资源使用量\\\\n
    b.dg_TOTAL_RES_NUM,  -- 订购定向流量资源总量\\\\n
    c.zs_USE_RES_NUM,    -- 赠送定向流量资源使用量\\\\n
    c.zs_TOTAL_RES_NUM ,   -- 赠送定向流量资源总量\\\\n       d.RES_USE_NUM,   -- GPRS国内资源使用量    20190523日调整口径\\\\n       case when e.phone_no is not null then 1 else 0 end is_4G_valid_user -- 是否为4G有效客户（集团口径）\\\\nfrom gbasedwi.dwi_usr_pesn_partinfo_ds_${dayid} a        \\\\nleft join (select  b.phone_no,\\\\n                   sum(b.USE_RES_NUM/1024/1024) dg_USE_RES_NUM,\\\\n                   sum(b.TOTAL_RES_NUM/1024/1024) dg_TOTAL_RES_NUM \\\\n           from dm.dim_dx_flow a\\\\n           left join gbasedwi.${table_name.name1} b on a.plan_id=b.plan_id and a.use_type=b.use_type \\\\n           group by phone_no\\\\n           ) b on a.phone_no=b.phone_no\\\\nleft join ( \\\\n           select  phone_no,\\\\n                   sum(USE_RES_NUM/1024/1024) zs_USE_RES_NUM, -- 赠送定向流量资源使用量\\\\n                   sum(TOTAL_RES_NUM/1024/1024) zs_TOTAL_RES_NUM -- 赠送定向流量资源总量\\\\n          from gbasedwi.${table_name.name1} \\\\n          where plan_id='111002069417'\\\\n          group by phone_no    \\\\n          ) c on a.phone_no=c.phone_no\\\\nleft join (\\\\n          select phone_no,\\\\n                sum(case when b.item_code is not null then a.FREE_RES_USE_NUM else 0 end)/1024 RES_USE_NUM    -- GPRS国内资源使用量 \\\\n          from gbasedwd.${tablename.dwdfreeres1} a\\\\n          left join (\\\\n                    select item_code from dm.dim_pub_freeres_lty_itemcode group by item_code\\\\n                    ) b on a.item_code=b.item_code\\\\n\\\\t\\\\t  where boss_prod_id not in ('54001105','53005095','50002352','54001809')\\\\n\\\\t\\\\t  and to_number(FREE_RES_TOTAL_NUM)<1000000000000000000\\\\n          group by a.phone_no\\\\n           ) d on a.phone_no=d.phone_no\\\\nleft join (\\\\n            select phone_no from gbasemsm.msm_dw_basekpi_110673_detail_${dayid} group by phone_no\\\\n          ) e on a.phone_no=e.phone_no\\\\nwhere a.PROD_KIND_CODE='171000000001'  And (a.MONTH_ARRIVE_FLAG = 1 Or a.MONTH_OFF_FLAG = 1 or a.MONTH_NEW_FLAG = 1);\\\\n