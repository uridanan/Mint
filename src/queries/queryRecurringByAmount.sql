-- Recurring expenses by amount are only relevant on the bank account
-- On credit cards, they will also be recurring by business

select min(be.business), R.count, '', be.debit, min(be.date) as first, max(be.date) as last
from
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
group by be.debit, R.count
order by be.debit desc


--select * from
--(SELECT
--    debit, COUNT(*)
--FROM
--    credit_entry
--GROUP BY
--    debit
--HAVING
--    COUNT(*) > 3
--) as R
--inner join credit_entry as be on r.debit = be.debit
--inner join business_entry on business_entry.id = be.business
--order by be.debit, report_date

