from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
import bcrypt                                    #for hashed passwords
import re                                        #for validation email
from password_validator import PasswordValidator
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


MY_EMAIL = os.getenv("EMAIL_MY_EMAIL")
MY_PASSWORD = os.getenv("EMAIL_MY_PASSWORD")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e:/PROJECTS/log in flask/db/users.db'
app.config['SECRET_KEY'] = [os.getenv("SECRET_KEY_DB")]
db = SQLAlchemy(app)


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/submit_form', methods=['GET'])
def submit_form():
    customer_email = request.args.get('emailContact')
    customer_name = request.args.get('fullNameC')
    customer_message = request.args.get('customer_message')

    try:
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)

        msg = MIMEText(f"Customer email: {customer_email}\n\n"
                             f"Customer name: {customer_name}\n\n"
                             f"Customer message:{customer_message}", 'plain', 'utf-8')

        msg['Subject'] = "Customer feedback"
        connection.sendmail(
            from_addr=customer_email,
            to_addrs=MY_EMAIL,
            msg=msg.as_string()
        )
    except Exception as ex:
        print(ex)

    return jsonify({"message": "successfully send", "email": customer_email})


@app.route('/product')
def product_page():
    return render_template('product.html')


@app.route('/product2')
def product_second_page():
    return render_template('product_secondPage.html')


@app.route('/product3')
def product_third_page():
    return render_template('product_thirdPage.html')


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


## Адмін панель в яку буде входити змога адміна добавляти асортимент змінювати ціни і тд

## Функція яка буде первіряти чи користувач зареєстрований, якщо це True автоматично давати знижку на весь асортимент

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email_data_from_input = request.form.get('email')
    password_data_from_input = request.form.get('password')

    try:
        user = Users.query.filter_by(email=email_data_from_input).one()
        check_passwords = bcrypt.checkpw(password=password_data_from_input.encode('utf-8'),
                                         hashed_password=user.password)

        if user and check_passwords:
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

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email_reg):
        print(True)
    else:
        return jsonify({"message": "Invalid email address"}), 400

    if not password_1 or not password_2:
        return jsonify({'message': 'Password fields cannot be empty'}), 400

    password_validator = PasswordValidator()

    password_validator.min(6).max(20).has().lowercase().has().uppercase().has().digits().has().symbols()
    is_valid = password_validator.validate(password_1)

    if is_valid:
        print('Password is valid')
    else:
        return jsonify({"message": "Invalid password, Password must have at list one Upper Case,"
                                   " digits, symbols and range 6-20"})

    if password_1 != password_2:
        return jsonify({'message': 'The password does not matches'}), 400

    existing_user = Users.query.filter_by(email=email_reg).first()
    if existing_user:
        return jsonify({'message': 'Email is already registered'}), 400

    else:
        role = 'User'
        hashed_password_1 = bcrypt.hashpw(password_1.encode('utf-8'), bcrypt.gensalt())
        new_user = Users(email=email_reg, password=hashed_password_1, role=role)
        db.session.add(new_user)
        db.session.commit()

    return jsonify({'message': 'Created account'}), 201


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

