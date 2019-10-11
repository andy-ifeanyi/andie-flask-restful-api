from db import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    major = db.Column(db.String(80))

    classroom_id = db.Column(
        db.Integer, db.ForeignKey('classrooms.classroomid'))
    classroom = db.relationship('ClassRoomModel')

    def __init__(self, name, major, classroom_id):
        self.name = name
        self.major = major
        self.classroom_id = classroom_id

    def json(self):
        return {'name': self.name, 'major': self.major}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
