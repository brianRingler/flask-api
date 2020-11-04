from user import User

users = [
    User(1, 'bob', 'asdf')
]

# Using set comprehension similar to list comprehension 
# The order will not be the same each time....like dictionary 
# for each user in users return the username 
username_mapping = {u.username: u for u in users}
# for each user in users return the users id
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    # validate that username matches the password in mapping dictionary 
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)