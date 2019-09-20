select * from bank_entry
select * from credit_entry
select * from business_entry
select * from recurrent_expense
select * from file_entry

delete from file_entry

select * from business_entry where marketing_name like '%check%'

select c.id, c.debit, b.id, b.debit, b,hide from credit_entry c, bank_entry b
where c.debit = b.debit
and c.bank_id = b.ref_id


select * from bank_entry where hide=1
select * from bank_entry order by "id"


select U.date,U.ref_id,U.debit,business_entry.marketing_name, business_entry.category
from (
select report_date as date, business,card_number as ref_id,debit
from credit_entry
where to_char(report_date, 'YYYY-MM') = '2018-04'
union
select date, business, ref_id, debit
from bank_entry
where to_char(date, 'YYYY-MM') = '2018-04'
and hide = 0
)
as U
inner join business_entry on business_entry.id = U.business
where debit > 0
and business_name <> '__TOTAL__'
order by date asc

SELECT * from daterange('2010-01-01 14:30', '2010-01-05 15:30')

select * from credit_entry order by card_number

select * from (
SELECT business, count(business) as recurs from bank_entry group by business
) as A where recurs > 2


SELECT
    debit, COUNT(*)
FROM
    bank_entry
GROUP BY
    debit
HAVING
    COUNT(*) > 3


select * from
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
order by be.debit, date



select * from bank_entry where business = 107


select * from
(SELECT
    business, COUNT(*)
FROM
    credit_entry
GROUP BY
    business
HAVING
    COUNT(*) > 3
) as R
inner join business_entry on business_entry.id = R.business
inner join credit_entry as ce on business_entry.id = ce.business
order by ce.business, report_date


select * from
(select re.id, re.name, re.business_id, re.amount, re.type, re.count, re.start_date, re.last_date, re.avg_amount, re.max_amount, re.min_amount, be.date, be.debit from recurrent_expense as re
inner join bank_entry as be on be.tracker_id = re.id
union
select re.id, re.name, re.business_id, re.amount, re.type, re.count, re.start_date, re.last_date, re.avg_amount, re.max_amount, re.min_amount, be.report_date as date, be.debit from recurrent_expense as re
inner join credit_entry as be on be.tracker_id = re.id) as U
order by U.id, U.date



select id, name, Start, Stop, Occurences, Average::numeric(16,2), Minimum::numeric(16,2), Maximum::numeric(16,2) from recurrent_expense
inner join
(
select tracker_id, to_char(MIN(monthName),'Mon DD, YYYY') as Start, to_char(MAX(monthName), 'Mon DD, YYYY') as Stop,  COUNT(debit) as Occurences, AVG(debit) as Average, MIN(debit) as Minimum, MAX(debit) as Maximum from
(select date as monthName, tracker_id, debit from bank_entry where tracker_id > 0
union
select report_date as monthName, tracker_id, debit from credit_entry where tracker_id > 0) as U
where to_date(to_char(U.monthName,'Mon YYYY'),'Mon YYYY') >= to_date('Jan 2018','Mon YYYY')
and to_date(to_char(U.monthName,'Mon YYYY'),'Mon YYYY') <= to_date('Mar 2018','Mon YYYY')
group by tracker_id
) as Q on Q.tracker_id = id



select U.date,U.ref_id,U.debit,
CASE WHEN R.name <> '' THEN R.name ELSE B.marketing_name END as marketing_name,
B.category,U.tracker_id,R.name
from (
select report_date as date, business,card_number as ref_id,debit,tracker_id
from credit_entry
where to_char(report_date, 'YYYY-MM') = '2018-04'
union
select date, business, ref_id, debit,tracker_id
from bank_entry
where to_char(date, 'YYYY-MM') = '2018-04'
and hide = 0
)
as U
inner join business_entry as B on B.id = U.business
inner join recurrent_expense as R on R.id = U.tracker_id
where debit > 0
--and category in (<filter>)
and business_name <> '__TOTAL__'
order by date asc


select U.date,U.ref_id,U.debit, CASE WHEN R.name <> '' THEN R.name ELSE B.marketing_name END as marketing_name, B.category, B.id as business_id, R.id as tracker_id
from (select report_date as date, business,card_number as ref_id,debit,tracker_id
        from credit_entry
        where to_char(report_date, 'YYYY-MM') = '2018-05'
        and user_id = '0'
        union
        select date, business, ref_id, debit,tracker_id
        from bank_entry
        where to_char(date, 'YYYY-MM') = '2018-05'
        and hide = 0
        and user_id = '0') as U
inner join business_entry as B on B.id = U.business
inner join recurrent_expense as R on R.id = U.tracker_id
where debit > 0
and B.user_id = '0'
and R.user_id = '0'
and category in ('')
and business_name <> '__TOTAL__'
order by date asc


select * from
(select to_char(date,'YYYYMM') as month, to_char(date,'Mon YYYY') as monthName, tracker_id, debit from bank_entry where tracker_id > 0 and user_id = '0'
union
select to_char(report_date,'YYYYMM') as month, to_char(report_date,'Mon YYYY') as monthName, tracker_id, debit from credit_entry where tracker_id > 0 and user_id = '0') as U
order by U.month, U.tracker_id



select * from
(select to_char(date,'YYYYMM') as month, to_char(date,'Mon YYYY') as monthName, tracker_id, debit from bank_entry where tracker_id > 0 and user_id = <userid>
union
select to_char(report_date,'YYYYMM') as month, to_char(report_date,'Mon YYYY') as monthName, tracker_id, debit from credit_entry where tracker_id > 0 and user_id = <userid>) as U
order by U.month, U.tracker_id



select id, name, Start, Stop, Occurences,  Average::numeric(16,2), Minimum::numeric(16,2), Maximum::numeric(16,2) from recurrent_expense
inner join
(select tracker_id, to_char(MIN(monthName),'Mon DD, YYYY') as Start, to_char(MAX(monthName), 'Mon DD, YYYY') as Stop,  COUNT(debit) as Occurences, AVG(debit) as Average, MIN(debit) as Minimum, MAX(debit) as Maximum from
(select date as monthName, tracker_id, debit from bank_entry where tracker_id > 0 and user_id = '0'
union
select report_date as monthName, tracker_id, debit from credit_entry where tracker_id > 0 and user_id = '0') as U
where to_date(to_char(U.monthName,'Mon YYYY'),'Mon YYYY') >= to_date('201802','Mon YYYY')
and to_date(to_char(U.monthName,'Mon YYYY'),'Mon YYYY') <=  to_date('201805','Mon YYYY')
group by tracker_id) as Q on Q.tracker_id = id where recurrent_expense.user_id = '0'



select U.id, U.date,U.ref_id,U.debit,
CASE WHEN R.name <> '' THEN R.name ELSE B.marketing_name END as marketing_name, B.category
from (
select report_date as date, business,card_number as ref_id,debit,tracker_id
from credit_entry
where to_char(report_date, 'YYYY-MM') = <month>
and user_id = <userid>
union
select date, business, ref_id, debit,tracker_id
from bank_entry
where to_char(date, 'YYYY-MM') = <month>
and hide = 0
and user_id = <userid>
)
as U
inner join business_entry as B on B.id = U.business
inner join recurrent_expense as R on R.id = U.tracker_id
where debit > 0
and B.user_id = <userid>
and R.user_id = <userid>
and category in (<filter>)
and business_name <> '__TOTAL__'
order by date asc


SELECT debit, COUNT(*), min(date) as first, max(date) as last
FROM bank_entry as BA
INNER JOIN business_entry as BU ON BU.id = BA.business
WHERE (marketing_name ~ '.*check.*') AND BA.user_id = '0'
GROUP BY debit
HAVING COUNT(*) > 3

select count(*) from bank_entry where debit is null