select * from
(
select U.date,U.ref_id,U.debit, B.marketing_name as marketing_name, B.category, B.id as business_id, U.tracker_id as tracker_id
from (
select report_date as date, business,card_number as ref_id,debit,tracker_id
from credit_entry
where to_char(report_date, 'YYYY-MM') = <month>
and user_id = <userid>
and tracker_id = 0
and debit > 0
union
select date, business, ref_id, debit,tracker_id
from bank_entry
where to_char(date, 'YYYY-MM') = <month>
and hide = 0
and user_id = <userid>
and tracker_id = 0
and debit > 0
)
as U
inner join business_entry as B on B.id = U.business
and B.user_id = <userid>
and business_name <> '__TOTAL__'
and B.category in (<filter>)
UNION
select U.date,U.ref_id,U.debit,
CASE WHEN R.name <> '' THEN R.name ELSE B.marketing_name END as marketing_name, B.category, B.id as business_id, R.id as tracker_id
from (
select report_date as date, business,card_number as ref_id,debit,tracker_id
from credit_entry
where to_char(report_date, 'YYYY-MM') = <month>
and user_id = <userid>
and tracker_id > 0
and debit > 0
union
select date, business, ref_id, debit,tracker_id
from bank_entry
where to_char(date, 'YYYY-MM') = <month>
and hide = 0
and user_id = <userid>
and tracker_id > 0
and debit > 0
)
as U
inner join business_entry as B on B.id = U.business
inner join recurrent_expense as R on R.id = U.tracker_id
where B.user_id = <userid>
and R.user_id = <userid>
and business_name <> '__TOTAL__'
and B.category in (<filter>)
) as V
order by date asc
