from typing import List

from sqlalchemy import inspect
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def __repr__(self):
        fields = ", ".join(f"{c.key}={getattr(self, c.key)}" for c in inspect(self).mapper.column_attrs)
        return f"{self.__class__.__name__}({fields})"


class Track(Base):
    __tablename__ = 'tracks'

    TrackId: Mapped[int] = mapped_column(primary_key=True)
    UnitPrice: Mapped[float]
    AlbumId: Mapped[int] = mapped_column(ForeignKey("albums.AlbumId"))

    album: Mapped["Album"] = relationship(back_populates="tracks")
    invoices: Mapped[List["InvoiceItem"]] = relationship(back_populates="track")


class Album(Base):
    __tablename__ = 'albums'

    AlbumId: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str]

    tracks: Mapped[List["Track"]] = relationship(back_populates="album")


class Invoice(Base):
    __tablename__ = 'invoices'

    InvoiceId: Mapped[int] = mapped_column(primary_key=True)
    InvoiceDate: Mapped[str]
    BillingAddress: Mapped[str]
    BillingCountry: Mapped[str]
    CustomerId: Mapped[int] = mapped_column(ForeignKey("customers.CustomerId"))
    Total: Mapped[float]

    customer: Mapped["Customer"] = relationship(back_populates="invoices")
    items: Mapped[List["InvoiceItem"]] = relationship(back_populates="invoice")


class Customer(Base):
    __tablename__ = 'customers'

    CustomerId: Mapped[int] = mapped_column(primary_key=True)
    FirstName: Mapped[str]
    LastName: Mapped[str]
    Email: Mapped[str]

    invoices: Mapped[List["Invoice"]] = relationship(back_populates="customer")


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    InvoiceItemId: Mapped[int] = mapped_column(primary_key=True)
    InvoiceId: Mapped[int] = mapped_column(ForeignKey("invoices.InvoiceId"))
    TrackId: Mapped[int] = mapped_column(ForeignKey("tracks.TrackId"))

    invoice: Mapped["Invoice"] = relationship(back_populates="items")
    track: Mapped["Track"] = relationship(back_populates="invoices")
