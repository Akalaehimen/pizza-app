from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the Namespace
# This is the name that will be used in the URL
# For example: http://localhost:5000/api/v1/orders
# The name of the namespace is orders
order_namespace = Namespace('orders', description='Namespace for Orders')

# Define the Model
# This is the structure of the data that will be returned
# The model is called Order
# The fields are id, flavour, quantity, size, and order_status
# The fields are required, and have a description
# The size field has an enum, which means that the value must be one of the values in the list
# The order_status field has an enum, which means that the value must be one of the values in the list
# The model is then added to the namespace
# The model is then used in the Resource classes
# The marshal_with decorator is used to return the model
# The expect decorator is used to expect the model
order_model = order_namespace.model(
    'Order', {
        # The id field is not required, because it is auto-generated
        'id': fields.Integer(description='Order ID'),
        'flavour': fields.String(description='Pizza Flavour', required=True),
        'quantity': fields.Integer(description='Number of Pizzas'),
        'size': fields.String(description='Pizza Size', required=True,
            enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']
        ),
        'order_status': fields.String(description='Current Order Status', required=True,
            enum = ['PENDING', 'IN_TRANSIT', 'DELIVERED']
        )
    }
)

# Define the Resource Classes
# The Resource classes are used to define the endpoints
# The Resource classes are decorated with the namespace
# The Resource classes are decorated with the route
# The Resource classes are decorated with the marshal_with decorator
# The Resource classes are decorated with the expect decorator
# The Resource classes are decorated with the jwt_required decorator
@order_namespace.route('/orders')
class OrderGetCreate(Resource):

    # The marshal_with decorator is used to return the model
    # The jwt_required decorator is used to require a JWT
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    # The get method is used to retrieve all orders
    def get(self):
        """
            Get All Orders
        """
        # Get all orders
        orders = Order.query.all()

        # Return the orders with a status of 200
        return orders, HTTPStatus.OK

    # The expect decorator is used to expect the model
    # The marshal_with decorator is used to return the model
    # The jwt_required decorator is used to require a JWT
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    # The post method is used to create an order
    def post(self):
        """
            Place an Order
        """
        # Get the current user
        # you remember we set the identity to be the user's username in the login route
        # The current user is retrieved from the JWT
        username = get_jwt_identity()

        # get the current user from the database by filtering the database by the username
        current_user = User.query.filter_by(username=username).first()

        # This code assigns the payload property of the order_namespace object to the variable 'data'.
        # The payload property is the data that was sent in the request
        # The data is then assigned to the variables in the Order model
        data = order_namespace.payload

        # Create a new order
        new_order = Order(
            size = data['size'],
            quantity = data['quantity'],
            flavour = data['flavour']
        )

        # Set the user of the order to the current user
        new_order.user = current_user

        # Save the order to the database
        # This will also save the user to the database
        # This is because the user is a relationship of the order
        # The user is saved to the database because the user is a relationship of the order
        new_order.save()

        # Return the new order with a status of 201
        return new_order, HTTPStatus.CREATED


# The Resource classes are decorated with the namespace
# The Resource classes are decorated with the route
@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

    # The marshal_with decorator is used to return the model
    # The jwt_required decorator is used to require a JWT
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    # The get method is used to retrieve an order by id
    def get(self, order_id):
        """
            Retrieve an Order by ID
        """
        # Get the order by id
        # the get_by_id method is defined in the Order model
        # The id is passed in as a parameter
        order = Order.get_by_id(order_id)

        # Return the order with a status of 200
        return order, HTTPStatus.OK

    # the put method is used to update an order by id
    def put(self, order_id):
        """
            Update an Order by ID
        """
        pass

    # the delete method is used to delete an order by id
    def delete(self, order_id):
        """
            Delete an Order by ID
        """
        pass

# The Resource classes are decorated with the namespace
# this route is used to a specific order by a specific user
@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):

    @order_namespace.marshal_with(order_model)
    @jwt_required()
    # the get method is used to retrieve a specific order by a specific user
    def get(self, user_id, order_id):
        """
            Get a User's Specific Order
        """
        # Get the user by id
        user = User.get_by_id(user_id)

        # filter the orders by the order id and the user
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()

        # Return the order with a status of 200
        return order, HTTPStatus.OK

# this route is used to retrieve all orders by a specific user
@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):

    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    # the get method is used to retrieve all orders by a specific user
    #  it takes in a user id as a parameter
    def get(self, user_id):
        """
            Get All Orders by a User
        """
        # Get the user by id
        user = User.get_by_id(user_id)

        # Get the user's orders
        orders = user.orders

        # Return the orders with a status of 200
        return orders, HTTPStatus.OK

# this route is used to update an order's status
@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    # the patch method is used to update an order's status
    # it takes in an order id as a parameter
    # the order id is used to retrieve the order
    def patch(self, order_id):
        """
            Update an Order's Status
        """
        pass