-- Recurring expenses by amount are only relevant on the bank account
-- Recurring expenses by amount are only relevant for checks
-- Everything else will also be recurring by business

UPDATE bank_entry
SET tracker_id = 246 --<tracker>
WHERE business = 2 --<business>

