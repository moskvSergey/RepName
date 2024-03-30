from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employers.db'
db = SQLAlchemy(app)

"""
class Employers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Article %r>' % self.id
    """
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/enter')
def enter():
    return render_template('open.html')

if __name__ == '__main__':
    app.run()
