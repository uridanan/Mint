select * from
(
select R.business, R.count, business_entry.marketing_name, be.id, be.date, be.credit, be.debit
from
(SELECT
    business, COUNT(*)
FROM
    bank_entry
GROUP BY
    business
HAVING
    COUNT(*) > 3
) as R
inner join business_entry on business_entry.id = R.business
inner join bank_entry as be on business_entry.id = be.business
UNION
select R.business, R.count, business_entry.marketing_name, ce.id, ce.report_date as date, ce.credit, ce.debit
from
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
) as U
order by business, date
/*-----------------*/



select * from
(SELECT
    business, COUNT(*)
FROM
    bank_entry
GROUP BY
    business
HAVING
    COUNT(*) > 3
) as R
inner join business_entry on business_entry.id = R.business
inner join bank_entry as be on business_entry.id = be.business
order by be.business, date


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


select * from
(SELECT
    debit, COUNT(*)
FROM
    credit_entry
GROUP BY
    debit
HAVING
    COUNT(*) > 3
) as R
inner join credit_entry as be on r.debit = be.debit
inner join business_entry on business_entry.id = be.business
order by be.debit, report_date