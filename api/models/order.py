from utils import db
from enum import Enum
from datetime import datetime


class Sizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'

class Flavour(Enum):
    Pepperoni = 'Pepperoni'
    Margherita = 'Margherita'
    Hawaiian = 'Hawaiian'
    Meatlovers = 'Meat lovers'
    Veggie = 'Veggie'
    BBQchicken = 'BBQ chicken'
    Fourcheese = 'Four cheese'
    Buffalochicken = 'Buffalo chicken'
    Whitepizza = 'White pizza'
    Supreme = 'Supreme'


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(Sizes), default=Sizes.SMALL)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.Enum(Flavour))                                                   
    quantity = db.Column(db.Integer(), default=1)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    order_id = db.Column(db.String(10), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    
    

    def __repr__(self):
        return f"<Order {self.id}>"
    

