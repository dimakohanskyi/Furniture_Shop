from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash  # for password validation
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e:/PROJECTS/log in flask/db/users.db'
db = SQLAlchemy(app)


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    time = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/product')
def product_page():
    return render_template('product.html')


@app.route('/services')
def services_page():
    return render_template('services.html')


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')

@app.route('/location')
def location_page():
    return render_template('location.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email_data_from_input = request.form.get('email')
    password_data_from_input = request.form.get('password')

    try:
        user = Users.query.filter_by(email=email_data_from_input).one()

        # Compare the hashed password from the database with the input password
        if user and user.password == password_data_from_input:
            return render_template('index.html')
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    except NoResultFound:
        return jsonify({'message': 'User not found'}), 404


@app.route('/register_validation', methods=['GET', 'POST'])
def register_validation():
    name_reg = request.form.get('name_reg')
    email_reg = request.form.get('email')
    password_reg = request.form.get('password')

    new_user = Users(name=name_reg, email=email_reg, password=password_reg)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Created account'}), 201


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

