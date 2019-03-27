select id, name, Start, Stop, Occurences, Average, Minimum, Maximum from recurrent_expense
inner join
(
select tracker_id, to_char(MIN(monthName),'Mon DD, YYYY') as Start, to_char(MAX(monthName), 'Mon DD, YYYY') as Stop,  COUNT(debit) as Occurences, AVG(debit) as Average, MIN(debit) as Minimum, MAX(debit) as Maximum from
(select date as monthName, tracker_id, debit from bank_entry where tracker_id > 0
union
select report_date as monthName, tracker_id, debit from credit_entry where tracker_id > 0) as U
where U.monthName > to_date(<start>,'Mon YYYY')
and U.monthName <  to_date(<stop>,'Mon YYYY')
group by tracker_id
) as Q on Q.tracker_id = id

