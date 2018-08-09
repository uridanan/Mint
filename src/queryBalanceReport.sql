select
to_char(to_date(month,'YYYY-MM'),'Mon YYYY') as monthName,
balance
from
(select
to_char(date, 'YYYY-MM') as month,
max(balance) as balance
from data_entry
group by month
order by month) as A