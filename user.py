import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/
    @classmethod # 81 min 8:52
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,)) # most have the comma after username
        
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod # 81 min 8:52
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,)) # most have the comma after username
        
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    
    parser.add_argument('username', 
        type=float, 
        required=True, 
        help='This field cannot be left blank!')

    parser.add_argument('password', 
        type=float, 
        required=True, 
        help='This field cannot be left blank!')

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cusrsor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
        


       