select * from
(select re.id, re.name, be.date, be.debit from recurrent_expense as re
inner join bank_entry as be on be.tracker_id = re.id
union
select re.id, re.name, be.report_date as date, be.debit from recurrent_expense as re
inner join credit_entry as be on be.tracker_id = re.id) as U
order by U.id, U.date


select * from
(select date, tracker_id, debit from bank_entry where tracker_id > 0
union
select report_date as date, tracker_id, debit from credit_entry where tracker_id > 0) as U
order by U.date, U.tracker_id

select * from recurrent_expense