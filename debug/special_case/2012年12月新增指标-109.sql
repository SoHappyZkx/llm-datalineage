create table  ${DM_PUB_201212018_TMP14_MONTHID}
    (   phone_no               varchar(20)
    ,IS_CHANGE_USIM                    SMALLINT
    ,IS_HANDLE_4G        SMALLINT
    ,IS_TERMINAL_4G     SMALLINT
    ,IS_MIFI_4G                SMALLINT
    ,TERMINAL_4G           varchar(800)
    ,IS_TEST_4G              SMALLINT
    ) DISTRIBUTED BY('phone_no') nolock;