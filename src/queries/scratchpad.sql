select * from bank_entry
select * from credit_entry
select * from business_entry



select c.id, c.debit, b.id, b.debit, b,hide from credit_entry c, bank_entry b
where c.debit = b.debit
and c.bank_id = b.ref_id


select * from bank_entry where hide=1
select * from bank_entry order by "id"


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

SELECT * from daterange('2010-01-01 14:30', '2010-01-05 15:30')

select * from credit_entry order by card_number

select * from (
SELECT business, count(business) as recurs from bank_entry group by business
) as A where recurs > 2


SELECT
    debit, COUNT(*)
FROM
    bank_entry
GROUP BY
    debit
HAVING
    COUNT(*) > 3


select * from
(SELECT
    debit, COUNT(*)
FROM
    bank_entry
GROUP BY
    debit
HAVING
    COUNT(*) > 3
) as R
inner join bank_entry as be on r.debit = be.debit
inner join business_entry on business_entry.id = be.business
order by be.debit, date



select * from bank_entry where business = 107


select * from
(SELECT
    business, COUNT(*)
FROM
    credit_entry
GROUP BY
    business
HAVING
    COUNT(*) > 3
) as R
inner join business_entry on business_entry.id = R.business
inner join credit_entry as ce on business_entry.id = ce.business
order by ce.business, report_date