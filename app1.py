from flask import Flask, render_template, request
import mysql.connector

app1 = Flask(__name__)

# Connect to MySQL Database
# REFERENCE (Python/MySQL/INSERT): https://www.w3schools.com/python/python_mysql_insert.asp
# REFERENCE (Python/MySQL/SELECT): https://www.w3schools.com/python/python_mysql_select.asp
database_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="test_db",
    port="3305",
    auth_plugin='mysql_native_password'
)
cursor = database_connection.cursor()

class Row:
    def __init__(self, id_column, value_column):
        self.id_column = id_column
        self.value_column = value_column

@app1.route('/')
def form():
    return render_template('form.html')

@app1.route('/submission', methods=['GET', 'POST'])
def submission():
    # Get Data from HTTP-POST Request
    id_column = request.form.get("id_column")
    value_column = request.form.get("value_column")

    # Convert id_column From String to Integer
    id_column = int(id_column)
    
    # Insert Data Into MySQL Database
    sql = "INSERT INTO test_table (id_column, value_column) VALUES (%s, %s)"
    values = (id_column, value_column)
    cursor.execute(sql, values)
    database_connection.commit()

    # Render HTML
    return render_template('submission.html', id_column=id_column, value_column=value_column)

@app1.route('/select')
def select():
    # Query MySQL Database
    sql = "SELECT id_column, value_column FROM test_table"
    cursor.execute(sql)
    result = cursor.fetchall()

    # Create an Empty List Which Will Store All of our Rows of Results
    list_of_results = []

    # Loop Through All Rows Returned By the Database Query 
    # And Add Each Row To Our list_of_results
    for row in result:
        newRow = Row(row[0], row[1])
        list_of_results.append(newRow)
    
    # Render HTML
    return render_template('select.html', list_of_results=list_of_results)
if __name__ == '__main__':
    app1.debug = True
    app1.run(host='localhost', port=5000)    