select 
extract (MONTH from date) as month,
extract (YEAR from date) as year,
max(balance) as balance
from data_entry
group by month,year
order by year, month

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

select 
to_char(to_date(month,'YYYY-MM'),'Mon YYYY') as monthName,
monthlycredit,
monthlydebit,
(monthlycredit-monthlydebit) as savings
from 
(select 
to_char(date, 'YYYY-MM') as month,
sum(credit) as monthlycredit,
sum(debit) as monthlydebit
from data_entry
group by month
order by month) as A

select * from data_entry where to_char(date, 'YYYY-MM') = '2018-04'