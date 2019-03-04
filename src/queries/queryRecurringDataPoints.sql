select * from
(select to_char(date,'Mon YYYY') as monthName, tracker_id, debit from bank_entry where tracker_id > 0
union
select to_char(report_date,'Mon YYYY') as monthName, tracker_id, debit from credit_entry where tracker_id > 0) as U
order by U.monthName, U.tracker_id