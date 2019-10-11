from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

from models.students_models import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()

    # parser.add_argument('name', type=str, required=True,
    #                     help='This field cannot be left blank.')

    parser.add_argument('major', type=str, required=True,
                        help='This field cannot be left blank.')

    parser.add_argument('classroom_id', type=str, required=True,
                        help='Every student needs a classroom id.')

    @jwt_required()
    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return student.json()
        return {'message': 'Student record not found'}, 404

    def post(self, name):
        if StudentModel.find_by_name(name):
            return {'message': "The student with name '{}' already exists.".format(name)}, 400

        data = Student.parser.parse_args()
        print(data)

        student = StudentModel(name, **data)
        # student = StudentModel(name, data['major'], data['classroom_id'])

        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred during an attempt to insert data into the database."}, 500

        return student.json(), 201

    def delete(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()
            return {'message': 'The student record has been deleted'}

        return {'message': 'The student record not found.'}, 404

    def put(self, name):
        data = Student.parser.parse_args()

        student = StudentModel.find_by_name(name)

        if student:
            student.major = data["major"]
        else:
            student = StudentModel(name, **data)
            # student = StudentModel(name, data['major'], data['classroom_id'])

        student.save_to_db()

        return student.json()


class StudentList(Resource):
    def get(self):
        # return {'student': [student.json() for student in StudentModel.query.all()]}
        return {'student': list(map(lambda x: x.json(), StudentModel.query.all()))}
