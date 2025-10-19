from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # optional but recommended

# Initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

with app.app_context():
    db.create_all()
@app.route('/')
def home():
    all_users = User.query.all()
    return render_template('index.html',all_users=all_users)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_User = User(
            username = username,
            password = password,
        )
        db.session.add(new_User)
        db.session.commit()
        return redirect('/')
    return render_template("register.html")


@app.route('/update/<sno>', methods=['GET', 'POST'])
def update(sno):
    user = User.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template("update.html", user=user)


@app.route('/delete/<sno>', methods=['GET', 'POST'])
def delete(sno):
    user = User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)