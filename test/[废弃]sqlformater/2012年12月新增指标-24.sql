DROP TABLE ${DM_PUB_201212018_TMP05_MONTHID};


create table ${dm_pub_201212018_tmp05_monthid} (product_no varchar(20) , cur_promotion_score bigint , cur_data_score bigint , cur_consume_score bigint , change_score_month bigint , change_score_year bigint , free_flow_all bigint , active_count smallint , gprs_count1 integer , gprs_count2 integer , gprs_count3 integer , gprs_count4 integer , is_4g_user smallint) distributed by('product_no') nolock;
