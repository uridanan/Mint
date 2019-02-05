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

/* uses report date, should I be using purchase date instead? */


select * from
(
select R.business, R.count, business_entry.marketing_name, avg(be.debit), min(be.debit), max(be.debit), min(be.date), max(be.date)
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
group by R.business, R.count, business_entry.marketing_name
UNION
select R.business, R.count, business_entry.marketing_name, avg(ce.debit), min(ce.debit), max(ce.debit), min(ce.report_date), max(ce.report_date)
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
group by R.business, R.count, business_entry.marketing_name
) as U
order by business