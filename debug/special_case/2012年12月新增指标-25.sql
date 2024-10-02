insert into ${DM_PUB_201212018_TMP05_MONTHID}
    (	 PRODUCT_NO
    ,CUR_PROMOTION_SCORE
    ,CUR_DATA_SCORE
    ,CUR_CONSUME_SCORE
    ,CHANGE_SCORE_MONTH
    ,CHANGE_SCORE_YEAR
    ,FREE_FLOW_ALL
    ,ACTIVE_COUNT
    ,GPRS_COUNT1
    ,GPRS_COUNT2
    ,GPRS_COUNT3
    ,GPRS_COUNT4
    ,IS_4G_USER		)
    select 	 distinct
    t1.phone_no					PRODUCT_NO
    ,t2.CUR_MON_NEW_SALE_SCORE       CUR_PROMOTION_SCORE
    ,t8.beixiang_TRUN_NUM  CUR_DATA_SCORE
    ,t2.CUR_MON_NEW_CONSM_SCORE      CUR_CONSUME_SCORE
    ,/*t2.CUR_MON_CUT_CONSM_SCORE*/ nvl(t8.TRUN_NUM,0)      CHANGE_SCORE_MONTH
    ,/*nvl(nvl(t4.CHANGE_SCORE_YEAR,0)+nvl(t2.CUR_MON_CUT_CONSM_SCORE,0),0)*/
    case when ${monthid}=${curyfirstmonth} then nvl(t8.TRUN_NUM,0) 
    else nvl(nvl(t4.CHANGE_SCORE_YEAR,0)+nvl(t8.TRUN_NUM,0),0) end CHANGE_SCORE_YEAR
    ,t3.PHONE_NET_FREE_RES_NUM      FREE_FLOW_ALL
    ,nvl(t7.active_count,0)         ACTIVE_COUNT                              /*--4G活跃天数 */
    /*,t4.GPRS_TOTAL_NUM               GPRS_COUNT1
    ,t4.GPRS_LOC_ONNET_NUM           GPRS_COUNT2*/
    ,l.GPRS_COUNT1
    ,l.GPRS_COUNT2
    ,l.GPRS_COUNT3                     /*当月gprs国内漫游上网次数*/
    ,l.GPRS_COUNT4                     /*当月gprs国际漫游上网次数*/
    ,t6.G4_USER_FLAG                IS_4G_USER
from ${DWI_USR_PESN_PARTINFO_MS_MONTHID} t1
left join (select phone_no,
    max(CUR_MON_NEW_SALE_SCORE   )   CUR_MON_NEW_SALE_SCORE ,
    max(CUR_MON_NEW_DOU_ENJOY_SCORE )  CUR_MON_NEW_DOU_ENJOY_SCORE,
    max(CUR_MON_NEW_CONSM_SCORE  )     CUR_MON_NEW_CONSM_SCORE,
    max(CUR_MON_CUT_CONSM_SCORE  )     CUR_MON_CUT_CONSM_SCORE,
    max(YEAR_TOTAL_CUT_CONSM_SCORE )  YEAR_TOTAL_CUT_CONSM_SCORE
from  ${DWI_INCO_BILL_USER_SCORE_DT_CURMLASTDAY}  group by phone_no) t2 on t1.phone_no=t2.phone_no
left join (select user_id,
    sum(PHONE_NET_FREE_RES_NUM) PHONE_NET_FREE_RES_NUM
from ${DWA_UV_USER_DATABUSI_MS_MONTHID} group by user_id) t3 on t1.user_id=t3.user_id
    /*left join (select phone_no,max(GPRS_TOTAL_NUM) GPRS_TOTAL_NUM,max(T_GPRS_FLOW) T_GPRS_FLOW,
    max(GPRS_LOC_ONNET_NUM) GPRS_LOC_ONNET_NUM,
    max(GPRS_LAND_ROAM_ONNET_NUM) GPRS_LAND_ROAM_ONNET_NUM,
    max(GPRS_INTER_ROAM_ONNET_NUM) GPRS_INTER_ROAM_ONNET_NUM
from ${DWI_BEH_USE_GPRS_USERTOT_MS_MONTHID} group by phone_no) t4 on t1.phone_no=t4.phone_no*/
left join ${DWI_USR_PESN_MS_MONTHID} t6 on t1.phone_no=t6.phone_no
left join dm_pub_201212018_${pmonthid} t4 on t1.phone_no=t4.product_no
left join (select phone_no,
    sum(CALL_NUM )  GPRS_COUNT1,
    sum(case when  ROAM_TYPE in (0,1,7) then  CALL_NUM  end ) GPRS_COUNT2,
    sum(case when  ROAM_TYPE in (5,9) then  CALL_NUM  end ) GPRS_COUNT3,
    sum(case when  ROAM_TYPE in (11,13,15,17,41) then  CALL_NUM  end ) GPRS_COUNT4
from gbasedwd.DWD_EVT_CDR_GPRS_BUSITYPETOT_MS_${monthid} group by phone_no ) l on t1.phone_no=l.phone_no
left join (select PHONE_NO,count(STAT_DATE) active_count from (
    select STAT_DATE,PHONE_NO ,sum(total_flow) total_flow  
from GBASEDWD.DWD_EVT_CDR_GPRS_BUSITYPETOT_DM_${monthid}
where    NET_TYPE=6  group by STAT_DATE ,PHONE_NO) a 
where a.total_flow>0  group by PHONE_NO 
    )   t7 on t1.PHONE_NO=t7.PHONE_NO
left join   (select  phone_no,
    sum(case when TRUN_TYPE IN  ('12','81')  then TRUN_NUM else 0 end ) TRUN_NUM,
    sum(case when TRUN_TYPE IN  ('88')  then TRUN_NUM else 0 end ) beixiang_TRUN_NUM
from  gbasedwi.DWI_INCO_BILL_SCORE_TRADESN_DT_${monthid} 
where TRUN_TYPE IN  ('12','81','88') 
group by phone_no
    )  t8 on t1.PHONE_NO=t8.PHONE_NO
where (t1.MONTH_ARRIVE_FLAG=1 And t1.PROD_KIND_CODE= '171000000001') or t1.MONTH_OFF_FLAG  =1;