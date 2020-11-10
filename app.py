from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# from the security.py import the two functions
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ringler'
api = Api(app)


# pass app, and two functions to the JWT Object 
# using these three together will allow for authentication of users
jwt = JWT(app, authenticate, identity) # jwt creates a NEW ENDPOINT /auth

# add_resource...this is similar to @app.route('/student/<string:name>')
# http://127.0.0.1:5000/item/name-of-item
# name below is a variable add comes from the get function get(self, name)
api.add_resource(Item, '/item/<string:name>')         
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)