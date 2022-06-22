from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


# endpoint
@app.route('/')
def index():
    return "Hello!"


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"drinks": output}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    # as dictionary is serializable, so we don't need to call jsonify
    # return jsonify({"name": drink.name, "description": drink.description})
    return {"name": drink.name, "description": drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    """
    https://web.postman.co/workspace/My-Workspace~23b4f037-e88d-476f-8504-a91a3dde1ff8/request/create?requestId=e11ab634-8bfd-40cf-93bc-7a9d9e8bafe4
    use postman to test
    :return:
    """
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "successfully delete!"}


@app.route('/drinks/<id>', methods=['PUT'])
def update_drink(id):
    # must add dict
    Drink.query.filter_by(id=id).update(dict(description="yo little little p!"))
    db.session.commit()
    return {"message": "updated!"}

