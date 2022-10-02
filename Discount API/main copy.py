from curses import flash
from typing import Final
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'allanchuang1.mysql.pythonanywhere-services.com'
app.config['MYSQL_DATABASE_USER'] = 'allanchuang1'
app.config['MYSQL_DATABASE_PASSWORD'] = '#A123b456'
app.config['MYSQL_DATABASE_DB'] = 'allanchuang1$default'






api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class courseModel(db.Model):
    course_id = db.Column(db.String(8), primary_key=True)
    course_name = db.Column(db.String(500), nullable = True)
    description = db.Column(db.String(500), nullable = True)
    GPA = db.Column(db.Integer, nullable = True)
    ASS1 = db.Column(db.Float, nullable = True)
    ASS2 = db.Column(db.Float, nullable = True)
    ASS3 = db.Column(db.Float, nullable = True)
    Exam = db.Column(db.Float, nullable = True)

    def __repr__(self):
        return f"Course(course_id={course_id}, course_name={course_name}, course_rating={rating}, course_GPA={GPA})"

course_put_args = reqparse.RequestParser()
course_put_args.add_argument("course_name", type=str, help="Name of the course", required = False)
course_put_args.add_argument("description", type=str, help="Course description", required = False)
course_put_args.add_argument("GPA", type=int, help="My GPA for this course", required = False)
course_put_args.add_argument("ASS1", type=float, help="First Assessment result", required = False)
course_put_args.add_argument("ASS2", type=float, help="Second Assessment result", required = False)
course_put_args.add_argument("ASS3", type=float, help="Third Assessment result", required = False)
course_put_args.add_argument("Exam", type=float, help="Final Exam result", required = False)

course_update_args = reqparse.RequestParser()
course_update_args.add_argument("name", type=str, help="Name of the course")
course_update_args.add_argument("views", type=int, help="View of the course")
course_update_args.add_argument("likes", type=int, help="Likes on the course")

resource_fields = {
    'course_id': fields.String,
    'course_name': fields.String,
    'rating': fields.Integer,
    'GPA': fields.Integer
    }




class course(Resource):
    @marshal_with(resource_fields)
    def get(self, course_id):
        result = courseModel.query.filter_by(course_id = course_id).first()
        if not result:
            abort(404, message = "Could not find course with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, course_id):
        args = course_put_args.parse_args()
        print(args['course_name'])
        result = courseModel.query.filter_by(course_id = course_id).first()
        if result:
            abort(409, message = "course id taken...")

        course = courseModel(course_id = course_id, course_name = args['course_name'], description = args['description'], GPA = args['GPA'],
                            ASS1 = args['ASS1'], ASS2 = args['ASS2'], ASS3 = args['ASS3'], Exam = args['Exam'])
         
        db.session.add(course)
        db.session.commit()
        #return course, 201

    @marshal_with(resource_fields)
    def patch(self, course_id):
        args = course_update_args.parse_args()
        result = courseModel.query.filter_by(id = course_id).first()
        if not result:
            abort(404, message = "course doesn't exist, canno update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.name = args['views']
        if args['likes']:
            result.name = args['likes']

        db.session.commit()

        return result

    def delete(self, course_id):
        abort_if_course_id_doesnt_exist(course_id)
        del courses[course_id]
        return '', 204
        
    
api.add_resource(course, "/course/<string:course_id>")

if __name__ == "__main__":
    app.run(debug=True)
