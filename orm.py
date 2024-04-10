from __init__ import db, app
from models import Workers, Vehicles, Shifts

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