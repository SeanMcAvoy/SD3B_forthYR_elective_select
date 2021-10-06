from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
# app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SEVER"] = "stmp.gmail.com"
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
#
# mail = Mail(app)
# https://www.w3schools.com/python/python_mysql_create_db.asp - link to help connect
mydb = mysql.connector.connect(
  host="localhost",
  user="Sean",
  password="seanmcavoy",
  database="elective",
  port="8889"
)
cursor = mydb.cursor()

app = Flask(__name__)

STUDENT_CHOICES = {}

ELECTIVES = [
    "Smart Technology",
    "AI",
    "Service Oriented Architecture",
    "Mobile IOS"
]


@app.route('/')
def index():
    return render_template("index.html", electives=ELECTIVES)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    elective = request.form.get("elective")
    if not name or not elective or elective not in ELECTIVES:
        return render_template("failure.html")
    STUDENT_CHOICES[name] = elective
    sql = "INSERT INTO student (Name, Elective) VALUES (%s, %s)"
    val = (name, elective)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close() #maybeNeeded
    # message = Message("You are Registered", recipients=[name])
    # mail.send(message)
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    cursor = mydb.cursor()
    sql = "SELECT name, elective from student"
    cursor.execute(sql)
    registrants = cursor.fetchall()
    cursor.close()
    return render_template("registrants.html", registrants=registrants)


app.run(debug=True)
