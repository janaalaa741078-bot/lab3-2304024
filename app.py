import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='Janaalaa2005',
        database='library_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('library'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
        conn.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('library'))
        else:
            flash('Incorrect username or password!', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                flash('Account already exists!', 'warning')
            else:
                cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
                conn.commit()
                flash('Successfully registered! Please login.', 'success')
                conn.close()
                return redirect(url_for('login'))
        conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/library')
def library():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM author')
        authors = cursor.fetchall()

        cursor.execute('''
            SELECT book.*, author.name AS author_name 
            FROM book 
            LEFT JOIN author ON book.author_id = author.author_id
        ''')
        books = cursor.fetchall()
    conn.close()

    return render_template('library.html', authors=authors, books=books)

@app.route('/author/add', methods=['GET', 'POST'])
def add_author():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        author_id = request.form.get('author_id')
        name = request.form['name']
        country = request.form.get('country', '')

        conn = get_db_connection()
        with conn.cursor() as cursor:

            if author_id:
                cursor.execute('SELECT * FROM author WHERE author_id = %s', (author_id,))
                if cursor.fetchone():
                    flash('Author ID already exists!', 'danger')
                    conn.close()
                    return render_template('add-author.html')

            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            if author_id:
                cursor.execute(
                    'INSERT INTO author (author_id, name, country, image) VALUES (%s, %s, %s, %s)',
                    (author_id, name, country, image_filename)
                )
            else:
                cursor.execute(
                    'INSERT INTO author (name, country, image) VALUES (%s, %s, %s)',
                    (name, country, image_filename)
                )
            conn.commit()
        conn.close()
        return redirect(url_for('library'))

    return render_template('add-author.html')

@app.route('/author/edit/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        country = request.form.get('country', '')

        with conn.cursor() as cursor:
            cursor.execute('SELECT image FROM author WHERE author_id = %s', (id,))
            existing = cursor.fetchone()
            image_filename = existing['image'] if existing else None

            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            cursor.execute(
                'UPDATE author SET name = %s, country = %s, image = %s WHERE author_id = %s',
                (name, country, image_filename, id)
            )
            conn.commit()
        conn.close()
        return redirect(url_for('library'))

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM author WHERE author_id = %s', (id,))
        author = cursor.fetchone()
    conn.close()

    return render_template('edit_author.html', author=author)

@app.route('/author/delete/<int:id>')
def delete_author(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM author WHERE author_id = %s', (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('library'))

@app.route('/book/add', methods=['GET', 'POST'])
def add_book():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        book_id = request.form.get('book_id')
        title = request.form['title']
        author_id = request.form['author_id']
        price = request.form.get('price', 0.0)

        with conn.cursor() as cursor:

            if book_id:
                cursor.execute('SELECT * FROM book WHERE book_id = %s', (book_id,))
                if cursor.fetchone():
                    flash('Book ID already exists!', 'danger')
                    cursor.execute('SELECT * FROM author')
                    authors = cursor.fetchall()
                    conn.close()
                    return render_template('add_book.html', authors=authors)

            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            if book_id:
                cursor.execute(
                    'INSERT INTO book (book_id, title, author_id, price, image) VALUES (%s, %s, %s, %s, %s)',
                    (book_id, title, author_id, price, image_filename)
                )
            else:
                cursor.execute(
                    'INSERT INTO book (title, author_id, price, image) VALUES (%s, %s, %s, %s)',
                    (title, author_id, price, image_filename)
                )
            conn.commit()
        conn.close()
        return redirect(url_for('library'))

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM author')
        authors = cursor.fetchall()
    conn.close()

    return render_template('add_book.html', authors=authors)

@app.route('/book/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        price = request.form.get('price', 0.0)

        with conn.cursor() as cursor:
            cursor.execute('SELECT image FROM book WHERE book_id = %s', (id,))
            existing = cursor.fetchone()
            image_filename = existing['image'] if existing else None

            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            cursor.execute(
                'UPDATE book SET title = %s, author_id = %s, price = %s, image = %s WHERE book_id = %s',
                (title, author_id, price, image_filename, id)
            )
            conn.commit()
        conn.close()
        return redirect(url_for('library'))

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM book WHERE book_id = %s', (id,))
        book = cursor.fetchone()
        cursor.execute('SELECT * FROM author')
        authors = cursor.fetchall()
    conn.close()

    return render_template('edit_book.html', book=book, authors=authors)

@app.route('/book/delete/<int:id>')
def delete_book(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM book WHERE book_id = %s', (id,))
        conn.commit()
    conn.close()
    return redirect(url_for('library'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)