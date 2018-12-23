from flask import Flask, render_template, request, make_response
import db

app = Flask(__name__)
if __name__ == '__main__':
    app.run()


# Gdy odwiedzimy localhost:5000/ naszym oczom ukaże się Hello World!
@app.route('/')
def hello_world():
    return 'Hello World!'


# Możemy też wygenerować naszą stronę z szablonu z folderu templates
@app.route('/hello/')
def hello_world2():
    return render_template('hello.html')


# Możemy modyfikować status zwracany przez naszą stronę (domyślnie jest 200, co oznacza "wszystko ok")
@app.route('/hello_not_found/')
def hello_not_found():
    return render_template('hello.html'), 404


# Poniższy dekorator pozwala nam zastąpić domyślną stronę błedu innym komunikatem
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# Przez url możemy przekazywać parametry. Poniżej url, gdzięki któremu możemy uzyskać sumę 2 liczb
@app.route('/addNumbers/<int:first>/<int:second>')
def add_numbers(first, second):
    return str(first + second)


# Parametry możemy też przekazywać do szablonu
@app.route('/hello/<name>')
def hello_extended(name):
    return render_template('hello.html', name=name)


# Możemy definiować różne rodzaje zapytań wykorzystując polecenia REST API, jak np. POST
@app.route('/helloPost/', methods=['POST'])
def hello_post():
    return render_template('hello.html', name=request.form['name'])


# Dane możemy przesyłać też w formacie Json
@app.route('/helloJson/', methods=['POST'])
def hello_json():
    return render_template('hello.html', name=request.json['name'])


# Możemy tworzyć ciasteczka - pliki lokalne przechowujące wartości
@app.route('/set_cookie/<string:cookie>')
def set_cookie(cookie):
    resp = make_response('You set cookie value as: ' + cookie)
    resp.set_cookie('my_cookie', cookie)
    return resp


# A także odczytywać ich wartość
@app.route('/get_cookie')
def get_cookie():
    return request.cookies.get('my_cookie')


# W obiekcie app mamy słownik config, do którego możemy przypisywać parametry - w tym wypadku będzie to nazwa pliku z
# bazą
app.config['DATABASE'] = 'flask.sqlite'
# Inicjalizacja połączenia z bazą
db.init_app(app)


# Jedyną funkcją możemy obsługiwać wiele poleceń REST API
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        db.get_db().execute("Insert INTO post VALUES(NULL,?,?,?)",
                            (request.json['author'], request.json['title'], request.json['body']))
        db.get_db().commit()  # Każda operacja zakończona modyfikacją bazy musi zostać zakończona przez commit
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()  # Domyślnie jest zwracany kursor - czyli obiekt bazodanowy działający na jedenym wierszu,
    # fetchall pobierze wszystkie wiersze
    return render_template('blog.html', posts=data)


# Tutaj mamy przykład wykorzystania szablonu rozszerzającego inny szablon
@app.route('/blog_extends')
def blog_extends():
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()
    return render_template('blogExtends.html', posts=data)


# Tutaj mamy nieco bardziej złożony szblon wykorzystujący bootstrap oraz plik css. Pliki wykorzystywane przez szablon
# (np. css, czy skrypty js) przechowywane są w folderze static
@app.route('/blog_pretty', methods=['GET', 'POST'])
def blog_pretty():
    if request.method == 'POST':
        db.get_db().execute("Insert INTO post VALUES(NULL,?,?,?)",
                            (request.json['author'], request.json['title'], request.json['body']))
        db.get_db().commit()
    cur = db.get_db().execute("SELECT * FROM post")
    data = cur.fetchall()
    return render_template('blogPretty.html', posts=data)
