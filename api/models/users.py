from ..utils import db


# User model
# This is the User model class that defines the user table in the database.
# The user table has the following fields: id, username, email, password_hash, is_staff, is_active, and orders.
# The id field is the primary key and is auto-incremented.
# The username field is a String field that is required and unique.
# The email field is a String field that is required and unique.
# The password_hash field is a Text field that is required.
# The is_staff field is a Boolean field that has a default value of False.
# The is_active field is a Boolean field that has a default value of False.
# The orders field is a relationship field that defines the relationship between the user and order tables.
# The __repr__ method returns a string representation of the User object.
# The save method adds the User object to the database session and commits the changes.
# The get_by_id method returns a User object with the specified id.
# If the User object with the specified id does not exist, a 404 error is returned.
# The __tablename__ variable is used to specify the name of the table in the database.
class User(db.Model):
    # Table name
    __tablename__ = 'users'
    # Fields
    # id field
    # This is the id field that is the primary key and is auto-incremented.
    id = db.Column(db.Integer(), primary_key=True)
    # username field
    # This is the username field that is a String field that is required and unique.
    username = db.Column(db.String(45), nullable=False, unique=True)
    # email field
    # This is the email field that is a String field that is required and unique.
    email = db.Column(db.String(50), nullable=False, unique=True)
    # password_hash field
    # This is the password_hash field that is a Text field that is required.
    password_hash = db.Column(db.Text(), nullable=False)
    # is_staff field
    # This is the is_staff field that is a Boolean field that has a default value of False.
    # this will determine if the user is a staff member or not.
    is_staff = db.Column(db.Boolean(), default=False)
    # is_active field
    # This is the is_active field that is a Boolean field that has a default value of False.
    # this will determine if the user is active or not.
    is_active = db.Column(db.Boolean(), default=False)
    # orders field
    # This is the orders field that is a relationship field that defines the relationship between the user and order tables.
    # The backref argument defines the name of the attribute that will be added to the Order model to get the user object.
    # The lazy argument defines how the data will be loaded from the database.
    # The lazy argument can be set to 'select' to load the data in one go.
    # The lazy argument can be set to 'dynamic' to load the data in a lazy manner.
    orders = db.relationship('Order', backref='user', lazy=True)

    # Methods
    # __repr__ method
    # This method returns a string representation of the User object.
    # The string representation is in the format <User username>.
    # The username is the username of the user.
    def __repr__(self):
        return f"<User {self.username}>"

    # save method
    # This method adds the User object to the database session and commits the changes.
    # The commit method is used to commit the changes to the database.
    # The commit method is called on the db.session object.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # get_by_id method
    # This method returns a User object with the specified id.
    # If the User object with the specified id does not exist, a 404 error is returned.
    # The get_or_404 method is used to get the User object with the specified id.
    # The get_or_404 method is called on the cls.query object.
    # The cls.query object is the query object for the User model.
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
