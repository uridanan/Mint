select U.date,U.ref_id,U.debit,business_entry.marketing_name, business_entry.category
from (
select report_date as date, business,card_number as ref_id,debit
from credit_entry
where to_char(report_date, 'YYYY-MM') = '2018-04'
union
select date, business, ref_id, debit
from bank_entry
where to_char(date, 'YYYY-MM') = '2018-04'
and hide = 0
)
as U
inner join business_entry on business_entry.id = U.business
where debit > 0
and business_name <> '__TOTAL__'
order by date asc