from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from utils import db
from flask import request, jsonify
from http import HTTPStatus
from api.models.user import UserModel
from api.models.order import OrderModel
from schema import OrderSchema
from schema import OrdSchema
from schema import OrdeSchema
from enum import Enum
import random
import string


blp = Blueprint("Orders", "orders", description="Operations on orders")


@blp.route('/orders')
class OrderGetCreate(MethodView):
    @blp.arguments(OrderSchema)
    @jwt_required()
    def post(self, place):
        """
            Place an Order
        """

        email = get_jwt_identity()

        current_user = UserModel.query.filter_by(email=email).first()

        data = request.json

        new_order = OrderModel(
            size=data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )

        new_order.user = current_user

        # generate a random order ID
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        new_order.order_id = order_id  # store the generated order ID in the database

        db.session.add(new_order)
        db.session.commit()

        return {"message": "Order placed successfully", "order_id": order_id},201



# retriev a user order by the order_id
@blp.route('/orders/<string:order_id>')
class OrderGetById(MethodView):
    @jwt_required()
    def get(self, order_id):
        order = OrderModel.query.filter_by(order_id=order_id).first()

        order_schema = OrdeSchema()
        order_json = order_schema.dump(order)

        if order:
            return jsonify(order_json)
        else:
            return jsonify({'message': 'No order found with ID "{}".'.format(order_id)})


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


# update an order by the ordder id 
@blp.route('/order/<string:order_id>', methods=['PUT'])
class OrderUpdateById(MethodView):
    @jwt_required()
    def put(self, order_id):
        order = OrderModel.query.filter_by(order_id=order_id).first()

        if not order:
            return jsonify({'message': 'No order found with ID "{}".'.format(order_id)}), 404

        # Parse the JSON payload from the request body
        data = request.get_json()

        # Check that the updated order status is in the list of available orders
        if 'status' in data and data['status'] not in [status.value for status in Flavour]:
            return jsonify({'message': 'Order status "{}" is not available.'.format(data['status'])}), 400

        # Update the order with the new data
        for key, value in data.items():
            setattr(order, key, value)

        # Save the updated order to the database
        db.session.commit()

        # Serialize the updated order and return it in the response
        order_schema = OrdeSchema()
        result = order_schema.dump(order)
        return jsonify({'message': 'Order updated successfully.', 'order': result}), 200

# cancel an order by a user
@blp.route('/orde/<string:order_id>', methods=['DELETE'])
class OrderDeleteById(MethodView):
    @jwt_required()
    def delete(self, order_id):
        order = OrderModel.query.filter_by(order_id=order_id).first()
        
        # check if the id exist
        if not order:
            return jsonify({'message': 'No order found with ID "{}".'.format(order_id)}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully.'}), 200                 


# getting all order
@blp.route('/ordersim')
class OrdersGetById(MethodView):
    @jwt_required()
    def get(self):

        orders = OrderModel.query.all()
        if not orders:
            return jsonify({"message": "No orders found"}), 404

        order_schema = OrderSchema()
        results = order_schema.dump(orders)

        return jsonify(results), 200
    
# delete a user by is user id 
@blp.route('/users/<string:user_id>')
class UserDeleteById(MethodView):
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "User not founds"}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message": "User deleted successfully"}), 200


class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in-transit'
    DELIVERED = 'delivered'
   
# update the status of an order   
@blp.route('/orders/<string:order_id>')
class OrderUpdateStatus(MethodView):
    @jwt_required()
    def post(self, order_id):
        order = OrderModel.query.filter_by(order_id=order_id).first()
        
        if not order:
            return jsonify({'message': 'No order found with ID "{}".'.format(order_id)}), 404

        # Parse the JSON payload from the request body
        data = request.get_json()

        # Check that the updated order status is in the list of available orders
        if 'status' in data and data['status'] not in [status.value for status in OrderStatus]:
            return jsonify({'message': 'Order status "{}" is not available.'.format(data['status'])}), 400

        # Update the order with the new data
        for key, value in data.items():
            setattr(order, key, value)

        # Save the updated order to the database
        db.session.commit()
        
        # Serialize the updated order and return it in the response
        order_schema = OrdSchema()
        result = order_schema.dump(order)

        return jsonify({"message": "Order status updated successfully", 'order': result}), 200