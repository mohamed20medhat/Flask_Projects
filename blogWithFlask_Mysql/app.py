from logging import error
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
#from data import Article
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__) 
# Config MySQL
#! don't forget to configure the db "it's name, and username and password"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yourUserName'
app.config['MYSQL_PASSWORD'] = 'yourPassword'
app.config['MYSQL_DB'] = 'yourDBname'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


#test when we got the articles from the python file
#Articles = Article()

# so far we used flask to render html templates and pass data to them when we go to the certain port of the server. like making the vs code live server but from the inside. 

#index
@app.route('/')
def index():
    return render_template('home.html')

#about
@app.route('/about')
def about():
    return render_template('about.html')

# all the articles page
@app.route('/articles')
def articles():
    #create cursoir
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM articles")

    #fetch all the articles into a dictionary and then pass it to the template.
    articles = cur.fetchall()

    # if the result is greater than 0 = "if there are articles"
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

    #close connection
    cur.close()

#single article
# notice how we pass the id to the templete and then use the id to get the data from the database.
@app.route('/article/<string:id>')
def article(id):
    #create cursoir
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    #fetch all the articles into a dictionary and then pass it to the template.
    article = cur.fetchone()

    return render_template('article.html', article=article)

#register form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

#user regester
# notice that we pass the form to the template.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login')) #return to the index if didn't work.

    return render_template('register.html', form=form)     

# user login
#switch to index if login doesn't work.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #get form fields
        # we set it in the normal way without using wt form.
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # get uesr by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])

        if result > 0:
            #get *the first user* to match the username
            #this is really bad. we should use a for loop to get all the users. or store them on an array and then use a for loop to get all the users.
            data = cur.fetchone()
            # we can access it this way cause we get the data in a dictionary. not a tuple.
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))


            else:
                error = "invalid login"
                return render_template('login.html', error=error)
            #close connection after checking the password
            cur.close()
        else:
            error = "Username not found"
            return render_template('login.html', error=error)

    
    return render_template('login.html')

#check if user is logged in and make sure they are logged in before they can access any url.
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap



#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


#dashboard for the user
@app.route('/dashboard')
@is_logged_in
def dashboard():
    #create cursoir
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM articles")

    #fetch all the articles into a dictionary and then pass it to the template.
    articles = cur.fetchall()

    # if the result is greater than 0 = "if there are articles"
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    
    #close connection
    cur.close()


# Article form class
# we use the class for adding and editing articles
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


#notice that the default is get. so when we need to use post we must set it in the route like this.
#add article
@app.route('/add_article', methods=['GET', 'POST'])
#another page that the user must be logged in to access. so we used the decorator that we created previously
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        #create cursor
        cur = mysql.connection.cursor()

        #execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


#edit article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    #create cursor
    cur = mysql.connection.cursor()

    #get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    #get form
    form = ArticleForm(request.form)

    #populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']


    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        #create cursor
        cur = mysql.connection.cursor()

        #execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title,body,id))

        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    #create cursor
    cur = mysql.connection.cursor()

    #execute
    cur.execute("DELETE FROM articles WHERE id=%s", [id])

    #commit to db
    mysql.connection.commit()

    #close connection
    cur.close()

    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)




















