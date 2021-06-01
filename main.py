import json
import model
from flask import abort, jsonify, request
from config import app, connect_db, db

HOST = '127.0.0.1'
PORT = '5000'


@app.route('/author/', methods=['GET', 'POST'])
def author():
    if request.method == 'GET':
        all_authors = model.Author.query\
            .order_by(model.Author.last_name).all()
        author_schema = model.AuthorSchema(many=True)
        response = jsonify(author_schema.dump(all_authors))
        return response
    if request.method == 'POST':
        new_author = json.loads(request.get_json())
        first_name = new_author.get('first_name')
        middle_name = new_author.get('middle_name')
        last_name = new_author.get('last_name')
        author_already_exists = model.Author.query\
            .filter(model.Author.first_name == first_name)\
            .filter(model.Author.middle_name == middle_name)\
            .filter(model.Author.last_name == last_name)\
            .one_or_none()
        if author_already_exists:
            abort(409, 'Author {} {} {} already exists.'
                  .format(first_name, middle_name, last_name))
        author_schema = model.AuthorSchema()
        new_author = author_schema.load(
            new_author, session=db.session
            )
        db.session.add(new_author)
        db.session.commit()
        response = jsonify(author_schema.dump(new_author))
        return response
    abort(405, 'Method not allowed.')


@app.route('/author_record/<author_id>/',
           methods={'GET', 'PATCH', 'PUT', 'DELETE'})
def author_record(author_id):
    if request.method == 'GET':
        record = model.Author.query\
            .filter(model.Author.id == author_id)\
            .one_or_none()
        if record is None:
            abort(404, 'Author with id {} not found.'
                  .format(author_id))
        author_schema = model.AuthorSchema()
        response = jsonify(author_schema.dump(record))
        return response
    if request.method == 'PUT':
        pass
    abort(405, 'Method not allowed.')


@app.route('/connect/', methods=['GET'])
def connect():
    try:
        with open('config.json') as file:
            login_info = json.load(file)
        connect_db(app, db, login_info)
    except Exception as e:
        return str(e)
    return 'Connected to {}'.format(db.engine)


@app.route('/', methods=['GET'])
def home():
    return ''


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
