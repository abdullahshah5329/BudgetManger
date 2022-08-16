import os
import re
import pandas as pd
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
    
    # Transactions (Table name: spending) 
    def get_trans(self, username):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        
        data = self.select('SELECT * FROM expense_activity WHERE USER_ID=?', [user_id])
        if data:
            return pd.read_sql_query(f"select * from expense_activity where user_id={self.get_user(username)['user_id']}", self.conn)
        else:
            return None
    
    def create_trans(self, username, activity, created_at, expense, comments):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        # user_id and expense_id is not None
        if user_id:
            self.execute('INSERT INTO expense_activity (USER_ID, ACTIVITY, CREATED_AT, EXPENSE, COMMENT) VALUES (?, ?, ?, ?, ?)', [user_id, activity, created_at, expense, comments])
        else:
            return None 

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    d = Database()
    print(d.get_user("a544"))
    print(d.get_user("f544"))
    print(d.get_trans("a544"))
    d.create_trans("a544", "FOOD", "2020-07-01", 200.0, "Truffle Mushrooms")
    print(d.get_trans("a544"))
    import pandas as pd
    a = pd.read_sql_query(f"select * from expense_activity where user_id={d.get_user('a544')['user_id']}", d.conn)
    print(a['created_at'])    
#d.create_user("jz2323", "Jay", "Zebra", "##########")
