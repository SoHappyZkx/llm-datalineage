INSERT INTO dm_top25_lost_cause_user456_ms_${monthid}
select a.phone_no, a.start_count, a.end_count, c.b_all
from
(
    select phone_no,start_count, end_count from table1
    where start_count > 30 and end_count < 90
) a
left join 
(
    select phone_call_number, sum(order_count) as b_all from table2
    group by phone_no
) c on a.phone_no=c.phone_call_number
desc order by c.b_all 




#
