
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Flatmate(Base):
    """"""
    __tablename__ = 'flatmate'

    id   = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)

    def __repr__(self):
        return 'Flatmate #{} called {}'.format(self.id, self.name)


class Delivery(Base):
    """"""
    __tablename__ = 'delivery'

    id    = Column(Integer, primary_key=True)
    date  = Column(Date, unique=True, nullable=False)
    total = Column(Float)

    def format_date(self):
        return self.date.strftime('%A %-d %b')

    def __repr__(self):
        return 'Delivery #{} delivered on {}'.format(self.id, str(self.date))


class Purchase(Base):
    """"""
    __tablename__ = 'purchase'

    id          = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    quantity    = Column(Integer)
    price       = Column(Float)
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    
    def __repr__(self):
        return 'Purchase #{}: {} {} bought for {} on delivery #{}'.format(self.id, self.quantity, self.description, self.price, self.delivery_id)


class Assignment(Base):
    """"""
    __tablename__ = 'assignment'

    id          = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    flatmate_id = Column(Integer, ForeignKey('flatmate.id'))

    def __repr__(self):
        return 'Assignment #{}: Flatmate {} bought a share of purchase {}'.format(self.id, self.flatmate_id, self.purchase_id)