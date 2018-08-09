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