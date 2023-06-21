from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

DB_URL = os.getenv('DB_URL')
connection = psycopg2.connect(DB_URL)

@app.route('/')
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM flats""")
            flats = cursor.fetchmany(100)

    posts = []
    for flat in flats:
        posts.append({
            'title': flat[1],
            'image_url': flat[2],
        })

    print('check')
    return render_template('home.html', posts=posts)

@app.route('/hello')
def hello():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
