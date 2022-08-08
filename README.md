# BudgetManger

#### BudgetManager is a web app that allows users to keep track of their activities and expenses. Many users especially students can benefit a lot from this as they need to manage their expenses. BudgetManager will also provide a social interacting element as well by connecting different users to each other based on categories/activities that they often choose.

# Tools and Software used:
  - ## Flask with python
  - ## HTML and CSS for frontend design
  - ## Chart.js for creating charts and visualizations for users to view their expenses.
  - ## Sqlite3 for relational tables/database to store data.

## Make sure to have flask and sqlite installed in your machine.

## To successfully run project:
- ### Step 1: clone repo

- ### Step 2: within terminal: in directory of project, create a virtual environment
  - in python:  python3.8 -m venv env
  - then activate it with the following command: source env/bin/activate
  - to deactivate, type in the follwoign command: deactivate

- ### Step 3: Once you do the above, run the following commands to have the web app running
  - (table already exist) this first step is to be done initially to create a new table: python init_db.py
  - export FLASK_APP=myapp
  - export export FLASK_ENV=development

- ### Step 4: When done step 3
  -  copy the URL and paste it into a browswer of your choosing
