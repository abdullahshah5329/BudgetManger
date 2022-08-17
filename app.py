from flask import Flask, request, redirect, g, render_template, session
from db import Database
import sqlite3 as sql
from passlib.hash import pbkdf2_sha256
import pandas as pd
import json 


app = Flask(__name__, )

# Secret Key for session
app.secret_key = b'CS375@SUMMER@ABDULLAH&HAJUN!'

# db:
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Maybe make a general home page
@app.route('/')
def index():
    try:
        user = session['user']
        return render_template("landing.html")
    except:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if username and passwd:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(passwd, user['passwd']):
                    session['user'] = user
                    return redirect('/')
            else:
                message = "Incorrect username or password"
    return render_template("login.html", message=message)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first']
        last_name = request.form['last']
        passwd = request.form['passwd']
        conf_passwd = request.form['confirm_pass']
        if passwd != conf_passwd:
            message = "Please confirm your password again"
        # check if username already exists:
        else:
            user = get_db().get_user(username)
            if user:
                message = "User already exists"
            else:
                encrypted_pass = pbkdf2_sha256.encrypt(passwd, rounds=200000, salt_size=16)
                get_db().create_user(username, first_name, last_name, encrypted_pass)
                return redirect('/login')
    return render_template('/create_account.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/enternew')
def new_expense_activity():
    return render_template("activity_form.html", msg=None)

@app.route('/expenses')
def list():
    con = sql.connect("budgetmanager.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from expense_activity where user_id=?", [session['user']['user_id']])
    rows = cur.fetchall()
    activityList = ['billsandutilities', 'entertainment', 'foodanddining', 'gasandfuel', 'grocery', 'shopping', 'traveling']
    
    try:
        df = get_db().get_trans(session['user']['username'])
        print(df)
        date = df['CREATED_AT'].values.tolist() # x axis
        data1 = df['EXPENSE'].values.tolist()
        expenseInfo = df['ACTIVITY'].values.tolist()
        expenseInfo1 = df['EXPENSE'].values.tolist()

        dff = df.groupby(["ACTIVITY"]).EXPENSE.sum().reset_index()
        listExpense = dff["EXPENSE"].values.tolist()

        # we need to make sure all values for each activity is included inside the listExpense list,
        # if it isn't, then the pie chart won't work.
        # we need to find a way where we can place 0 or -1 as a place holder
        counter = 0
        for i in activityList:
            counter += 1
            if i not in dff.values:
                listExpense.insert(counter-1, 0)
                #counter += 1
                print(counter)
            else:
                print("good to go")

        dfTimeSeries = df.groupby(["CREATED_AT"]).EXPENSE.sum().reset_index() #grouped dates
        dfTimeSeriesExpense = dfTimeSeries['EXPENSE'].values.tolist()
        dateNew = dfTimeSeries['CREATED_AT'].values.tolist() # x axis new
        # print(dfTimeSeries)
        # print(dateNew)
        # print(dfTimeSeriesExpense)
        # print(listExpense)

            # deal with pie chart having some missing activities
        
        print(dff)
        return render_template('/expenses.html', rows=rows,dateNew=dateNew, dfTimeSeriesExpense=dfTimeSeriesExpense, expenseInfo=expenseInfo, listExpense=listExpense)
    except: # No data was fetched
        return render_template("activity_form.html", msg = "No data was found. Please create new data.")

@app.route('/social')
def social():
    friends = get_db().get_friends(session['user']['username']) # Returns a tuple (user_id, dictionary)
    friends_dict = json.loads(friends[1])
    friends_list = friends_dict["friends"]
    if len(friends_list) == 0:
        friends_name_list = None
    else:
        friends_name_list = [get_db().get_user(user) for user in friends_list]
    print(friends_name_list)
    return render_template('/social.html', friends = friends_name_list)


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        activity = request.form['activity']
        expense = request.form['expense']
        created_at = request.form['created_at']
        comment = request.form['comment']
        username = session['user']['username']
        get_db().create_trans(username, activity, created_at, expense, comment)
    return redirect('/expenses')
            


## Add the generic function here

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port=8080, debug=True)
