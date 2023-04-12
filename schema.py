from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)
    password = fields.Str(required=True)
    country = fields.Str(required=True)


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    flavour = fields.Str(required=True, enum= ['Pepperoni', 'Margherita', 'Hawaiian', 'Meatlovers'
                                               'Veggie', 'BBQchicken', 'Fourcheese', 'Buffalochicken',
                                              'Whitepizza', 'Supreme'])
    quantity = fields.Int(required=True)
    size = fields.Str(required=True, enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class OrdersSchema(Schema):
    id = fields.Int(dump_only=True)
    flavour = fields.Str(required=True, enum= ['Pepperoni', 'Margherita', 'Hawaiian', 'Meatlovers'
                                               'Veggie', 'BBQchicken', 'Fourcheese', 'Buffalochicken',
                                              'Whitepizza', 'Supreme'])
    quantity = fields.Int(required=True)
    size = fields.Str(required=True, enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])
    order_id = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    

class OrdeSchema(Schema):
    id = fields.Int(dump_only=True)
    flavour = fields.Str(required=True, enum= ['Pepperoni', 'Margherita', 'Hawaiian', 'Meatlovers'
                                               'Veggie', 'BBQchicken', 'Fourcheese', 'Buffalochicken',
                                              'Whitepizza', 'Supreme'])
    quantity = fields.Int(required=True)
    size = fields.Str(required=True, enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])
    order_status = fields.Str(required=True, enum = ['PENDING', 'IN_TRANSIT', 'DELIVERED'])


class OrdSchema(Schema):
    id = fields.Int(dump_only=True)
    flavour = fields.Str(required=True, enum= ['Pepperoni', 'Margherita', 'Hawaiian', 'Meatlovers'
                                               'Veggie', 'BBQchicken', 'Fourcheese', 'Buffalochicken',
                                              'Whitepizza', 'Supreme'])
    quantity = fields.Int(required=True)
    size = fields.Str(required=True, enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])
    order_status = fields.Str(required=True, enum = ['PENDING', 'IN_TRANSIT', 'DELIVERED'])


    