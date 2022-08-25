from flask import Flask, jsonify
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
    

@app.errorhandler(404)
def page_not_found(error):
    return f"<h1>Page not found</h1> {error}", 404


if __name__ == "__main__":
    app.config.from_object(settings['development'])
    app.run()