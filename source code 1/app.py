# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:36:31 2022

@author: ADMIN
"""


from flask import Flask, render_template, request,redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas as pd 
import numpy as np
import pickle
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)
app.secret_key = "flash_message"
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = 'wqms'
mysql = MySQL(app)


@app.route('/')
def landingpage():
    return render_template( 'landingpage.html' )

@app.route('/index')
def index():
    return render_template( 'index.html' )

@app.route('/intro')
def intro():
    return render_template( 'intro.html' )

@app.route('/ps')
def ps():
    return render_template( 'ps.html' )

@app.route('/scope')
def scope():
    return render_template( 'scope.html' )

@app.route('/objective')
def objective():
    return render_template( 'objective.html' )

@app.route('/crud')
def crud():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('crud.html', users=data)
    

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('crud'))
    
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
         id_data = request.form['id']
         name = request.form['name']
         email = request.form['email']
         phone = request.form['phone']
 
         cur = mysql.connection.cursor()
         cur.execute("""
            UPDATE users
             SET name=%s, email=%s, phone=%s
             WHERE id=%s
             """, (name, email, phone, id_data))
         flash("Data Updated Successfully")
         mysql.connection.commit()
         return redirect(url_for('crud'))
     
@app.route('/delete/<string:id_data>', methods=['POST','GET'])
def delete(id_data):
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id=%s", [id_data])
        mysql.connection.commit()
        return redirect(url_for('crud'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO accounts VALUES (% s, % s, % s)''', (username, password, email))
        mysql.connection.commit()
        msg = "You have successfully registered !"
    return render_template("register.html", msg=msg)


@app.route("/contact")
def contact():
    return render_template( 'contact.html' )

@app.route("/about")
def about():
    return render_template( 'about.html' )

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''SELECT * FROM accounts WHERE username = % s AND password = % s''', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = "Logged in successfully "
            return render_template("index.html", msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", msg=msg)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    
    # If a form is submitted
    if request.method == "POST":
        

        # Unpickle classifier
        clf1 = joblib.load("clfwq.pkl")
        
        # Get values through input bars
        do = request.form.get("do")
        ph = request.form.get("ph")
        orp = request.form.get("orp")
        ec = request.form.get("ec")
        tds = request.form.get("tds")
        temp = request.form.get("temp")
        cdo = request.form.get("cdo")
        cph = request.form.get("cph")
        corp = request.form.get("corp")
        cec = request.form.get("cec")
        ctds = request.form.get("ctds")
        cwt = request.form.get("cwt")
        
        # Put inputs to dataframe
        X = pd.DataFrame([[do, ph, orp, ec, tds, temp, cdo, cph, corp, cec, ctds, cwt ]], columns = ["Do", "Ph", "ORP", "EC", "TDS", "Water_Temp", "CDO","CpH","CORP", "CEC", "CTDS","CWT"])
        
        # Get prediction
        prediction1 = clf1.predict(X)[0]
        
    else:
        prediction1 = ""
        
    return render_template('classify.html', output = prediction1)

if __name__ == '__main__':
    app.run(debug = False)
    
