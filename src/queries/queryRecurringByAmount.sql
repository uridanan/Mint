-- Recurring expenses by amount are only relevant on the bank account
-- Recurring expenses by amount are only relevant for checks
-- Everything else will also be recurring by business

SELECT debit, COUNT(*), min(date) as first, max(date) as last
FROM bank_entry as BA
INNER JOIN business_entry as BU ON BU.id = BA.business
WHERE (marketing_name ~ '.*check.*') AND BA.user_id = <userid>
GROUP BY debit
HAVING COUNT(*) > 3
