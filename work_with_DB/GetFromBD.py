from Models.models import Login
import psycopg2
from work_with_DB.conn import connection


async def getFromDBlogin(login: Login):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute('''SELECT fio, "group", id 
        FROM users 
        WHERE email = %s AND password = %s''', (login.email, login.password,))
        data = cur.fetchone()
        if data is None:
            return False
        return {"fio": data[0], "group": data[1], "id": data[2]}
    except (Exception, psycopg2.Error) as error:
        return {"Error": error}
    finally:
        if conn is not None:
            conn.close()
            cur.close()


async def get_subjects(id):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute('''SELECT array_agg(sub.sub_name), array_agg(connect.grade), array_agg(connect.semester) 
        FROM connect 
        JOIN users ON connect.group = users.id
        JOIN subjects sub ON connect.subject = sub.id
        WHERE users.id = %s
        GROUP BY users.id''', (id,))
        data = cur.fetchall()
        if data is None:
            return False
        return {x[0]: {"grade": x[1], "semester": x[2]}
                for x in zip(data[0][0], data[0][1], data[0][2])}
    except (Exception, psycopg2.DatabaseError) as error:
        return {"error": error}
    finally:
        if conn is not None:
            conn.close()
            cur.close()


async def get_all_achievements(id):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute('''SELECT array_agg("date"), array_agg(type), array_agg("describe")
        FROM achievements
        WHERE achievements.user = %s''', (id,))
        data = cur.fetchall()
        if data is None:
            return False
        return [{"date": x[0], "type": x[1], "describe": x[2]}
                for x in zip(data[0][0], data[0][1], data[0][2])]
    except (Exception, psycopg2.DatabaseError) as error:
        return {"error": error}
    finally:
        if conn is not None:
            conn.close()
            cur.close()


async def get_all_my_teachers(id):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute('''SELECT array_agg(fio) , array_agg(department), array_agg(sub.sub_name)
        FROM connect con
        JOIN teacher tea ON con.subject = tea.subject
        JOIN subjects sub ON con.subject = sub.id
        WHERE "group" = %s''', (id,))
        data = cur.fetchall()
        if data is None:
            return False
        return [{"fio": x[0], "department": x[1], "sub_name": x[2]}
                for x in zip(data[0][0], data[0][1], data[0][2])]
    except (Exception, psycopg2.DatabaseError) as error:
        return {"error": error}
    finally:
        if conn is not None:
            conn.close()
            cur.close()
