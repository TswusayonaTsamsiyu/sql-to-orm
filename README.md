# SQL -> ORM
A small exercise for converting SQL queries to SQLAlchemy queries.

The sample DB is `chinook.db`. There is an ORM template in `orm.py`. Your code should be written in `queries.py`.

The queries to be converted are:
```sql
select InvoiceDate, BillingAddress
from invoices
where strftime('%Y', InvoiceDate) between '2012' and '2013'
  and BillingCountry = 'Canada';
```
```sql
select c.FirstName, c.LastName, c.Email, sum(i.Total) as total
from customers c
join invoices i on c.CustomerId = i.CustomerId
group by c.CustomerId
order by total desc
limit 10;
```
```sql
with popular as (select a.AlbumId
                 from albums a
                 join tracks t on a.AlbumId = t.AlbumId
                 join invoice_items i on t.TrackId = i.TrackId
                 group by a.AlbumId
                 having count(*) > 10)
update tracks
set UnitPrice = UnitPrice * 1.05
where AlbumId in popular;
```
