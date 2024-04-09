from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employers.db'
db = SQLAlchemy(app)


class Workers(db.Model):
    __tablename__ = "Workers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(300), nullable=False)
    first_name = db.Column(db.String(300), nullable=False)
    key = db.Column(db.String(300), nullable=False)

    @staticmethod
    def select_all():
        return Workers.query.all()


class Vehicles(db.Model):
    __tablename__ = "Vehicles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(300), nullable=False)
    plate = db.Column(db.String(300), nullable=False)

    @staticmethod
    def select_all():
        return Vehicles.query.all()

class Shifts(db.Model):
    __tablename__ = "Shifts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_started = db.Column(db.DateTime, default=datetime.utcnow)
    date_ended = db.Column(db.DateTime,  nullable=True, default=None)
    odometer = db.Column(db.Integer, nullable=False)
    diesel = db.Column(db.Integer, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('Workers.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicles.id'))

    @staticmethod
    def select_all():
        return Shifts.query.all()

class ORM:
    @staticmethod
    def create_tables():
        with app.app_context():
            db.create_all()
    @staticmethod
    def get_table(table):
        if table == "Workers": return Workers
        if table == "Vehicles": return Vehicles
        if table == "Shifts": return Shifts

    @staticmethod
    def insert(table, data):
        table = ORM.get_table(table)
        with app.app_context():
            new_data = table(**data)
            print(new_data)
            db.session.add(new_data)
            db.session.commit()

    @staticmethod
    def select(table, id='All'):
        table = ORM.get_table(table)
        with app.app_context():
            rows = table.select_all()
            if id == 'All': return rows
            for row in rows:
                if row.id == id:
                    return row

    @staticmethod
    def update(table, old_id, new_data):
        table = ORM.get_table(table)
        with app.app_context():
            old = db.session.query(table).get(old_id)
            for key, value in new_data.items():
                setattr(old, key, value)
            db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def enter():
    ORM.create_tables()
    if request.method == "POST":
        key = request.form['KeyInput']
        return redirect(url_for('worker_shifts', key=key))
    else:
        return render_template('enter.html')

@app.route('/user/<key>', methods=['POST', 'GET'])
def worker_shifts(key):
    if request.method == 'POST':
        return redirect(url_for('new_shift', key=key))
    else:
        worker = Workers.query.filter_by(key=key).first()
        if worker is None:
            return "Пользователь не найден"
        else:
            shifts = Shifts.query.filter_by(employer_id=worker.id, date_ended=None).all()
            return render_template('user.html', worker=worker, shifts=shifts)


@app.route('/user/<key>/new_shift', methods=['POST', 'GET'])
def new_shift(key):
    if request.method == 'POST':
        vehicle_id = request.form['vehicle']
        odometer = request.form['odometer']
        fuel = request.form['fuel']
        worker = Workers.query.filter_by(key=key).first()

        new_shift = Shifts(vehicle_id=vehicle_id, odometer=odometer, diesel=fuel, employer_id=worker.id)
        db.session.add(new_shift)
        db.session.commit()

        return redirect(url_for('worker_shifts', key=key))
    else:
        vehicles = Vehicles.query.all()
        worker = Workers.query.filter_by(key=key).first()
        print(worker)
        return render_template('new_shift.html', vehicles=vehicles, worker=worker)



@app.route('/user/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        sql_query = request.form['sql_query']
        try:
            result = db.session.execute(text(sql_query))
            if result.returns_rows:
                result_set = [dict(row) for row in result]
                return render_template('admin.html', result_set=result_set)
            else:
                db.session.commit()
                print("Запрос выполнен успешно")
        except Exception as e:
            print("Ошибка:", str(e))

    workers = ORM.select('Workers')
    vehicles = ORM.select('Vehicles')
    shifts = ORM.select('Shifts')
    return render_template('admin.html', workers=workers, vehicles=vehicles, shifts=shifts)

if __name__ == '__main__':
    app.run()


