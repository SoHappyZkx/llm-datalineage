drop table tmp_20150512_gprs_${dayid};
    CREATE TABLE tmp_20150512_gprs_${dayid}     
    (     
    phone_no varchar(20) ,
    dg_USE_RES_NUM int , -- 订购定向流量资源使用量(MB)
    dg_TOTAL_RES_NUM bigint , -- 订购定向流量资源总量(MB)
    zs_USE_RES_NUM bigint ,  -- 赠送定向流量资源使用量(MB)
    zs_TOTAL_RES_NUM bigint , -- 赠送定向流量资源总量(MB)
    gprs_USE_RES_NUM bigint ,-- GPRS国内资源使用量(kb)
    is_4G_valid_user bigint(1)      -- 是否为4G有效客户（集团口径）
    ) distributed by ('phone_no');
    insert into tmp_20150512_gprs_${dayid}
    select a.phone_no,
    b.dg_USE_RES_NUM,    -- 订购定向流量资源使用量
    b.dg_TOTAL_RES_NUM,  -- 订购定向流量资源总量
    c.zs_USE_RES_NUM,    -- 赠送定向流量资源使用量
    c.zs_TOTAL_RES_NUM ,   -- 赠送定向流量资源总量
    d.RES_USE_NUM,   -- GPRS国内资源使用量    20190523日调整口径
    case when e.phone_no is not null then 1 else 0 end is_4G_valid_user -- 是否为4G有效客户（集团口径）
from gbasedwi.dwi_usr_pesn_partinfo_ds_${dayid} a        
left join (select  b.phone_no,
    sum(b.USE_RES_NUM/1024/1024) dg_USE_RES_NUM,
    sum(b.TOTAL_RES_NUM/1024/1024) dg_TOTAL_RES_NUM 
from dm.dim_dx_flow a
left join gbasedwi.${table_name.name1} b on a.plan_id=b.plan_id and a.use_type=b.use_type 
group by phone_no
    ) b on a.phone_no=b.phone_no
left join ( 
    select  phone_no,
    sum(USE_RES_NUM/1024/1024) zs_USE_RES_NUM, -- 赠送定向流量资源使用量
    sum(TOTAL_RES_NUM/1024/1024) zs_TOTAL_RES_NUM -- 赠送定向流量资源总量
from gbasedwi.${table_name.name1} 
where plan_id='111002069417'
group by phone_no    
    ) c on a.phone_no=c.phone_no
left join (
    select phone_no,
    sum(case when b.item_code is not null then a.FREE_RES_USE_NUM else 0 end)/1024 RES_USE_NUM    -- GPRS国内资源使用量 
from gbasedwd.${tablename.dwdfreeres1} a
left join (
    select item_code from dm.dim_pub_freeres_lty_itemcode group by item_code
    ) b on a.item_code=b.item_code
where boss_prod_id not in ('54001105','53005095','50002352','54001809')
and to_number(FREE_RES_TOTAL_NUM)<1000000000000000000
group by a.phone_no
    ) d on a.phone_no=d.phone_no
left join (
    select phone_no from gbasemsm.msm_dw_basekpi_110673_detail_${dayid} group by phone_no
    ) e on a.phone_no=e.phone_no
where a.PROD_KIND_CODE='171000000001'  And (a.MONTH_ARRIVE_FLAG = 1 Or a.MONTH_OFF_FLAG = 1 or a.MONTH_NEW_FLAG = 1);
