select * from
(select re.id, re.name, re.business_id, re.amount, re.type, re.count, re.start_date, re.last_date, re.avg_amount, re.max_amount, re.min_amount, be.date, be.debit from recurrent_expense as re
inner join bank_entry as be on be.tracker_id = re.id
union
select re.id, re.name, re.business_id, re.amount, re.type, re.count, re.start_date, re.last_date, re.avg_amount, re.max_amount, re.min_amount, be.report_date as date, be.debit from recurrent_expense as re
inner join credit_entry as be on be.tracker_id = re.id) as U
order by U.id, U.date


select * from
(select re.id, re.name, be.date, be.debit from recurrent_expense as re
inner join bank_entry as be on be.tracker_id = re.id
union
select re.id, re.name, be.report_date as date, be.debit from recurrent_expense as re
inner join credit_entry as be on be.tracker_id = re.id) as U
order by U.id, U.date