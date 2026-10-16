import json
from flask import Flask,render_template
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
    if connection:
        requete = connection.cursor()
        requete.execute("select * from seances order by id desc")
        resultat = requete.fetchall()
        connection.close()
        return resultat
    else:
        return 'abc'

if __name__ == '__main__':
    app.run()
