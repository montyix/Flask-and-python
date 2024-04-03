from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/Monty'
db = SQLAlchemy(app)

# Define models
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Person(name='{self.name}')>"

class Things(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    owner = db.relationship("People", backref="things")

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def __repr__(self):
        return f"<Thing(name='{self.name}', owner='{self.owner.name}')>"

# Routes
@app.route('/')
def index():
    return 'Welcome to Monty database!'

@app.route('/add_sample_data')
def add_sample_data():
    person1 = People(name='Alice')
    person2 = People(name='Bob')

    thing1 = Things(name='Book', owner=person1)
    thing2 = Things(name='Laptop', owner=person2)

    db.session.add_all([person1, person2, thing1, thing2])
    db.session.commit()
    return 'Sample data added successfully.'

@app.route('/people')
def get_people():
    people = People.query.all()
    return jsonify([{'id': person.id, 'name': person.name} for person in people])

@app.route('/things')
def get_things():
    things = Things.query.all()
    return jsonify([{'id': thing.id, 'name': thing.name, 'owner': thing.owner.name} for thing in things])

if __name__ == '__main__':
    app.run(debug=True)
