select * from bank_entry
select * from credit_entry
select * from business_entry



select c.id, c.debit, b.id, b.debit, b,hide from credit_entry c, bank_entry b
where c.debit = b.debit
and c.bank_id = b.ref_id


select * from bank_entry where hide=1
select * from bank_entry order by "id"