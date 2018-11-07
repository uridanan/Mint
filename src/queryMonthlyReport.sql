select * from (
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
where debit > 0
and length (business) > 0
order by date asc


select c.id, c.debit, b.id, b.debit, b,hide from credit_entry c, bank_entry b
where c.debit = b.debit
and c.bank_id = b.ref_id
