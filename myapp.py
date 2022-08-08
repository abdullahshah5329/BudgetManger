from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_expense_activity():
    return render_template("activity_form.html")


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            activity = request.form['activity']
            expense = request.form['expense']
            created_at = request.form['created_at']
            comment = request.form['comment']
           
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO expense_activity (activity, expense, created_at, comment) VALUES (?,?,?,?)",(activity, expense, created_at, comment) )
                
                con.commit()
                msg = "Record successfully added"
      
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("result.html",msg = msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from expense_activity")
    df = pd.read_sql_query("select * from expense_activity", con)

    rows = cur.fetchall(); 

    date = df['created_at'].values.tolist() # x axis
    data1 = df['expense'].values.tolist()
    return render_template("list.html", rows = rows, date=date, data1=data1)

if __name__ == '__main__':
    app.run(debug = True)
