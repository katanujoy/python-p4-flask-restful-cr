#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Home Route
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(response_dict, 200)
        return response

# All Newsletters Route (GET and POST)
class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()
        response = make_response(response_dict, 201)
        return response

# Single Newsletter by ID Route
class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if record:
            response = make_response(record.to_dict(), 200)
        else:
            response = make_response({"error": "Newsletter not found"}, 404)
        return response

# Register Resources
api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
