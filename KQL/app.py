import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from operation import Operation
from ddl_operation import DdlOperation
from dml_operation import DmlOperation

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    folders_to_skip = {'venv', '__pycache__', 'static', 'templates', 'database','.git'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]
    return render_template('index.html', databases=available_databases)

@app.route('/query', methods=['POST'])
def handle_query():
    database = request.form['database']
    folders_to_skip = {'venv', '__pycache__', 'static', 'templates', 'database','.git'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]
    
    if database not in available_databases:
        os.mkdir(database)
    
    txt = request.form['query']
    query = txt.split()
    op = Operation(query)
    operation_name, operation_index, operation_type = op.first_query()
    
    if operation_type == 'ddl':
        ddl = DdlOperation(query, operation_index, database)
        response = ddl.perform_operation()
    elif operation_type == 'dml':
        dml = DmlOperation(query, operation_index, database)
        response = dml.perform_operation()
    else:
        response = "Enter a valid operation"

    # Convert response data into a structured format for HTML rendering
    headers = response[0]
    rows = response[1:]


    # Flash message
    flash("Query executed successfully")

    if "successfully" in response:
        return render_template('index.html', databases=available_databases, response=response)
    else:
        return render_template('index.html', databases=available_databases, headers=headers, rows=rows)



@app.route('/get_databases', methods=['GET'])
def get_databases():
    folders_to_skip = {'venv', '__pycache__', 'static', 'templates', 'database'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]
    return jsonify(available_databases)

if __name__ == '__main__':
    app.run(debug=True)
