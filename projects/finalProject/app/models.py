from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple
import pymongo
import json

client = pymongo.MongoClient(
    'mongodb+srv://betote:6hBzndMr3RLsBDFx@cluster0-3vp2d.mongodb.net/test?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE')
db = client.test

class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False, objectID=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

        # Para guardar el objeto durante la sesión
        self.objectID = objectID

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_object(self, user):

        userToJSON = json.dumps(user.__dict__)

        filter = {'user_id': self.id}

        newvalues = {'$set': {'objectID': userToJSON} }

        db.userBlockChain.update_one(filter, newvalues, upsert=False)

    def register(self, user):
        userToJSON = json.dumps(user.__dict__)
        db.userBlockChain.insert_one({'user_id': self.id, 'name':self.name, 'email': self.email, 'password': self.password, 'is_admin':self.is_admin, 'objectID': userToJSON})

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @staticmethod
    def get_by_id(id):

        if id is not None:
            userInfo = db.userBlockChain.find_one({'user_id': int(id)})

            if userInfo is not None:
                objectID = userInfo.get('objectID')

                if objectID is not None:
                    return User(**json.loads(objectID))

        return None

    @staticmethod
    def get_by_email(email, passwd):
        userInfo = db.userBlockChain.find_one({'email': email})

        if userInfo is not None:
            password = check_password_hash(userInfo.get('password'), passwd)

            if password:
                return userInfo

        return None

    @staticmethod
    def getUsers():
        users = db.userBlockChain.find({"$or": [{"is_admin": 0}, {"is_admin": False}]}, {"email":1, "name":1})
        accounts = []
        for user in users:
            del user["_id"]
            accounts.append(user)
        return accounts

    @staticmethod
    def deleteUser(email):
        user = db.userBlockChain.find({"email":email})
        if user.count() == 0:
            return False
        db.userBlockChain.delete_one({"email":email})
        return True
