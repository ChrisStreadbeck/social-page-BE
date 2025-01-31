from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://eapvloonqchbui:b68a1562f7564eb2df52510787b45284c6be9793d71f2547737948316c59e624@ec2-107-20-251-130.compute-1.amazonaws.com:5432/detee95h0trtt8"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Social(db.Model):
    __tablename__ = "socials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(500))
    shortdescription = db.Column(db.String(100))
    longdescription = db.Column(db.String(2000))
    
    def __init__(self, name, image, shortdescription, longdescription):
        self.name = name
        self.image = image
        self.shortdescription = shortdescription
        self.longdescription = longdescription

class SocialSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "image", "shortdescription", "longdescription")

social_schema = SocialSchema()
socials_schema = SocialSchema(many=True)

@app.route("/")
def greeting():
    return "<h1>Social Cards API</h1>"

@app.route("/socials", methods=["GET"])
def get_socials():
    all_socials = Social.query.all()
    result = socials_schema.dump(all_socials)
    return jsonify(result.data)

@app.route("/social/<id>", methods=["GET"])
def get_social(id):
    social = Social.query.get(id)
    return social_schema.jsonify(social)

@app.route("/add-social", methods=["POST"])
def add_social():
    name = request.json["name"]
    image = request.json["image"]
    shortdescription = request.json["shortdescription"]
    longdescription = request.json["longdescription"]

    new_social = Social(name, image, shortdescription, longdescription)

    db.session.add(new_social)
    db.session.commit()

    return jsonify("Social POSTED!")

@app.route("/social/<id>", methods=["PUT"])
def update_social(id):
    social = Social.query.get(id)

    name = request.json["name"]
    image = request.json["image"]
    shortdescription = request.json["shortdescription"]
    longdescription = request.json["longdescription"]


    social.name = name
    social.shortdescription = shortdescription 
    social.longdescription = longdescription
    
    db.session.commit()
    return social_schema.jsonify(social)


@app.route("/social/<id>", methods=["DELETE"])
def delete_social(id):
    record = Social.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Record DELETED!!")  

if __name__ == "__main__":
    app.debug = True
    app.run()