from flask import Flask, render_template, request, make_response
import db

app = Flask(__name__)
if __name__ == '__main__':
    app.run()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello/')
def hello_world2():
    return render_template('hello.html')


@app.route('/hello_not_found/')
def hello_not_found():
    return render_template('hello.html'), 404


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/addNumbers/<int:first>/<int:second>')
def add_numbers(first, second):
    return str(first + second)


@app.route('/hello/<name>')
def hello_extended(name):
    return render_template('hello.html', name=name)


@app.route('/helloPost/', methods=['POST'])
def hello_post():
    return render_template('hello.html', name=request.form['name'])


@app.route('/helloJson/', methods=['POST'])
def hello_json():
    return render_template('hello.html', name=request.json['name'])


@app.route('/set_cookie/<string:cookie>')
def set_cookie(cookie):
    resp = make_response('You set cookie value as: ' + cookie)
    resp.set_cookie('my_cookie', cookie)
    return resp


@app.route('/get_cookie')
def get_cookie():
    return request.cookies.get('my_cookie')


app.config['DATABASE'] = 'flask.sqlite'
db.init_app(app)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        db.get_db().execute("Insert INTO post VALUES(NULL,?,?,?)",
                            (request.json['author'], request.json['title'], request.json['body']))
        db.get_db().commit()
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()
    return render_template('blog.html', posts=data)


@app.route('/blog_extends')
def blog_extends():
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()
    return render_template('blogExtends.html', posts=data)


@app.route('/blog_pretty', methods=['GET', 'POST'])
def blog_pretty():
    if request.method == 'POST':
        db.get_db().execute("Insert INTO post VALUES(NULL,?,?,?)",
                            (request.json['author'], request.json['title'], request.json['body']))
        db.get_db().commit()
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()
    return render_template('blogPretty.html', posts=data)
