import pymysql
from app.my_project import db

def call_procedure(name, args=()):
    connection = db.session.connection().connection
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.callproc(name, tuple(args))
        rows = list(cursor.fetchall())
        while cursor.nextset():
            pass
        db.session.commit()
        return rows
    except Exception:
        db.session.rollback()
        raise
    finally:
        cursor.close()
