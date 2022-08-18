import os
import re
import pandas as pd
import sqlite3
import json
from passlib.hash import pbkdf2_sha256

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
        user_id = self.get_user(username)['user_id']
        friends = json.dumps({"username":username, "friends":[]})
        self.execute('INSERT INTO friends (USER_ID, FRIENDS) VALUES (?, ?)', [user_id, friends])
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

    def get_friends(self, username):        
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
    
        data = self.select('SELECT * FROM friends WHERE USER_ID=?', [user_id])
        if data:
            d = data[0]
            return d # It's a tuple
        else:
            return None
                

    def add_friend(self, username, friend):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        friends = self.get_friends(username) # Receives a tuple
        # Get json of the string
        friends_list = json.loads(friends[1])
        friends_list['friends'].append(friend)
        self.execute('UPDATE friends SET FRIENDS=? WHERE USER_ID=?', [json.dumps(friends_list), user_id])

    def remove_friend(self, username, friend):
        user = self.get_user(username)
        if user:
            user_id = user['user_id']
        else:
            return None
        friends = self.get_friends(username)
        friends_list = json.loads(friends[1])
        friends_list['friends'].remove(friend)
        self.execute('UPDATE friends SET FRIENDS=? WHERE USER_ID=?', [json.dumps(friends_list), user_id])

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    import random
    random.seed(2022)
    d = Database()
    for i in range(0, 20):
        passwd = pbkdf2_sha256.hash(f"a{i}", rounds=200000, salt_size=16)
        d.create_user(f"a{i}", f"FIRST{i}", f"LAST{i}", passwd)
        d.create_trans(f"a{i}", "grocery", "2022-08-01", float(random.randint(1,20) * 10), "Truffle Mushrooms")
        d.create_trans(f"a{i}", "grocery", "2022-08-10", float(random.randint(1,20) * 10), "Bananas")
        d.create_trans(f"a{i}", "grocery", "2022-08-12", float(random.randint(1,20) * 10), "Tomatoes")
        d.create_trans(f"a{i}", "entertainment", "2022-08-13", float(random.randint(1,20) * 10), "Karaoke")
        d.create_trans(f"a{i}", "shopping", "2022-08-23", float(random.randint(1,20) * 10), "Clothes")
        d.create_trans(f"a{i}", "Traveling", "2022-08-25", float(random.randint(1,20) * 10), "Europe")
        d.create_trans(f"a{i}", "foodanddining", "2022-08-11", float(random.randint(1,20) * 10), "Urban Eatery")
        d.create_trans(f"a{i}", "billsandutilities", "2022-08-12", float(random.randint(1,20) * 10), "Rent")
        d.create_trans(f"a{i}", "foodanddining", "2022-08-12", float(random.randint(1,20) * 10), "Urban Eatery")
        d.create_trans(f"a{i}", "grocery", "2022-08-24", float(random.randint(1,20) * 10), "Truffle Mushrooms")
        d.create_trans(f"a{i}", "grocery", "2022-08-17", float(random.randint(1,20) * 10), "Bananas")
        d.create_trans(f"a{i}", "foodanddining", "2022-08-15", float(random.randint(1,20) * 10), "Hans")
        d.create_trans(f"a{i}", "grocery", "2022-08-06", float(random.randint(1,20) * 10), "Truffle Mushrooms")
    # Testing user:
    passwd = pbkdf2_sha256.hash("testing", rounds=200000, salt_size=16)
    d.create_user("testing", "testing", "testing", passwd)
    d.create_trans("testing", "grocery", "2022-08-01", 30.0, "Truffle Mushrooms")
    d.create_trans("testing", "grocery", "2022-08-10", 10.0, "Bananas")
    d.create_trans("testing", "grocery", "2022-08-12", 20.0, "Tomatoes")
    d.create_trans("testing", "entertainment", "2022-08-13", 70.0, "Karaoke")
    d.create_trans("testing", "shopping", "2022-08-23", 70.0, "Clothes")
    d.create_trans("testing", "Traveling", "2022-08-25", 300.0, "Europe")
    d.create_trans("testing", "foodanddining", "2022-08-11", 20.0, "Urban Eatery")
    d.create_trans("testing", "billsandutilities", "2022-08-12", 700.0, "Rent")
    d.create_trans("testing", "foodanddining", "2022-08-12", 20.0, "Urban Eatery")
    d.create_trans("testing", "grocery", "2022-08-24", 30.0, "Truffle Mushrooms")
    d.create_trans("testing", "grocery", "2022-08-17", 15.0, "Bananas")
    d.create_trans("testing", "foodanddining", "2022-08-15", 30.0, "Hans")
    d.create_trans("testing", "grocery", "2022-08-06", 20.0, "Truffle Mushrooms")

    for i in range(0,20):
        d.add_friend("testing", f"a{i}")
