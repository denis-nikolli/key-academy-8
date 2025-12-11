import json
from flask import jsonify, request, abort
from flasgger import Swagger
from bookstore import app

swagger = Swagger(app)



def load_books():
    with open('bookstore/books.json', 'r') as file:
        return json.load(file)


def save_books(books):
    with open('bookstore/books.json', 'w') as file:
        json.dump(books, file, indent=4)


@app.route('/books', methods=['GET'])
def get_books():
    """List all books
    ---
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              name:
                type: string
              author:
                type: string
              isbn:
                type: string
              price:
                type: number
    """
    books=load_books()
    return jsonify(books), 200


@app.route('/book/<int:book_id>', methods=['POST'])
def add_book(book_id):
    """Add a new book
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: The ID of the book
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            author:
              type: string
            isbn:
              type: string
            price:
              type: number
    responses:
      201:
        description: Book created
      400:
        description: Book ID already exists or invalid input
    """
    books = load_books()
    if any(book['id'] == book_id for book in books):
        abort(400, description="Book ID already exists.")
    book_data = request.json
    testing_variable = book_data['name']
    required_fields = ['name', 'author', 'isbn', 'price']
    if not all(field in book_data for field in required_fields):
        abort(400, description="Missing required fields.")
    new_book = {
        "id": book_id,
        "name": book_data['name'],
        "author": book_data['author'],
        "isbn": book_data['isbn'],
        "price": book_data['price']
    }
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201


@app.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update the price of a book
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: The ID of the book
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            price:
              type: number
    responses:
      201:
        description: Updated book
      404:
        description: Book not found
    """
    books = load_books()
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        abort(404, description="Book not found.")
        
    book['price'] = request.json.get('price', book['price'])
    save_books(books)
    return jsonify(book), 201


@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: The ID of the book
    responses:
      200:
        description: Book deleted
      404:
        description: Book not found
    """
    books = load_books()
    book = next((book for book in books if book['id'] == Book_id), None)
    if book is None:
        abort(404, description="Book not found.")
    books = [book for book in books if book['id'] != book_id]
    save_books(books)
    return jsonify({"message": "Book deleted."}), 200
