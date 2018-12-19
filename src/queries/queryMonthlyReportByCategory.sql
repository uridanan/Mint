select business_entry.category, SUM(U.debit) as amount
from (
select report_date as date, business,card_number as ref_id,debit
from credit_entry
where to_char(report_date, 'YYYY-MM') = <month>
union
select date, business, ref_id, debit
from bank_entry
where to_char(date, 'YYYY-MM') = <month>
and hide = 0
)
as U
inner join business_entry on business_entry.id = U.business
where debit > 0
and category in (<filter>)
and business_name <> '__TOTAL__'
group by category
order by amount desc