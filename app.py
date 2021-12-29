from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)


class Keyboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    img = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)
    info = db.Column(db.String(), nullable=False)
    origin = db.Column(db.String(), nullable=False)

    def __init__(self, uuid, name, img, date, price, info, origin):
        self.uuid = uuid
        self.name = name
        self.img = img
        self.date = date
        self.price = price
        self.info = info
        self.origin = origin

    
    def serialize(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "img": self.img,
            "date": self.date,
            "price": self.price,
            "info": self.info,
            "origin": self.origin
        }


@app.route("/api/keyboards", methods=["GET"])
def get_keyboards():
    keyboards = Keyboard.query.all()
    res = [keyboard.serialize() for keyboard in keyboards]
    return jsonify(res)
    

@app.route("/api/keyboards/<id>", methods=["GET"])
def get_keyboard(id):
    keyboard = Keyboard.query.filter_by(uuid=id).first()
    return jsonify(keyboard.serialize())


if __name__ == "__main__":
    app.run(debug=False)
