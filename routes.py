from datetime import datetime

from flask import render_template, request, redirect, url_for, send_file
from sqlalchemy import text
from __init__ import app, db
from models import Workers, Vehicles, Shifts
from orm import ORM
import pandas as pd
from word_patterns.patterns import download_pl


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
            return render_template('error.html', Text="Такого пользователя нет.")
        else:
            shift = Shifts.query.filter(Shifts.employer_id == worker.id, Shifts.date_ended == None).first()
            if shift:
                car = Vehicles.query.filter(Vehicles.id == shift.vehicle_id).first()
            else:
                car = None
            return render_template('user.html', worker=worker, shift=shift, car=car)


@app.route('/user/<key>/new_shift', methods=['POST', 'GET'])
def new_shift(key):
    if request.method == 'POST':
        try:
            vehicle_id = request.form['vehicle']
            type = request.form['type']
            int(request.form['odometer'])
            int(request.form['fuel'])
            odometer = request.form['odometer']
            fuel = request.form['fuel']
            worker = Workers.query.filter_by(key=key).first()

            new_shift = Shifts(vehicle_id=vehicle_id, type=type, odometer_start=odometer, diesel_start=fuel, employer_id=worker.id)
            db.session.add(new_shift)
            db.session.commit()
        except:
            return render_template('error.html', Text="Некорректные данные")

        return redirect(url_for('worker_shifts', key=key))
    else:
        vehicles = Vehicles.query.all()
        worker = Workers.query.filter_by(key=key).first()
        return render_template('new_shift.html', vehicles=vehicles, worker=worker)

@app.route('/close/<int:id>', methods=['POST', 'GET'])
def close_shift(id):

    shift = Shifts.query.get(id)
    worker = Workers.query.get(shift.employer_id)
    car = Vehicles.query.get(shift.vehicle_id)

    if request.method == "POST":
        try:
            int(request.form['odometer'])
            int(request.form['fuel'])
            int(request.form['refill'])
            shift.odometer_end = request.form['odometer']
            shift.diesel_end = request.form['fuel']
            shift.refill = request.form['refill']
            shift.date_ended = datetime.now()
            db.session.commit()
        except Exception as e:
            print("Ошибка:", str(e))

        return render_template('error.html', Text="Некорректные данные")
    else:
        return render_template('close_shift.html', shift=shift, worker=worker, car=car)

@app.route('/user/404', methods=['GET', 'POST'])
def admin():
    workers = ORM.select('Workers')
    vehicles = ORM.select('Vehicles')
    shifts = ORM.select('Shifts')
    if request.method == 'POST':
        sql_query = request.form['sql_query']
        print(sql_query)
        try:
            result = db.session.execute(text(sql_query))
            if result.returns_rows:
                result_set = [{column: value for column, value in zip(result.keys(), row)} for row in result]
                return render_template('admin.html', result_set=result_set, workers=workers, vehicles=vehicles, shifts=shifts)
            else:
                db.session.commit()
                print("Запрос выполнен успешно")

                workers = ORM.select('Workers')
                vehicles = ORM.select('Vehicles')
                shifts = ORM.select('Shifts')

        except Exception as e:
            print("Ошибка:", str(e))

    return render_template('admin.html', workers=workers, vehicles=vehicles, shifts=shifts)

@app.route('/user/404/upload', methods=['GET', 'POST'])
def read_excel():
    if request.method == 'POST':
        file = request.files['file']

        if len(pd.read_excel(file, engine='openpyxl').columns) > 2:
            data = pd.read_excel(file, engine='openpyxl', names=[
                'last_name', 'first_name', 'surname', 'tabel', 'snils', 'license_number',
                'license_date', 'key'
            ],  index_col=None)
            data['license_date'] = pd.to_datetime(data['license_date']).dt.date

            for index, row in data.iterrows():
                existing_worker = Workers.query.filter_by(
                    last_name=row['last_name'],
                    first_name=row['first_name'],
                    surname=row['surname']
                ).first()

                if not existing_worker:
                    worker = Workers(
                        last_name=row['last_name'],
                        first_name=row['first_name'],
                        surname=row['surname'],
                        tabel=row['tabel'],
                        snils=row['snils'],
                        license_number=row['license_number'],
                        license_date=row['license_date'],
                        key=row['key']
                    )
                    db.session.add(worker)
        else:
            data = pd.read_excel(file, engine='openpyxl', names=['model', 'plate'], index_col=None)
            for index, row in data.iterrows():
                existing_car = Vehicles.query.filter_by(
                    model=row['model'],
                    plate=row['plate']
                ).first()

                if not existing_car:
                    car = Vehicles(
                        model=row['model'],
                        plate=row['plate']
                    )
                    db.session.add(car)

        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('upload-excel.html')


@app.route('/download/<int:id>', methods=['POST'])
def download(id):
    shift = Shifts.query.get(id)
    worker = Workers.query.get(shift.employer_id)
    car = Vehicles.query.get(shift.vehicle_id)
    try:
        answer = download_pl(shift,worker, car)[7:]
        return send_file(answer, as_attachment=True)
    except Exception as e:
        return render_template("error.html", Text=str(e))