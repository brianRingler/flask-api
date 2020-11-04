from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
# from the security.py import the two functions
from security import authenticate, identity

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
    @jwt_required()
    def get(self, name):
        # in the items list search the key 'name' for matching value
        # next takes the first returned match
        # if nothing matches then None is returned 
        item = next(filter(lambda x: x['name'] == name, items), None)
        # item will be the matching furniture item or None
        return {'item': item}, 200 if item is not None else 404


# Every Resource works with an Api and every Resource must be a class
# The class 'Item' inherits from the Resource class
#=====USING a for loop====
# class Item(Resource):
#     def get(self, name): # define a get Method that this resource will use
#         for item in items:
#             # jsonify not required b/c flask_restful manages this for us
#             if item['name'] == name:
#                 # returning a dictionary 
#                 return item  
#         # if item is not in list return a dictionary indicating None.
#         # When run in postman this will be Null
#         # adding 404 will force the status 404 instead of status code 200...which is not correct
#         return {'item':None}, 404


    def post(self, name):
        # Added Error control
        # Using the filter function we are checking if not None then item exists
        # The client creating item that already exists. Return 400 error bad request
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f"An item with name {name} already exists"}, 400 

        data = request.get_json()
        item = {'name': name, 'price': data['price']} # Access the price key of dictionary
        # add item to the items list
        items.append(item)
        # 202 indicates excepted. Use when delaying the creation of the object. This lets the client know you have excepted without having to wait. 
        # 201 indicates created 
        return item, 201

# add_resource...this is similar to @app.route('/student/<string:name>')
# http://127.0.0.1:5000/item/name-of-item
# name below is a variable add comes from the get function get(self, name)
api.add_resource(Item, '/item/<string:name>') 

# Will return all the items
class ItemList(Resource):
    def get(self):
        return {'items': items}
        
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)