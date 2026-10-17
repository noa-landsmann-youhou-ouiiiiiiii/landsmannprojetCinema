from typing import Any

from flask import Flask,render_template
import pymysql
from pymysql.cursors import Cursor

from config import Config

app = Flask(__name__)

def get_connection():
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(e)
        return None
@app.route('/')
def accueil():
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("select current_timestamp")
        date_actuelle = cursor.fetchall()
        cursor.execute("select * from seances order by heure asc")
        seances = cursor.fetchall()
        i = 0
        for row in seances:
            if row["heure"] > date_actuelle[0]["current_timestamp"]:
                id_seance = seances[i]["id"]
                id_seance_2 = seances[i+1]["id"]
                id_seance_3 = seances[i+2]["id"]
                break
            else:
                pass
            i += 1
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        prochaine_seance = cursor.fetchall()
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance_2}")
        seance_2 = cursor.fetchall()
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance_3}")
        seance3 = cursor.fetchall()
        tableau = [prochaine_seance,seance_2,seance3]
    else:
        return None
    return render_template('index.html', tableau_seances=tableau)

@app.route('/seances')
def seances():
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("select current_timestamp")
        date_actuelle = cursor.fetchall()
        cursor.execute("select * from seances order by heure asc")
        seances = cursor.fetchall()
        i = 0
        for row in seances:
            if row["heure"] > date_actuelle[0]["current_timestamp"]:
                id_seance = seances[i]["id"]
                id_seance_2 = seances[i + 1]["id"]
                id_seance_3 = seances[i + 2]["id"]
                break
            else:
                pass
            i += 1
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        prochaine_seance = cursor.fetchall()
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance_2}")
        seance_2 = cursor.fetchall()
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance_3}")
        seance3 = cursor.fetchall()
        tableau = [prochaine_seance, seance_2, seance3]
    else:
        return None
    return render_template('seances.html', tableau_seances=tableau)

@app.route('/leemiller')
def leemiller():
    return render_template('film-leemiller.html')

@app.route('/croquette')
def croquette():
    return render_template('film-croquette.html')

@app.route('/smile')
def smile():
    return render_template('film-smile.html')


if __name__ == '__main__':
    app.run()
