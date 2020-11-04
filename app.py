from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
# from the security.py import the two functions
from security import authenticate, identity
from user import UserRegister

# jwt = JSON web token

app = Flask(__name__)
app.secret_key = 'ringler'
api = Api(app)
# pass app, and two functions to the JWT Object 
# using these three together will allow for authentication of users
jwt = JWT(app, authenticate, identity) # jwt creates a NEW ENDPOINT /auth

items = []

#=====Using filter function in-place of for loop
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
                type=float, 
                required=True, 
                help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        # in the items list search the key 'name' for matching value
        # next takes the first returned match
        # if nothing matches then None is returned 
        item = next(filter(lambda x: x['name'] == name, items), None)
        # item will be the matching furniture item or None
        return {'item': item}, 200 if item else 404


    def post(self, name):
        # Added Error control
        # Using the filter function we are checking if not None then item exists
        # The client creating item that already exists. Return 400 error bad request
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f"An item with name {name} already exists".format(name)}, 400 
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']} # Access the price key of dictionary
        # add item to the items list
        items.append(item)
    
        # 201 indicates created 202 indicates excepted 
        return item, 201

    def delete(self, name):
        global items # Need to declare global b/c out list is items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self,name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(Item)
        else:
            item.update(data)
        return item

# Will return all the items
class ItemList(Resource):
    def get(self):
        return {'items': items}

# add_resource...this is similar to @app.route('/student/<string:name>')
# http://127.0.0.1:5000/item/name-of-item
# name below is a variable add comes from the get function get(self, name)
api.add_resource(Item, '/item/<string:name>')         
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)