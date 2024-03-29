import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth_file import authenticate, identity
from resources.user import UserRegister
from resources.students import Student, StudentList
from resources.classroom import ClassRoom, ClassRoomList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'denzy'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(ClassRoom, '/classroom/<string:name>')
api.add_resource(ClassRoomList, '/classrooms')
api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
