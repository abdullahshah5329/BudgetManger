from flask import Flask, render_template, request, flash, redirect, render_template_string, url_for, session
import sqlite3 as sql
import pandas as pd
import uuid
from wtforms import Form, StringField, TextAreaField, DateField, DecimalField, PasswordField, validators


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_expense_activity():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from expense_activity")
    df = pd.read_sql_query("select * from expense_activity", con)

    rows = cur.fetchall(); 

    date = df['created_at'].values.tolist() # x axis
    data1 = df['expense'].values.tolist()
    return render_template("activity_form.html", rows = rows, date=date, data1=data1)


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            activity_id = str(uuid.uuid4())
            activity = request.form['activity']
            expense = request.form['expense']
            created_at = request.form['created_at']
            comment = request.form['comment']
           
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO expense_activity (activity_id, activity, expense, created_at, comment) VALUES (?,?,?,?,?)",(activity_id, activity, expense, created_at, comment) )
                
                con.commit()
                msg = "Record successfully added"
      
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("result.html", msg = msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from expense_activity")
    df = pd.read_sql_query("select * from expense_activity", con)

    rows = cur.fetchall(); 


    activityList = ['billsandutilities', 'entertainment', 'foodanddining', 'gasandfuel', 'grocery', 'shopping', 'traveling']

    date = df['created_at'].values.tolist() # x axis
    data1 = df['expense'].values.tolist()
    expenseInfo = df['activity'].values.tolist()
    expenseInfo1 = df['expense'].values.tolist()

    dff = df.groupby(["activity"]).expense.sum().reset_index()
    listExpense = dff["expense"].values.tolist()

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

    dfTimeSeries = df.groupby(["created_at"]).expense.sum().reset_index() #grouped dates
    dfTimeSeriesExpense = dfTimeSeries['expense'].values.tolist()
    dateNew = dfTimeSeries['created_at'].values.tolist() # x axis new
   # print(dfTimeSeries)
   # print(dateNew)
   # print(dfTimeSeriesExpense)
   # print(listExpense)

    # deal with pie chart having some missing activities
    
    print(dff)
  
    return render_template("list.html", rows = rows, dateNew=dateNew, dfTimeSeriesExpense=dfTimeSeriesExpense, expenseInfo=expenseInfo, listExpense=listExpense)


@app.route('/edit_activity/<string:activity_id>',methods = ['POST', 'GET'])
def edit_activity(activity_id):
    conn = sql.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        activity_id = str(activity_id)
        activity = request.form['activity']
        expense = request.form['expense']
        created_at = request.form['created_at']
        comment = request.form['comment']
    
        cur.execute("UPDATE expense_activity SET activity = ?, expense = ?, created_at = ?, comment = ? WHERE activity_id = ?",
                    (activity, expense, created_at, comment, activity_id))
        conn.commit()
       
    item = cur.fetchone()
    
    conn.close()
    test = fully_edit_activity(activity_id)

    #return render_template("edit.html", item=item)
    return render_template('edit_activity.html', item=item, activity_id=activity_id, test=test)

@app.route('/fully_edit_activity/<activity_id>',methods = ['POST', 'GET'])
def fully_edit_activity(activity_id):
    if request.method == 'POST':
        try:
            activity_id = activity_id
            activity = request.form['activity']
            expense = request.form['expense']
            created_at = request.form['created_at']
            comment = request.form['comment']
           
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE expense_activity SET activity = ?, expense = ?, created_at = ?, comment = ? WHERE activity_id = ?",
                    (activity, expense, created_at, comment, activity_id))
                con.commit()
                msg = "Record successfully added"
      
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("result.html", msg = msg, activity_id = activity_id)
            con.close()


@app.route('/delete/<activity_id>', methods = ['POST'])
#@is_logged_in
def delete_record(activity_id):

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('delete from expense_activity where activity_id = ?', [activity_id])
        #con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur1 = con.cursor()
        cur1.execute("select * from expense_activity")
        df = pd.read_sql_query("select * from expense_activity", con)

        rows = cur1.fetchall(); 
        
        date = df['created_at'].values.tolist() # x axis
        data1 = df['expense'].values.tolist()
        con.commit()
    return render_template("activity_form.html", rows = rows, date=date, data1=data1)



if __name__ == '__main__':
    app.run(debug = True)
