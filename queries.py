from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func, desc, create_engine

from orm import Track, Album, Customer, Invoice, InvoiceItem


def get_canadian_invoices():
    return select(Invoice.InvoiceDate, Invoice.BillingAddress).where(
        and_(
            func.strftime('%Y', Invoice.InvoiceDate).between('2012', '2013'),
            Invoice.BillingCountry == 'Canada'
        )
    )


def get_most_loyal():
    return (
        select(Customer, func.sum(Invoice.Total).label('total'))
        .join(Invoice)
        .group_by(Customer.CustomerId)
        .order_by(desc('total'))
        .limit(10)
    )


def get_popular_albums():
    return (
        select(Album)
        .join(Track)
        .join(InvoiceItem)
        .group_by(Album.AlbumId)
        .having(func.count() > 10)
    )


def get_popular_album_tracks():
    return select(Track).join(get_popular_albums().subquery())


def raise_popular_albums(session_):
    for track in session_.scalars(get_popular_album_tracks()):
        track.UnitPrice *= 1.05
    session_.commit()


def main():
    engine = create_engine('sqlite:///C:/Users/Gabi/Downloads/chinook.db')
    with Session(engine) as session:
        for row in session.execute(get_canadian_invoices()):
            print(row)
        for row in session.execute(get_most_loyal()):
            print(row)
        for row in session.scalars(get_popular_album_tracks()):
            print(row)
        raise_popular_albums(session)


if __name__ == '__main__':
    main()
