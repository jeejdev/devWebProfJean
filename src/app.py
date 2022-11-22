from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL

def create_app():
    from app import routes
    routes.init_app(app)

    return app

app = Flask(__name__)

# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost' # 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'contatos'

mysql = MySQL(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template('public/index.html')

@app.route("/quemsomos")
def quemsomos():
    return render_template('public/quemsomos.html')

@app.route("/contatos")
def contatos():
    return render_template('public/contatos.html')

@app.route("/users", methods=['GET'])
def usersGet():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CONTATOS")
    todosChamados = cur.fetchall()
    return render_template('public/users.html', todosChamados = todosChamados)

@app.route('/contatos', methods=['GET', 'POST'])
def contatosPost():
    if request.method == "POST":
        email = request.form['email']
        assunto = request.form['assunto']
        descricao = request.form['desc']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contatos(email, assunto, `desc`) VALUES (%s, %s, %s)", (email, assunto, descricao))
       
        mysql.connection.commit()
        cur.close()
    return render_template('public/contatos.html')