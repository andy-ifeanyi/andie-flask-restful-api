from flask_restful import Resource
from models.classroom_model import ClassRoomModel


class ClassRoom(Resource):
    def get(self, name):
        classroom = ClassRoomModel.find_by_name(name)
        if classroom:
            return classroom.json()
        return {'message': 'Classroom not found'}, 404

    def post(self, name):
        if ClassRoomModel.find_by_name(name):
            return {'message': 'A classromm with name "{}" already exists'.format(name)}, 400

        classroom = ClassRoomModel(name)

        try:
            classroom.save_to_db()
        except:
            return {'message': 'An error occurred while creating the classroom.'}, 500
        return classroom.json(), 201

    def delete(self, name):
        classroom = ClassRoomModel.find_by_name(name)
        if classroom:
            classroom.delete_from_db()
        return {'message': 'Classroom deleted.'}


class ClassRoomList(Resource):
    def get(self):
        return {'classrooms': [classroom.json() for classroom in ClassRoomModel.query.all()]}
