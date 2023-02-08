from ..utils import db
from enum import Enum
from datetime import datetime

# Enum class for order sizes
"""
This is an Enum class for sizes with four different size options: small, medium, large, and extra large.
"""
class Sizes(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

# Enum class for order status
# This is an Enum class for order status with three different status options: pending, in-transit, and delivered.
class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'

# Order model
# This is the Order model class that defines the order table in the database.
# The order table has the following fields: id, size, order_status, flavour, quantity, date_created, and customer.
# The id field is the primary key and is auto-incremented.
# The size field is an Enum field that has four different size options: small, medium, large, and extra large.
# The order_status field is an Enum field that has three different status options: pending, in-transit, and delivered.
# The flavour field is a String field that is required.
# The quantity field is an Integer field that has a default value of 1.
# The date_created field is a DateTime field that has a default value of the current date and time.
# The customer field is an Integer field that is a foreign key to the id field in the users table.
# The __repr__ method returns a string representation of the Order object.
# The save method adds the Order object to the database session and commits the changes.
# The get_by_id method returns an Order object with the specified id.
# If the Order object with the specified id does not exist, a 404 error is returned.
# The __tablename__ variable is used to specify the name of the table in the database.
class Order(db.Model):
    # Table name
    __tablename__ = 'orders'
    # Fields
    # id field
    # This is the id field that is the primary key and is auto-incremented.
    id = db.Column(db.Integer(), primary_key=True)
    # size field
    # This is the size field that is an Enum field that has four different size options: small, medium, large, and extra large.
    size = db.Column(db.Enum(Sizes), default=Sizes.MEDIUM)
    # order_status field
    # This is the order_status field that is an Enum field that has three different status options: pending, in-transit, and delivered.
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    # flavour field
    # This is the flavour field that is a String field that is required.
    flavour = db.Column(db.String(), nullable=False)
    # quantity field
    # This is the quantity field that is an Integer field that has a default value of 1.
    quantity = db.Column(db.Integer(), default=1)
    # date_created field
    # This is the date_created field that is a DateTime field that has a default value of the current date and time.
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    # customer field
    # This is the customer field that is an Integer field that is a foreign key to the id field in the users table.
    customer = db.Column(db.Integer(), db.ForeignKey('users.id'))

    # Class methods
    # __repr__ method
    # This is the __repr__ method that returns a string representation of the Order object.
    def __repr__(self):
        return f"<Order {self.id}>"

    # save method
    # This is the save method that adds the Order object to the database session and commits the changes.
    # The save method is used to add a new Order object to the database.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # get_by_id method
    # This is the get_by_id method that returns an Order object with the specified id.
    # If the Order object with the specified id does not exist, a 404 error is returned.
    # The get_by_id method is used to get an Order object with the specified id.
    # The get_by_id method is used in the OrderResource class in the orders.py file in the resources folder.
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
