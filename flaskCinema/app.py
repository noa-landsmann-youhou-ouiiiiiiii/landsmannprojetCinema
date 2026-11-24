from flask import Flask, render_template, redirect, url_for, jsonify
import pymysql
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
                try:
                    id_seance = seances[i]["id"]
                    id_seance_2 = seances[i+1]["id"]
                    id_seance_3 = seances[i+2]["id"]
                    break
                except IndexError:
                    return "Erreur : aucune séance programmée dans les prochains jours"
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

def prochaines_seances(id_film):
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("select current_timestamp")
        date_actuelle = cursor.fetchall()
        cursor.execute(f"select * from seances where id={id_film} order by heure asc")
        seances = cursor.fetchall()
        i = 0
        for row in seances:
            if row["heure"] > date_actuelle[0]["current_timestamp"]:
                id_seance = seances[i]["id"]
                # id_seance_2 = seances[i + 1]["id"]
                # id_seance_3 = seances[i + 2]["id"]
                # id_seance_4 = seances[i + 3]["id"]
                # id_seance_5 = seances[i + 4]["id"]
                # id_seance_6 = seances[i + 5]["id"]
                # id_seance_7 = seances[i + 6]["id"]
                # id_seance_8 = seances[i + 7]["id"]
                # id_seance_9 = seances[i + 8]["id"]
                # id_seance_10 = seances[i + 9]["id"]
                break
            else:
                pass
            i += 1
        cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        prochaine_seance = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance2 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance3 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance4 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance5 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance6 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance7 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance8 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance9 = cursor.fetchall()
        # cursor.execute(f"select * from seances join films on seances.id_film=films.id where seances.id={id_seance}")
        # seance10 = cursor.fetchall()
    else:
        return 'Echec de connexion mysql'
    return prochaine_seance


@app.route('/film/<abc>/')
def film(abc):
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(f"select * from films where id={abc}")
        film = cursor.fetchone()
        print(film)
        return render_template('film.html', film=film)
    else:
        return 'Echec de connexion mysql'

@app.route('/film')
def oui():
    return redirect(url_for('accueil'))

@app.route('/getseances/<numero_salle>')
def get_seance(numero_salle):
    connection = get_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(f"SELECT heure, films.titre, version, films.interdiction_moins_de_16_ans FROM `seances` JOIN salles ON seances.id_salle = salles.id JOIN films ON seances.id_film = films.id WHERE DATE(seances.heure) = CURRENT_DATE AND salles.numero = {numero_salle} ORDER BY heure ASC")
        seance = cursor.fetchall()
        return jsonify(seance)
    return None


if __name__ == '__main__':
    app.run()
