from unicodedata import name
from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, jsonify
import json
import ast
from time import sleep


app = Flask(__name__)
mysql = MySQL(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "couchie"
app.config["MYSQL_DB"] = "foods"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/info")
def info():
    return render_template("info.html")    

@app.route('/info/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        food = request.form['food']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from food_item WHERE food_name = '%s';" % (food))
        data = cursor.fetchall()
        print (type(data))
        
        return render_template('start.html', data=data)

    return render_template("start.html")

@app.route('/info/more_info')
def more_info():
    return render_template("more_info.html")

#for daily log, not functioning yet
@app.route('/info/start/daily_log', methods=['GET', "POST"])
def daily_log():
    if request.method == 'POST':
        foodName = request.form['foodName']
        foodCarbon = request.form['foodCarbon']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO foodLog (foodName, foodCarbon) VALUES ('%s', '%s')" % (foodName, foodCarbon))
    return render_template("daily_log.html")


# for user logins, not functioning yet
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method =='POST':
        user = request.form['nm']
        return redirect(url_for("user", usr=user))
    else:
        return render_template('login.html')

# For integrating Sophie's microservice
@app.route('/info/start/activity')
def activity():
    data = {}
    with open('request_most_popular.txt', 'w') as f:
        f.write('WHAT_IS_THE_MOST_POPULAR_ACTIVITY')
        f.close()
    while True:
        with open('activity.txt', 'r') as f:
            line = f.read()
            f.close()
        if not line:
            continue
        else:
            with open('activity.txt', 'w') as f:
                f.write('')
                f.close
            data = json.loads(line)
            print(data)
            return render_template('activity.html', line=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3308, debug=True)