from sqlite3 import Cursor
from flask import Flask, jsonify, request
from app_config import settings
from flask_mysqldb import MySQL

app = Flask(__name__)
conn = MySQL(app)

@app.route('/courses')
def get_courses():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT * FROM api_flask.course;"
        cursor.execute(sql)
        data = cursor.fetchall()
        courses = []
        for row in data:#Accedemos a los datos por medio de su posicion 
            course = {"id": row[0], "name": row[1], "credits": row[2]}        
            courses.append(course)
        print(courses)
        return jsonify({"message": "Courses listed", "courses": courses})
    except Exception as ex:
        return f'ERROR: {ex}'

@app.route('/courses/<course_code>')
def get_course(course_code):
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT id, name, credits FROM api_flask.course WHERE id = '{0}'".format(course_code)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            course = {"id": data[0], "name": data[1], "credits": data[2]}
            return jsonify({"message": "Course found", "course": course})
        else:
            return jsonify({"message": "Course not found"})
    except Exception as ex:
        return f"Error: {ex}"
   
@app.route('/courses', methods=['POST'])
def add_course():
    try:
        id = request.json['id']
        name = request.json['name']
        credits = request.json['credits']
        cursor = conn.connection.cursor()
        sql = "INSERT INTO api_flask.course(id, name, credits) VALUES ('{0}', '{1}', '{2}')".format(id, name, credits)
        cursor.execute(sql)
        conn.connection.commit()
        return jsonify({"message": "Added course"})
    except Exception as ex:
        return f"Error: {ex}"

@app.route('/courses/<course_code>', methods=['DELETE'])
def delete_course(course_code):
    try:
        cursor = conn.connection.cursor()
        sql = "DELETE FROM api_flask.course WHERE id = {0}".format(course_code)
        cursor.execute(sql)
        conn.connection.commit()
        return jsonify({"message": "Deleted course"})
    except Exception as ex:
        return f"Error: {ex}"

@app.route('/courses/<course_code>', methods=['PUT'])
def update_course(course_code):
    try:
        name = request.json['name']
        credits = request.json['credits']

        cursor = conn.connection.cursor()
        sql = "UPDATE api_flask.course SET name = '{0}', credits = '{1}' WHERE id = '{2}'".format(name, credits, course_code)
        cursor.execute(sql)
        conn.connection.commit()
        return jsonify({"message": "Update course"})
    except Exception as ex:
        return f"Error: {ex}"

@app.errorhandler(404)
def page_not_found(error):
    return f"<h1>Page not found</h1> {error}", 404

# def validate_id(new_id):
#     try:
#         cursor = conn.connection.cursor()
#         sql = "SELECT id FROM api_flask.course"
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         course_id = []
#         for id in data:
#             course_id.append(id)
#         print(course_id)
#         if new_id in course_id:
#             return jsonify({"message": "Existing id"})
#         else:
#             return new_id
#     except Exception as ex:
#         return jsonify({"message": "Duplicate entry"})

if __name__ == "__main__":
    app.config.from_object(settings['development'])
    app.run()