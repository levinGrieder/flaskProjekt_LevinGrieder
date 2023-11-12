from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
books = [
    {"id": 1, "title": "Buch 1", "author": "Autor 1"},
    {"id": 2, "title": "Buch 2", "author": "Autor 2"},
    {"id": 3, "title": "Buch 3", "author": "Autor 3"},
]

# Funktionen für die CRUD-Operationen
def get_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

def add_book(title, author):
    new_id = len(books) + 1
    new_book = {"id": new_id, "title": title, "author": author}
    books.append(new_book)
    return new_book

def update_book(book_id, title, author):
    book = get_book(book_id)
    if book:
        book['title'] = title
        book['author'] = author
        return book
    return None

def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]

# Routen und Views
@app.route('/')
def index():
    return render_template('index_books.html', books=books)

@app.route('/add', methods=['GET'])
def add_form():
    return render_template('add_book.html')

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    author = request.form.get('author')
    if title and author:
        add_book(title, author)
    return redirect(url_for('index'))

@app.route('/edit/<int:book_id>')
def edit(book_id):
    book = get_book(book_id)
    if book:
        return render_template('edit_book.html', book=book)
    return redirect(url_for('index'))

@app.route('/update/<int:book_id>', methods=['POST'])
def update(book_id):
    title = request.form.get('title')
    author = request.form.get('author')
    update_book(book_id, title, author)
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete(book_id):
    delete_book(book_id)
    return redirect(url_for('index'))

@app.route('/api/books', methods=['GET'])
def api_books():
    return jsonify(books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    book = get_book(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Buch nicht gefunden"}), 404

if __name__ == '__main__':
    app.run(debug=True)
