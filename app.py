from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy, query, session
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e:/PROJECTS/log in flask/db/users.db'
app.config['SECRET_KEY'] = 'dimadima milavika dimadima'
db = SQLAlchemy(app)


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    confirm_password = db.Column(db.String(50))
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


@app.route('/try')
def try_page():
    return render_template('try_xyi.html')


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
    email_reg = request.form.get('email')
    password_1 = request.form.get('password1')
    password_2 = request.form.get('password2')

    if len(email_reg) < 4:
        return jsonify({'message': 'The email must be more then 4 symbols'})

    elif len(password_1) <= 8:
        return jsonify({'message': 'The password must be more then 8 symbols'})

    elif password_1 != password_2:
        return jsonify({'message': 'The password does not matches'})

    else:
        new_user = Users(email=email_reg, password=password_1, confirm_password=password_2)
        db.session.add(new_user)
        db.session.commit()

    return jsonify({'message': 'Created account'}), 201


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

