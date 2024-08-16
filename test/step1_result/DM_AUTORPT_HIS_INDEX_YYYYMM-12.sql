#效果不太好，需要测试下能否再处理后变成正常的样子
DROP TABLE ${TARGET_DM_AUTORPT_HIS_INDEX_YYYYMM};


CREATE TABLE ${TARGET_DM_AUTORPT_HIS_INDEX_YYYYMM} (OP_TIME DATE ,STATIS_MONTH INTEGER ,PRODUCT_NO VARCHAR(20) ,
                                                                                                   HF0001 DECIMAL(12, 2) ,
                                                                                                          HF0002 DECIMAL(12, 2) ,
                                                                                                                 HF0003 DECIMAL(12, 2) ,
                                                                                                                        HF0004 DECIMAL(12, 2) ,
                                                                                                                               HF0005 DECIMAL(12, 2) ,
                                                                                                                                      HF0006 DECIMAL(12, 2) ,
                                                                                                                                             HF0007 DECIMAL(12, 2) ,
                                                                                                                                                    HF0008 DECIMAL(12, 2) ,
                                                                                                                                                           HF0009 DECIMAL(12, 2) ,
                                                                                                                                                                  HF0010 DECIMAL(12, 2) ,
                                                                                                                                                                         HF0011 DECIMAL(12, 2) ,
                                                                                                                                                                                HF0012 DECIMAL(12, 2) ,
                                                                                                                                                                                       HF0013 DECIMAL(12, 2) ,
                                                                                                                                                                                              HF0014 DECIMAL(12, 2) ,
                                                                                                                                                                                                     HF0015 DECIMAL(12, 2) ,
                                                                                                                                                                                                            HF0016 DECIMAL(12, 2) ,
                                                                                                                                                                                                                   HFGJ01 DECIMAL(12, 2) ,
                                                                                                                                                                                                                          HFGJ01_1 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                   HFGJ01_2 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                            HFGJ01_3 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                     HFGJ01_4 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                              HFGJ02 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                     HFGJ02_1 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                              HFGJ02_2 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                       HFGJ02_3 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                HFGJ02_4 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                         HFGJ03 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                                HFGJ03_1 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                                         HFGJ03_2 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                                                  HFGJ03_3 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                                                           HFGJ03_4 DECIMAL(12, 2) ,
                                                                                                                                                                                                                                                                                                                                                    HM0001 INTEGER ,HM0002 INTEGER ,HM0003 INTEGER ,HM0004 INTEGER ,HM0005 INTEGER ,HM0006 INTEGER ,HM0007 INTEGER ,HM0008 INTEGER ,HM0009 INTEGER ,HM0010 INTEGER ,HM0011 INTEGER ,HM0012 INTEGER ,HM0013 INTEGER ,HM0014 INTEGER ,HM0015 INTEGER ,province_name varchar(50) -- 漫游省份   以下指标20190227新增
 ,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  last3_mounth_avg_cc decimal(41, 2) -- 近三个月平均消费（剔除即扣即返收入）
 ,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      last6_mounth_avg_cc decimal(44, 2) -- 近六个月平均消费（剔除即扣即返收入）
 ,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          dg_USE_RES_NUM BIGINT -- 订购定向流量资源使用量
 ,dg_TOTAL_RES_NUM BIGINT -- 订购定向流量资源总量
 ,zs_USE_RES_NUM BIGINT -- 赠送定向流量资源使用量
 ,zs_TOTAL_RES_NUM BIGINT -- 赠送定向流量资源总量
 ,gprs_USE_RES_NUM BIGINT -- GPRS国内资源使用量
 ,is_acct_uesr_cc bigint(1) -- 是否为出账客户（不含物联网）
 ,
                  LAST1_PLAN_MONTHLY_FEE decimal(12, 2) -- 主套餐月租费-前第1月
 ,
                                         LAST2_PLAN_MONTHLY_FEE decimal(12, 2) -- 主套餐月租费-前第2月
 ,
                                                                LAST3_PLAN_MONTHLY_FEE decimal(12, 2) -- 主套餐月租费-前第3月
 ,
                                                                                       LAST6_PLAN_MONTHLY_FEE decimal(12, 2) -- 主套餐月租费-前第6月
 ,
                                                                                                              last1_tc_month_fee decimal(12, 2) -- 套餐月租费-前第1月
 ,
                                                                                                                                 last2_tc_month_fee decimal(12, 2) -- 套餐月租费-前第2月
 ,
                                                                                                                                                    last3_tc_month_fee decimal(12, 2) -- 套餐月租费-前第3月
 ,
                                                                                                                                                                       last4_tc_month_fee decimal(12, 2) -- 套餐月租费-前第6月
 ,
                                                                                                                                                                                          lastyear_d_tc_month_fee decimal(12, 2) -- 套餐月租费-去年同期
 ,
                                                                                                                                                                                                                  lastyear_d_ztc_month_fee decimal(12, 2) -- 主套餐月租费-去年同期
 ,
                                                                                                                                                                                                                                           is_bxl_plan_user bigint(2) -- 是否不限量套餐到达用户
 ,
                                                                                                                                                                                                                                                            rc_id bigint(20) -- 区域中心
 ,
                                                                                                                                                                                                                                                                  end_time date -- 客户星级有效期
 ,bd_call_fee_cc decimal(23, 2) -- 本地通话费（剔除低消）20190411日添加
 ,
                 prom_fee decimal(44, 2) -- 低消费用       以下20190415日添加
 ,
                          this_fee decimal(35, 3) -- 当月预付费欠费
 ,
                                   this_backfee decimal(42, 2) -- 当月预付费欠费收回
 ,
                                                trans_amt decimal(44, 2) -- 赠费金额
 ,
                                                          minus_fee decimal(45, 2) -- 折后收入
 ,
                                                                    is_group_plan_user bigint(1) -- 是否集团套餐用户
 ,
                                                                                       is_groupplan_mn_user bigint(1) -- 是否集团套餐当月新增用户
 ,
                                                                                                            total_Fee decimal(33, 2) -- 套餐外语音费
 ,
                                                                                                                      dept_county_id int(11) -- 当月高频通信分公司 以下20190425日添加
 ,
                                                                                                                                     grid_id int(11) -- 当月高频通信网格
 ,
                                                                                                                                             is_4gnet_newuser bigint(1) --  是否4G网络客户（本地剔除物联网） 以下20190428日添加
 ,
                                                                                                                                                              is_4g_arrieduser bigint(1) --  是否4G有效客户（本地2019）
 ,
                                                                                                                                                                               CA_CUST_ID varchar(50) --  客户CA编码
 ,
                                                                                                                                                                                          REMOVE_FEE DECIMAL(12, 2) -- 折后ARPU（分)
 ,
                                                                                                                                                                                                     CALING_NUM decimal(42, 0) -- 主叫通话次数   -- 以下20190528日添加
 ,
                                                                                                                                                                                                                CALLED_NUM decimal(42, 0) -- 被叫通话次数
 ,
                                                                                                                                                                                                                           bhd_lgprs_res double(20, 3) -- 饱和度国内流量资源
 ,
                                                                                                                                                                                                                                         micro_id varchar(20) -- 当月高频通信微格
 ,
                                                                                                                                                                                                                                                  is_5gpuls int -- 是否5G终端用户
 ,lvl_name varchar(20) -- CO重要程度
 ,
           co_grid varchar(200) -- CO归属经分网格
 ,
                   co_begin_time datetime , -- CO起始时间
 call_dur_gj_xg bigint, -- 国际长途通话时长-香港
 call_fee_gj_xg decimal(12, 2), -- 国际长途超套费-香港
 call_dur_gj_xjp bigint, -- 国际长途通话时长-新加坡
 call_fee_gj_xjp decimal(12, 2), -- 国际长途超套费-新加坡
 call_dur_gj_hg bigint, -- 国际长途通话时长-韩国
 call_fee_gj_hg decimal(12, 2), -- 国际长途超套费-韩国
 call_dur_gj_mg bigint, -- 国际长途通话时长-蒙古
 call_fee_gj_mg decimal(12, 2), -- 国际长途超套费-蒙古
 call_dur_gj_dg bigint, -- 国际长途通话时长-德国
 call_fee_gj_dg decimal(12, 2), -- 国际长途超套费-德国
 call_dur_gj_fg bigint, -- 国际长途通话时长-法国
 call_fee_gj_fg decimal(12, 2), -- 国际长途超套费-法国
 call_dur_gj_od bigint, -- 国际长途通话时长-澳大利亚
 call_fee_gj_od decimal(12, 2), -- 国际长途超套费-澳大利亚
 call_dur_gj_am bigint, -- 国际长途通话时长-美国
 call_fee_gj_am decimal(12, 2), -- 国际长途超套费-美国
 is_top25_user bigint(1), -- 是否重点客户保拓（TOP25%拍照客户）
 is_other75_user bigint(1), -- 是否重点客户保拓（其他75%拍照客户）
 is_top25_by_user bigint(1), -- 是否重点客户保拓（TOP25%拍照客户保有客户）
 is_other75_tz_user bigint(1),-- 是否重点客户保拓（其他75%拍照客户拓展客户）
 is_2018_zerocall_user bigint(1),-- 是否重点客户保拓（2018年拍照期末0通信客户）
 is_2018_zerocall_tz_user bigint(1), -- 是否重点客户保拓（2018年拍照期末0通信客户拓展客户）
 is_2019_newnet_user bigint(1), -- 是否重点客户保拓（2019年新入网客户拓展客户）
 is_top25_lius int, -- 是否重点客户保拓(TOP25%流失客户)
 is_top25_lius2 int, -- 是否重点客户保拓(流失TOP25%客户-ARPU同时低于最低拍照ARPU值和拍照期80%客户)
 is_top25_lius3 int, -- 是否重点客户保拓(流失TOP25%客户-ARPU高于最低拍照ARPU值但低于80%客户)
 is_top25_lius4 int, -- 是否重点客户保拓(流失TOP25%客户-ARPU高于80%但低于拍照最低ARPU值客户)
 zh_curm_arpu decimal(18, 2), ###折后当月ARPU（剔除国际业务收入） fee001 decimal(18, 2), -- ARPU-主套餐月租费
 fee002 decimal(18, 2), -- ARPU-流量
 fee003 decimal(18, 2), -- ARPU-语音套外
 fee004 decimal(18, 2), -- ARPU-短彩信
 fee005 decimal(18, 2), -- ARPU-家庭宽带
 fee006 decimal(18, 2), -- ARPU-个人融合产品
 fee007 decimal(18, 2), -- ARPU-And Market
 fee008 decimal(18, 2), -- ARPU-其他数据业务
 fee009 decimal(18, 2), -- ARPU-其他收入
 fee010 decimal(18, 2), -- ARPU-信息化
 fee011 decimal(18, 2), -- ARPU-套餐及套外
 fee012 decimal(18, 2), -- ARPU（国际业务收入）
 fee013 decimal(18, 2), -- ARPU(折扣金额)
 last_REMOVE_FEE DECIMAL(12, 2), -- 上个月折后ARPU
 last2_REMOVE_FEE DECIMAL(12, 2), -- 上上个月折后ARPU
 youhui_fee DECIMAL(12, 2), -- arpu(优惠金额)
 ycff_fee DECIMAL(12, 2), -- arpu(预存返费金额)
 fee014 decimal(18, 2) -- 折后实收收入
 ) DISTRIBUTED BY('product_no');