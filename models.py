from __init__ import db
from datetime import datetime, timedelta


class Workers(db.Model):
    __tablename__ = "Workers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(300), nullable=False)
    first_name = db.Column(db.String(300), nullable=False)
    surname = db.Column(db.String(300), nullable=False)
    tabel = db.Column(db.String(300), nullable=False)
    snils = db.Column(db.String(300), nullable=False)
    license_number = db.Column(db.String(300), nullable=False)
    license_date = db.Column(db.DateTime, nullable=False)
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
    type = db.Column(db.String(300), nullable=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow)
    date_ended = db.Column(db.DateTime,  nullable=True, default=lambda: datetime.utcnow() + timedelta(hours=12))
    odometer = db.Column(db.Integer, nullable=False)
    diesel = db.Column(db.Integer, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('Workers.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicles.id'))

    @staticmethod
    def select_all():
        return Shifts.query.all()
