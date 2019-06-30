select
to_char(to_date(month,'YYYY-MM'),'Mon YYYY') as date,
business_entry.category,
SUM(U.debit) as amount
from (
select to_char(report_date, 'YYYY-MM') as month, debit, business
from credit_entry
where user_id = <userid>
union
select to_char(date, 'YYYY-MM') as month, debit, business
from bank_entry
where hide = 0
and user_id = <userid>
)
as U
inner join business_entry on business_entry.id = U.business
where debit > 0
and business_entry.user_id = <userid>
and business_name <> '__TOTAL__'
group by category, month
order by month,category asc
