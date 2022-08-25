from flask import Flask
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
        print(data)
        return 'okS'
    except Exception as ex:
        return f'ERROR: {ex}'

@app.errorhandler(404)
def page_not_found(error):
    return f"Page not found: {error}"


if __name__ == "__main__":
    app.config.from_object(settings['development'])
    app.run()