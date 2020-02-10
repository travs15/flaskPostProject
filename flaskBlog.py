from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import  RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bce366eec07e95abbd1e9556ba0dc34b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# modelos de datos
# lazy carga los datos desde la base de datos de una vez cuando es true
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #la relacion se entabla con el modelo de Post escrito abajo
    #backref referencia para saber que autor ha creado el post
    #lazy, cuando carga la data del database, en una sol carga
    ## relacion de 1 a muchos 
    # 'Post' porque estamos referenciando la clase

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
        # asi se van a ver los resultados cuando se pidan los datos

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    # primer argumento la primarykey
    # segundo llave foranea que es el id del usuario
    # 'user.attr' refernciando la tabla y una columna porque es lowercase

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'Corey Shafer',
        'title': 'Blog Post1',
        'content': 'First post content',
        'date_posted': 'April 20 , 2018'
    },
    {
        'author': 'Alejandro reyes ',
        'title': 'Blog Post1',
        'content': 'First post content',
        'date_posted': 'April 21 , 2018'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title = "About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Acount created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title = "Register", form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, check your password','danger')

    return render_template('login.html', title = "Login", form = form)    

if __name__ == "__main__":
    app.run(debug=True)
