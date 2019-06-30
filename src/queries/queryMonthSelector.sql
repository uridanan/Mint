select
to_char(to_date(month,'YYYY-MM'),'Mon YYYY') as monthName,
month
from
(select distinct
to_char(date, 'YYYY-MM') as month
from bank_entry
where user_id = <userid>
UNION
select distinct
to_char(report_date, 'YYYY-MM') as month
from credit_entry
where user_id = <userid>
) as U
order by month desc