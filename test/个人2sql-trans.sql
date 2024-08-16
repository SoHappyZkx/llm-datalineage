INSERT INTO dm.dm_pub_2021_add_${monthid}
SELECT DISTINCT '${curm_first_day}',
                a.phone_no,
                b.hcy_flow_m,
                b.is_5gsa_dengw,
                c.is_2021_pz_user_new,
                c.USER_VIDEO_REGISTER,
                c2.is_chzh_user_yj,
                ykl_flow_m,
                dy_app_flow,
                nvl(is_shuzi_quanyi_user, 0),
                addr_id, -- IP地址/位置信息-实名相关
 addr_imei, -- 设备IMEI-实名相关
 is_5g_dengw_kh,
 is_all_manyou,
 is_tongxin_user, --  通信用户
 FEATURE_VALUE , -- 主套餐档位
 new_plan_name , -- 下月生效套餐名称
 is_campus_plan , -- 是否校园套餐用户
 free_res_use_num , -- 当月GPRS资源使用量（GB）
 credit_sum, -- 中移信用分值
 credit_date, -- 中移信用分对应的账期
 total_yy_num, -- 主套餐语音资源
 total_ll_num, -- 主套餐流量资源
 total_flow_new,
 volume_5g,
 is_5g_dengw_kh_3m,
 sx_arpu_avg,
 is_timeout_contract,
 is_no_contract,
 is_contract,
 ship_plan_name,
 ship_plan_lvl,
 is_5g_dengw_kh_6m,
 is_5g_dengw_kh_12m,
 is_banben_up,
 is_5g_sa_open,
 is_overdeal,
 is_high_three,
 is_dengw_yij,
 is_high_one,
 is_high_two, -- 高频高额超套客户
 z_call_days, -- 语音通话主叫天数
 taowai_gprs, --  套外流量
 taowai_gprs_fee, --  套外流量费
 zhuanqu_5g_gprs, -- 5G流量5G专区（MB）
 nvl(dy_flow_m, 0),
 nvl(xmly_flow_m, 0),
 nvl(sjds_flow_m, 0),
 nvl(hfx_flow_m, 0),
 nvl(yx139_flow_m, 0),
 nvl(xxqg_flow_m, 0),
 nvl(wyxw_flow_m, 0),
 nvl(zh_flow_m, 0),
 nvl(same_cust_all_fee, 0),
 nvl(last_same_cust_all_fee, 0),
 nvl(last2_same_cust_all_fee, 0),
 nvl(last3_same_cust_all_fee, 0),
 second_iden_check,
 low_fee,
 totalflow_wifi,
 totalflow_lt,
 totalflow_dx,
 xyd_arpu,
 xyd_lvl,
 count_rkdt, -- 人卡分离实人核验单停
 count_rkdtfj, -- 人卡分离实人核验单停复机
 v_yy_calldur, -- VOLTE语音主叫通话时长
 v_sp_calldur, -- VOLTE视频主叫通话时长
 v_yy_callnum, -- VOLTE语音主叫通话次数
 v_sp_callnum, -- VOLTE视频主叫通话次数
 is_paizhao, -- 2022年价值拍照客户
 is_paizhao_by, -- 2022年价值拍照-保有
 is_paizhao_ls, -- 2022年价值拍照-流失
 snapshot_income, -- 2022年价值拍照客户ARPU
 avg_income, -- 2022年价值拍照客户折后ARPU-实时
 duanxin_5G , -- 5G短信（条）
 xiaoxi_5G , -- 5G消息（条）
 is_panzhen,
 nvl(jituan_co_code, 0),
 syisi_qianzai, -- 疑似潜在
 USE_RES_NUM,
 nvl(c14.sp_gprs_m, 0), -- 视频流量总量/MB
 CASE
     WHEN c20.phone_no IS NOT NULL THEN vol_02
     ELSE '非调研用户'
 END myddy_user,-- 满意度调研用户
 c18.is_5G_taobao_jt, -- 是否5G套包(集团口径)
 NVL(c21.gprs_month_VALUE, 0), -- 指定流量资源包-当月生效档位
 NVL(c21.gprs_month_fee, 0), -- 指定流量资源包-当月生效费用(出账)
 NVL(c21.call_month_VALUE, 0), -- 指定语音资源包-当月生效档位
 NVL(c21.call_month_fee, 0), -- 指定语音资源包-当月生效费用(出账)
 NVL(c6.next_FEATURE_VALUE, 0), -- 下月生效主套餐档位
 NVL(c21.next_gprs_VALUE, 0), -- 指定流量资源包-下月生效档位
 NVL(c21.next_call_VALUE, 0), -- 指定语音资源包-下月生效档位
 NVL(c6.next_FEATURE_VALUE, 0)-NVL(c22.next_zhu_zk_fee, 0) next_FEATURE_VALUE_zk, -- 下月生效主套餐档位(剔除折扣产 品)
 NVL(c21.next_gprs_VALUE, 0)-NVL(c22.next_gprs_zk_fee, 0) next_gprs_VALUE_zk, -- 指定流量资源包-下月生效档位(剔除折扣产品)
 NVL(c21.next_call_VALUE, 0)-NVL(c22.next_call_zk_fee, 0) next_call_VALUE_zk, -- 指定语音资源包-下月生效档位(剔除折扣产品)
 c2201.is_chunxz_m,
 c2201.is_xlxz_m,
 c2201.is_chunxz_y,
 c2201.is_xlxz_y,
 CASE
     WHEN c2202.user_id IS NOT NULL THEN 1
     ELSE 0
 END is_xinzeng_user, -- 是否当月新增用户（新增质量日报口径）
 c23.cell_num , -- 当月语音主叫基站个数
 c23.imei_num , -- 当月语音主叫终端个数
 c23.b_opp_rule_no_num , -- 当月被叫对端号码个数
 c23.z_opp_rule_no_num , -- 当月主叫对端号码个数
 c23.z_opp_rule_no_ls , -- 当月主叫对端号码离散度
 c23.z_cell_id_ls , -- 当月主叫基站离散度
 nvl(c24.DEPT_COUNTY_ID, 0) , -- 2022重拍照归属分公司
 c24.MKT_REGION_CNTR , -- 2022重拍照经营网格
 c24.grid_id , -- 2022重拍照经分网格
 c23.SHOULD_fee , -- 出账收入（一经口径）
 CASE
     WHEN c25.product_no IS NOT NULL THEN 1
     ELSE 0
 END is_xinzeng_user_y, -- 是否当年新增用户-新增质量日报口径
 c23.arpu_avg, -- 前三月折前ARPU均值（手厅5G金币预存换机）
 c23.is_tongxin_user_new, -- 是否通信客户（分公司考核）
 CASE
     WHEN c26.user_id IS NOT NULL THEN 1
     ELSE 0
 END is_zhicha_user, -- 是否网络质差用户
 c27.is_lan_rh_user, -- 名下是否有移动宽带
 c27.is_shenzx_user, -- 是否神州行用户（一经口径）
 c27.chl_lvl1, -- 一级归类（发卡）-新增质量日报口径
 c27.chl_lvl2, -- 二级归类（发卡）-新增质量日报口径
 c27.voice, -- 语音质差次数
 c27.shangwang, -- 上网质差次数
 c27.is_dll ,-- 是否大流量客户
 c27.is_sjd_user, -- 是否升降档客户
 c27.is_sd_user, -- 是否升档客户
 c27.is_jd_user, -- 是否降档客户
 c27.is_myd_user, -- 是否满意度重点关注客户-移动业务
 c28.Z_CALL_DUR AS Z_CALL_DUR_avg3, -- 近3月平均主叫通话时长
 c28.CALL_DUR AS CALL_DUR_avg3, -- 近3月平均通话时长
 c28.total_flow AS gprs_avg3, -- 近3月平均gprs流量（kb）
 c28.GN_GPRS, -- gprs国内漫游流量占比
 c28.BD_GPRS, -- gprs本地流量占比
 c28.is_shipin_user, -- 是否视频客户活跃客户
 c29.bend_4G_GPRS , -- 本地4G流量(MB)
 c29.bend_5G_GPRS , -- 本地5G流量(MB)
 c29.manru_4G_GPRS , -- 国内漫游4G流量(MB)
 c29.manru_5G_GPRS , -- 国内漫游5G流量(MB)
 nvl(c14.ysj_flow_d, 0) , -- 云手机流量（MB）
 c30.voc_out_fee , -- 语音结出费用
 c30.gprs_out_fee, -- 流量结出费用
 c31.hldd_fhy_fee , -- 好礼多多非会员版低消金额
 c31.hldd_fhy_name, -- 好礼多多非会员版策划名称
 c31.hldd_hy_fee, -- 好礼多多会员版低消金额
 c31.hldd_hy_name, -- 好礼多多会员版策划名称
 c31.is_pyear_zgd_user, -- 是否上年度中高端拍照客户
 c32.skczt, -- 双卡槽状态
 c34.arup_zh,-- 出账大于0用户折后arpu
 c34.user_id_tx, -- 出账大于0且通信客户
 c34.lj_fact_fee,-- 全年累计平均折后arpu
 c34.avg_arpu_2023, -- 用户全年月均平均收入（月均折后arpu）-2023年
 c34.avg_arpu_2024, -- 全年月均平均收入
 c34.flag , -- 等效客户档位
 c34.if_dx_user -- 等效移动客户
FROM gbasedwi.DWI_USR_PESN_PARTINFO_MS_${monthid} a
LEFT JOIN dm.DM_PUB_INCREASE_${monthid} a1 ON a.phone_no=a1.product_no
LEFT JOIN dm.DM_AUTORPT_CUST_${monthid} a2 ON a.phone_no=a2.product_no -- left join dm.DM_PUB_INCREASE_01_${monthid} a3 on a.phone_no=a3.product_no
LEFT JOIN dm.tmp_pub_2021_add_${monthid} b ON a.phone_no=b.phone_no
LEFT JOIN dm.tmp_pub_2021_add_01_${monthid} c ON a.phone_no=c.phone_no
LEFT JOIN dm.tmp_pub_2021_add_02_${monthid} c2 ON a.phone_no=c2.phone_no
LEFT JOIN dm.tmp_pub_2021_add_03_${monthid} c3 ON a.phone_no=c3.phone_no
LEFT JOIN dm.tmp_pub_2021_add_04_${monthid} c4 ON a.phone_no=c4.phone_no
LEFT JOIN dm.tmp_pub_2021_add_05_${monthid} c5 ON a.phone_no=c5.phone_no
LEFT JOIN dm.tmp_pub_2021_add_06_${monthid} c6 ON a.phone_no=c6.product_no
LEFT JOIN dm.tmp_pub_2021_add_07_${monthid} c7 ON a.phone_no=c7.phone_no
LEFT JOIN dm.tmp_pub_2021_add_08_${monthid} c8 ON a.phone_no=c8.phone_no
LEFT JOIN dm.tmp_pub_2021_add_09_${monthid} c9 ON a.phone_no=c9.phone_no
LEFT JOIN dm.tmp_pub_2021_add_10_${monthid} c10 ON a.phone_no=c10.phone_no
LEFT JOIN dm.tmp_pub_2021_add_11_${monthid} c11 ON a.phone_no=c11.phone_no
LEFT JOIN dm.tmp_pub_2021_add_12_${monthid} c12 ON a.phone_no=c12.phone_no
LEFT JOIN dm.tmp_pub_2021_add_13_${monthid} c13 ON a.phone_no=c13.phone_no
LEFT JOIN dm.tmp_pub_2021_add_14_${monthid} c14 ON a.phone_no=c14.phone_no
LEFT JOIN dm.tmp_pub_2021_add_15_${monthid} c15 ON a.phone_no=c15.phone_no
LEFT JOIN dm.tmp_pub_2021_add_16_${monthid} c16 ON a.phone_no=c16.phone_no
LEFT JOIN dm.tmp_pub_2021_add_17_${monthid} c17 ON a.phone_no=c17.phone_no
LEFT JOIN dm.tmp_pub_2021_add_18_${monthid} c18 ON a.phone_no=c18.phone_no
LEFT JOIN dm.tmp_pub_2021_add_19_${monthid} c19 ON a.phone_no=c19.phone_no
LEFT JOIN dm.dm_satisfaction_user_ms_${monthid} c20 ON a.phone_no=c20.phone_no
LEFT JOIN dm.tmp_pub_2021_add_20_${monthid} c21 ON a.phone_no=c21.phone_no
LEFT JOIN dm.tmp_pub_2021_add_21_${monthid} c22 ON a.phone_no=c22.phone_no
LEFT JOIN dm.tmp_pub_2021_add_22_${monthid} c2201 ON a.user_id=c2201.user_id
LEFT JOIN gbaserpt.nq_201806383_002_${curmlastday} c2202 ON a.user_id=c2202.user_id
LEFT JOIN dm.tmp_pub_2021_add_23_${monthid} c23 ON a.phone_no=c23.phone_no
LEFT JOIN
  (SELECT *
   FROM dim_dwi_usr_pesn_persn_paizhao_year_2022_Y@dblink_dm) c24 ON a.phone_no=c24.phone_no
AND a.user_id=c24.user_id -- 20230106日备份2022重拍照属地化表至小集群 create table dm.dim_dwi_usr_pesn_persn_paizhao_year_2022_y
LEFT JOIN dm_pub_2021806383_xinzeng_user_ys_${YEAR} c25 ON a.phone_no=c25.product_no
LEFT JOIN
  (SELECT DISTINCT user_id
   FROM dm.dm_zhicha_users_top165w_ms_${monthid}) c26 ON a.user_id=c26.user_id
LEFT JOIN dm.tmp_pub_2021_add_24_${monthid} c27 ON a.phone_no=c27.phone_no
LEFT JOIN dm.tmp_pub_2021_add_25_${monthid} c28 ON a.phone_no=c28.phone_no
LEFT JOIN dm.tmp_pub_2021_add_26_${monthid} c29 ON a.phone_no=c29.phone_no
LEFT JOIN dm.tmp_pub_2021_add_27_${monthid} c30 ON a.phone_no=c30.phone_no
LEFT JOIN dm.tmp_pub_2021_add_28_${monthid} c31 ON a.phone_no=c31.phone_no
LEFT JOIN gbasemcd.dw_cocnew_label_cmc_zhuka_new_${monthid} c32 ON a.phone_no=c32.product_no
LEFT JOIN dm.tmp_pub_2021_add_31_1_${monthid} c34 ON a.phone_no=c34.phone_no
WHERE (a.MONTH_ARRIVE_FLAG=1
       OR a.MONTH_OFF_FLAG =1)
  AND a.PROD_KIND_CODE=171000000001;