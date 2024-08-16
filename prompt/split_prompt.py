
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
llmodel_dir = os.path.join(root_dir, 'llmodel')
sys.path.append(root_dir)
sys.path.append(llmodel_dir)

from llmodel import llmapi
sql_code = '''
insert into DM_PUB_20191202_${dayid}
    select '${day_id}',
    t.phone_no,
    nvl(t1.is_xc,0),
    t1.port_out_time,
    t1.PORT_IN_NET_NAME,
    nvl(t2.is_xr,0),
    t2.port_in_time,
    t2.port_out_net_name,
    nvl(xr_days,0),
    t3.org_id,
    parent_org_id,
    chl_name,
    county_name,
    nvl(is_dx_day,0),
    nvl(is_dx_month,0),
    nvl(is_hr_day,0),
    nvl(is_hr_month,0),
    nvl(is_yyt_day,0),
    nvl(is_yyt_month,0),
    nvl(is_sq_day,0),
    nvl(is_sq_month,0),
    nvl(is_hq_day,0),
    nvl(is_hq_month,0),
    nvl(lvl_name,'不详'),
    nvl(t6.rc_id,0),
    t7.co_grid,
    t7.co_regional,
    t7.co_begin_time,
    trans_amt,
    mt_should_income,
    is_top25_lius,
    is_top25_lius2,
    is_top25_lius3,
    is_top25_lius4,
    is_top25_lius5,
    is_shengdang,
    is_jiangdang,
    is_pingdang,
    top40_01,
    top40_02,
    top40_03,
    top40_04,
    top40_05,
    top40_06,
    top40_07,
    top40_08,
    top40_09,
    trans_amt as trans_amt1,
    is_5g_zd_yj   ,  
    is_jt_yt   ,  
    is_5g_new_add   ,  
    is_5g_zd   ,  
    is_dgdd_user,   
    is_5g_plan_jt,  
    is_5g_plan_bd,   
    is_zh_sjd,  
    plan_fee_zh_jj,
    is_5g_wl_user, 
    paz_zhe_arpu , 
    paz_zhe10_arpu , 
    paz_zhe11_arpu  , 
    paz_zhe12_arpu , 
    is_zb_25 , 
    is_zb_40,  
    jif_bt_fee   ,   
    m_no_jif_bt_fee   ,   
    migu_fee,    
    new_add,
    nvl(t17.sms_cxzd_cnt,0),
    nvl(t17.sms_cxye_cnt,0),
    nvl(t17.sms_cxtc_cnt,0),
    nvl(t17.sms_cxxj_cnt,0),
    nvl(is_5g_dengw,0),
    nvl(flow_5g,0),
    nvl(total_flow,0),
    nvl(votel_total_flow,0),
    nvl(is_5g_open,0),
    nvl(open_5g_days,0),
    nvl(land_roam_days,0),
    nvl(is_tongxin_yj,0),
    nvl(is_tongxin_mnyj,0),
    nvl(is_chuzhang_mnyj,0),
    nvl(is_5g_jtwpp_county,0),
    nvl(is_2021pz_baoyou_user,0),
    nvl(is_2021pz_liushi_user,0),
    nvl(arpu_2021pz_jz,0),
    nvl(is_5g_dengw_bend,0),
    onetofive_fee,
    last_onetofive_fee,
    last2_onetofive_fee,
    last_3onetofive_fee,
    hcy_flow_m,
    ykl_flow_m,
    is_5gsa_dengw,
    is_2021_pz_user_new,
    is_2021_by_user_new,
    is_2021_ls_user_new,
    pz_user_new_arpu,
    USER_VIDEO_REGISTER,
    nvl(is_chyj_user_new,0),
    nvl(is_shuzi_quanyi_user,0),
    freeze_fee,  
    no_freeze_fee,  
    addr_id,     
    addr_imei ,        
    is_5g_dengw_kh,
    is_all_manyou,
    is_30_85_call,
    is_60_85_call,
    is_30_86_call,
    is_60_86_call,
    is_tongxin_user,
    zk_name,   
    new_plan_id,   
    new_plan_name,  
    plan_fee_new,  
    credit_sum,  
    credit_date,  
    is_kdzjzt,  
    is_jkwfg ,     
    t16.msm_should_fee_ft, 
from gbasedwi.dwi_usr_pesn_partinfo_ds_${dayid} t
left join tmp_20191202_01_${dayid} t1 on t.phone_no=t1.product_no
left join tmp_20191202_02_${dayid} t2 on t.phone_no=t2.product_no
left join tmp_20191202_03_${dayid} t3 on t.phone_no=t3.product_no
left join tmp_20191202_04_${dayid} t4 on t.phone_no=t4.product_no
left join tmp_20191202_05_${dayid} t5 on t.phone_no=t5.product_no
left join tmp_20191202_06_${dayid} t6 on t.phone_no=t6.product_no
left join tmp_20191202_07_${dayid} t7 on t.phone_no=t7.product_no
left join tmp_20191202_08_${dayid} t8 on t.phone_no=t8.product_no
left join tmp_20191202_09_${dayid} t9 on t.phone_no=t9.product_no
left join tmp_20191202_10_${dayid} t10 on t.phone_no=t10.product_no
left join tmp_20191202_11_${dayid} t11 on t.phone_no=t11.product_no
left join tmp_20191202_12_${dayid} t12 on t.phone_no=t12.product_no
left join tmp_20191202_13_${dayid} t13 on t.phone_no=t13.product_no
left join tmp_20191202_14_${dayid} t14 on t.phone_no=t14.product_no
left join tmp_20191202_15_${dayid} t15 on t.phone_no=t15.product_no
left join tmp_20191202_16_${dayid} t16 on t.user_id=t16.user_id
left join tmp_20191202_17_${dayid} t17 on t.phone_no=t17.product_no
left join tmp_20191202_18_${dayid} t18 on t.phone_no=t18.product_no
left join tmp_20191202_19_${dayid} t19 on t.phone_no=t19.product_no
left join tmp_20191202_20_${dayid} t20 on t.phone_no=t20.product_no
left join dm_20191202_21_${dayid} t21 on t.phone_no=t21.product_no
left join tmp_20191202_22_${dayid} t22 on t.phone_no=t22.product_no
left join tmp_20191202_23_${dayid} t23 on t.phone_no=t23.product_no
left join tmp_20191202_24_${dayid} t24 on t.phone_no=t24.product_no
left join tmp_20191202_25_${dayid} t25 on t.phone_no=t25.product_no
left join tmp_20191202_26_${dayid} t26 on t.phone_no=t26.product_no
left join tmp_20191202_27_${dayid} t27 on t.phone_no=t27.product_no
left join tmp_20191202_28_${dayid} t28 on t.phone_no=t28.product_no
left join tmp_20191202_29_${dayid} t29 on t.phone_no=t29.product_no
where t.prod_kind_code='171000000001' and (t.month_arrive_flag = 1 or t.month_off_flag = 1 or t.month_new_flag = 1);
'''
#这个太长了 可能输出也不够
#prompt = f"请你帮我把下面这段sql代码中所有的字段都取出来。格式是table_name.field_name, 以逗号分隔。sql代码为：\"\"\"{sql_code}\"\"\""

#试试这个
prompt = f"请你帮我把下面这段sql代码中的被create或者insert的表中，第一个字段提出来，并且给出所有和这个字段相关的代码，不涉及的就不需要。输出格式是 table_name.field_name: field_sql_code。 这段sql代码是：\"\"\"{sql_code}\"\"\""
'''
DM_PUB_20191202_${dayid}.phone_no: left join DM_PUB_20191202_${dayid} t on t.phone_no=t.product_no
tmp_20191202_01_${dayid}.product_no: left join tmp_20191202_01_${dayid} t1 on t.phone_no=t1.product_no
tmp_20191202_02_${dayid}.product_no: left join tmp_20191202_02_${dayid} t2 on t.phone_no=t2.product_no
tmp_20191202_03_${dayid}.product_no: left join tmp_20191202_03_${dayid} t3 on t.phone_no=t3.product_no
'''

filepath = "F:\\GITClone\\CMCCtest\\dateline\\config\\llm_conf.yaml"
API_KEY = "sk-fbd56500a79e44a79ceaae02d567f25e"
PLATFORM = "qwen".upper()
model_name = "qwen-turbo"
system_prompt = "你是一个非常重要聪明有用的助手"
#question = "你是谁？"
client = llmapi.init_client(API_KEY,PLATFORM)
answer_content, finish_reason, completion_tokens,prompt_tokens,total_tokens = llmapi.get_response(client, model_name, system_prompt, prompt)
print(answer_content)
print(completion_tokens,prompt_tokens,total_tokens)