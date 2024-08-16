
--1 最后字段不是为字段名的。
DROP TABLE tmp_dm_20130916_06;

\
CREATE TABLE tmp_dm_20130916_06\ (product_no varchar(20),\ gprs_monthly_fee decimal(12, 2), -- 流量出账-月租费\
 gprs_gasbag_fee decimal(12, 2), -- 流量出账-加油包费\
 gprs_flow_fee decimal(12, 2), -- 流量出账-流量费\
 gprs_wlan_fee decimal(12, 2), -- 流量出账-WLAN\
 gprs_yearhalfyear_fee decimal(12, 2), -- 流量出账-年包半年包\
 gprs_quarter_fee decimal(12, 2), -- 流量出账-季包\
 gprs_payment_fee decimal(12, 2), -- 流量出账-流量统付\
 gprs_direct_fee decimal(12, 2), -- 流量出账-流量直充\
 gprs_infinite_fee decimal(12, 2), -- 流量出账-不限量\
 gprs_personality_fee decimal(12, 2), -- 流量出账-个性化\
 gprs_national_fee decimal(12, 2), -- 流量出账-国漫套餐\
 gprs_unified_fee decimal(12, 2), -- 流量出账-统付\
 day_fee decimal(12, 2), -- 流量出账\
 user_4gnet_flag smallint,\ offer_bracket bigint ,\ last_offer_bracket bigint\) distributed BY ('product_no');

","parentDsName":"GbaseDM