-- Recurring expenses by amount are only relevant on the bank account
-- Recurring expenses by amount are only relevant for checks
-- Everything else will also be recurring by business

UPDATE bank_entry
SET tracker_id = <tracker>
WHERE business IN (SELECT id FROM business_entry WHERE marketing_name ~ '.*check.*')
AND debit = <amount>
