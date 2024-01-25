import psycopg2
from Lab_6.helpers.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

user = '> '


def connect_db():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = connection.cursor()

    return cursor


def db_sign_in(username, password):
    cursor = connect_db()

    query = "SELECT * FROM patient WHERE username = %s AND password = %s;"

    cursor.execute(query, (username, password))

    results = cursor.fetchone()

    if results:
        print(results[0], results[3], results[4])
        user = username
    else:
        print('\nUsername or password is not valid\n')


def db_sign_in_staff(email, password):
    cursor = connect_db()

    query = "SELECT first_name, last_name FROM staff WHERE email = %s AND password = %s;"

    cursor.execute(query, (email, password))

    results = cursor.fetchall()

    if results:
        print(results)
    else:
        print('\nUsername or password is not valid\n')
