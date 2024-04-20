from __init__ import app
from orm import ORM

if __name__ == '__main__':
    ORM.create_tables()
    app.run(debug=False, host="0.0.0.0")