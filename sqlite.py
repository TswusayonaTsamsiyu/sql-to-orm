import sqlite3
from functools import partial
from typing import List, Tuple, Any


def run_sql(sql: str) -> List[Tuple[Any]]:
    conn = sqlite3.connect('chinook.db')
    return conn.execute(sql).fetchall()


CANADIAN_INVOICES_SQL = """
select InvoiceDate, BillingAddress
from invoices
where strftime('%Y', InvoiceDate) between '2012' and '2013'
  and BillingCountry = 'Canada';"""

LOYAL_CUSTOMERS_SQL = """
select c.FirstName, c.LastName, c.Email, sum(i.Total) as total
from customers c
join invoices i on c.CustomerId = i.CustomerId
group by c.CustomerId
order by total desc
limit 10;"""

RAISE_POPULAR_ALBUMS_SQL = """
with popular as (select a.AlbumId
                 from albums a
                 join tracks t on a.AlbumId = t.AlbumId
                 join invoice_items i on t.TrackId = i.TrackId
                 group by a.AlbumId
                 having count(*) > 10)
update tracks
set UnitPrice = UnitPrice * 1.05
where AlbumId in popular;"""

get_canadian_invoices = partial(run_sql, CANADIAN_INVOICES_SQL)
get_most_loyal = partial(run_sql, LOYAL_CUSTOMERS_SQL)
raise_popular_albums = partial(run_sql, RAISE_POPULAR_ALBUMS_SQL)
