-- uses report date, should I be using purchase date instead?
-- Skip entries identified as checks
select * from
(
select R.business, R.count, business_entry.marketing_name, avg(be.debit), min(be.debit), max(be.debit), min(be.date) as first, max(be.date) as last
from
(SELECT
    business, COUNT(*)
FROM
    bank_entry
WHERE
    debit > 0
GROUP BY
    business
HAVING
    COUNT(*) > 3
) as R
inner join business_entry on business_entry.id = R.business
inner join bank_entry as be on business_entry.id = be.business
AND (marketing_name !~ '.*check.*')
group by R.business, R.count, business_entry.marketing_name
UNION
select R.business, R.count, business_entry.marketing_name, avg(ce.debit), min(ce.debit), max(ce.debit), min(ce.report_date) as first, max(ce.report_date) as last
from
(SELECT
    business, COUNT(*)
FROM
    credit_entry
WHERE
    debit > 0
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