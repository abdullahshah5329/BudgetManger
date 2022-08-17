-- user
CREATE TABLE IF NOT EXISTS users (
   USER_ID integer NOT NULL CONSTRAINT USER_ID PRIMARY KEY,
   USERNAME text NOT NULL,
   FIRST_NAME text NOT NULL,
   LAST_NAME text NOT NULL,
   PASSWD text NOT NULL,
   UNIQUE(USERNAME, PASSWD)
);

-- spending
CREATE TABLE IF NOT EXISTS expense_activity (
   EXPENSE_ID integer NOT NULL CONSTRAINT EXPENSE_ID PRIMARY KEY,
   USER_ID integer NOT NULL,
   ACTIVITY text NOT NULL,
   CREATED_AT text NOT NULL,
   EXPENSE double NOT NULL,
   COMMENT text NOT NULL,
   FOREIGN KEY(USER_ID) REFERENCES users(USER_ID)
);

-- social
CREATE TABLE IF NOT EXISTS friends (
    USER_ID integer NOT NULL CONSTRAINT USER_ID PRIMARY KEY,
    FRIENDS text,
    FOREIGN KEY(USER_ID) REFERENCES users(USER_ID)
);

-- EXAMPLES:
-- users data
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("a544", "Ali", "Tattar", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("b544", "Ben", "Tattar", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("c544", "Anna", "Tattar", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("d544", "Adam", "Thomas", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("e544", "Eve", "Thomas", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("f544", "Zen", "Thomas", "##########");
INSERT INTO users (USERNAME, FIRST_NAME, LAST_NAME, PASSWD) VALUES ("g544", "Hugo", "Thomas", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("h544", "Victor", "Thomas", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("i544", "Connor", "Thomas", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("j544", "James", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("k544", "John", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("l544", "Jamie", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("m544", "Jayci", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("n544", "Yucca", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("o544", "Skinny", "Jimmy", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("p544", "Brown", "June", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("q544", "Tommy", "June", "##########");
INSERT INTO users (username, first_name, last_name, passwd) VALUES ("r544", "Heather", "June", "##########");
