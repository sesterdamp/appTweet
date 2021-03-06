from flask import Flask, Blueprint, request, abort
from flask_restful import Api, Resource, reqparse

User = [
    {
        "username": "sam",
        "email": "sam@gmail.com",
        "password": "123",
        "fullname": "Samsam M.N.",
        "tweet":""
    },
    {
        "username": "jack",
        "email": "jack@gmail.com",
        "password": "123",
        "fullname": "Jack The Reaper",
        "tweet":""
    }
]

Tweets = {
    "jack@gmail.com":[],
    "sam@gmail.com":[]
}

def checkEmailExists(email,check):
    if check == True:
        for data in User:
            if data["email"] == email:
                abort(400, "Email sudah digunakan")

        return email
    elif check == False:
        for data in User:
            if data["email"] == email:
                return email

        abort(400, "Email tidak ditemukan")

def isRequired(field):
    parser = reqparse.RequestParser()
    for kolom in field:
        parser.add_argument(kolom,required = True, location = ["json"], help = "Kolom "+kolom+" tidak ditemukan")
    return parser.parse_args()

class signUp(Resource):
    def post(self):
        #validasi kolom dlu
        isRequired(["username","email","password","fullname"])

        #cek email dulu bro
        checkEmailExists(request.json["email"],True)

        req = request.json
        req.update({"tweet":""})

        User.append(req)
        Tweets[request.json["email"]] = []
        return "Daftar Berhasil!", 201    

class signIn(Resource):
    def post(self):
        isRequired(["email","password"])
        
        email = request.json["email"]
        password = request.json["password"]

        for login in User:
            if login["email"] == email and login["password"] == password:
                login["tweet"] = Tweets[login["email"]]

                return login

        return "Email atau Password salah!", 401

class Tweet(Resource):
    def post(self):
        #validasi kolom dulu
        isRequired(["email","tweet"])

        #check email dlu bro
        checkEmailExists(request.json["email"],False)
        Tweets[request.json["email"]].append(request.json["tweet"])

        return "Tweet Berhasil", 201

class delTweet(Resource):
    def post(self):
        email = request.json["email"]
        tweet = request.json["tweet"]

        checkEmailExists(request.json["email"],False)
        for keyEmail in Tweets:
            if keyEmail == email:
                for index,tw in enumerate(Tweets[keyEmail]):
                    if tw == tweet:
                        # print('a')
                        del Tweets[keyEmail][index]
                        return "Tweet berhasil dihapus!",200
                
                return "Tweet '"+tweet+"' tidak ditemukan!", 400

class allData(Resource):
    def post(self):
        for data in User:
            data["tweet"] = Tweets[data["email"]]
        
        return User, 200


user_api = Blueprint('users',__name__)
api = Api(user_api)

api.add_resource(signUp,'/signUp')
api.add_resource(signIn,'/signIn')
api.add_resource(Tweet,'/tweet')
api.add_resource(delTweet,'/deltweet')
api.add_resource(allData,'/allData')