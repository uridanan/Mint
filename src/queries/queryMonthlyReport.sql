select U.date,U.ref_id,U.debit,
CASE WHEN R.name <> '' THEN R.name ELSE B.marketing_name END as marketing_name, B.category
from (
select report_date as date, business,card_number as ref_id,debit,tracker_id
from credit_entry
where to_char(report_date, 'YYYY-MM') = <month>
union
select date, business, ref_id, debit,tracker_id
from bank_entry
where to_char(date, 'YYYY-MM') = <month>
and hide = 0
)
as U
inner join business_entry as B on B.id = U.business
inner join recurrent_expense as R on R.id = U.tracker_id
where debit > 0
and category in (<filter>)
and business_name <> '__TOTAL__'
order by date asc