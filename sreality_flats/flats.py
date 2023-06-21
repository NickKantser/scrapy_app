from flask import Flask, render_template
import psycopg2
app = Flask(__name__)

connection = psycopg2.connect('postgres://elsjbyqx:thpxz1QRoIbx34LqqsgLsAG3kdxCcfGg@lallah.db.elephantsql.com/elsjbyqx')
#
#
#
# # flats = [
# # {}
# # ]
#
@app.route('/')
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM flats""")
            flats = cursor.fetchmany(100)
            # print(title)

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
