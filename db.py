import os
import re
import sqlite3


database = "budgetmanager.db"
SQLITE_PATH = os.path.join(os.path.dirname(__file__), database)


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    # User auth (Table name : users)
    def create_user(self, username, f_name, l_name, password):
        self.execute('INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES (?, ?, ?, ?)',
                     [username, f_name, l_name, password])
        # Also create connections table
        data = self.get_user(username)
        user_id = data['user_id']
        self.execute('INSERT INTO social (USER_ID, USER_CONNECTION) VALUES (?, ?)', [user_id, ""])
        return

    def get_user(self, username):
        data = self.select('SELECT * FROM users WHERE USERNAME=?', [username])
        if data:
            d = data[0]
            return {
                'user_id': d[0],
                'username': d[1],
                'first_name': d[2],
                'last_name': d[3],
                'passwd' : d[4]
            }
        else:
            return None
    # Expenses (Table name : expense)
    def get_expense_id(self, expense_cat, expense_subcat):
        data = self.select('SELECT * FROM expense WHERE EXPENSE_CAT=? AND EXPENSE_SUBCAT=?', [expense_cat, expense_subcat])
        if data:
            d = data[0]
            return {
                'expense_id': d[0],
                'expense_cat' : d[1],
                'expense_subcat' : d[2]
            }
        else:
            return None
    # Transactions (Table name: spending) 
    def get_trans(self, username, start_date = None, end_date = None):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        
        if start_date and end_date:
            # Need to fix this part so that date and time are matched
            data = self.select('SELECT * FROM spending WHERE USER_ID=? AND DATE_PURCH<=? AND DATE_PURCH >=?', [user_id, start_date, end_date])
        else:
            data = self.select('SELECT * FROM spending WHERE USER_ID=?', [user_id])
        if data:
            return data
        else:
            return None
    
    def create_trans(self, username, expense_cat, expense_subcat, date_purchased, quantity, price, comments):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        expense = self.get_expense_id(expense_cat, expense_subcat)
        if expense:
            expense_id = expense['expense_id']
        else:
            return None
        # user_id and expense_id is not None
        if user_id and expense_id:
            self.execute('INSERT INTO spending (USER_ID, EXPENSE_ID, DATE_PURCH, QUANTITY, PRICE, COMMENTS) VALUES (?, ?, ?, ?, ?, ?)', [user_id, expense_id, date_purchased, quantity, price, comments])
        else:
            return None 

    # Social
    def get_social(self, username):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        data = self.select('SELECT * FROM social WHERE USER_ID=?', [user_id])
        if data:
            return data
            '''return {
                'user_id' : data[0],
                'connection' : data[1]
            }'''
        else:
            return None

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    d = Database()
    #print(d.get_user("a544"))
    #print(d.get_user("f544"))
    #print(d.get_trans("a544"))
    #d.create_trans("a544", "FOOD", "VEGETABLES", "2020-07-01", 1, 200.0, "Truffle Mushrooms")
    #print(d.get_trans("a544"))

    #d.create_user("jz2323", "Jay", "Zebra", "##########")
    print(d.get_social("jz2323"))
