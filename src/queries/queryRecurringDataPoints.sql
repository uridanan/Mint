select U.monthName, U.tracker_id, U.debit from
(select to_char(date,'YYYYMM') as month, to_char(date,'Mon YYYY') as monthName, tracker_id, debit from bank_entry where tracker_id > 0 and user_id = <userid>
union
select to_char(report_date,'YYYYMM') as month, to_char(report_date,'Mon YYYY') as monthName, tracker_id, debit from credit_entry where tracker_id > 0 and user_id = <userid>) as U
order by U.month, U.tracker_id