import os
from flask import Flask, render_template, request, redirect, url_for
from operation import Operation
from ddl_operation import DdlOperation
from dml_operation import DmlOperation

app = Flask(__name__)

# Your existing database code for selecting or creating databases can be integrated here
# Example:
@app.route('/')
def index():
    
    folders_to_skip = {'venv','__pycache__','static','templates','database'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]

    return render_template('index.html', database=available_databases)

# Implement routes and functions for handling various SQL operations
# Example:
@app.route('/query', methods=['POST'])
def handle_query():
    database = request.form['database']
    folders_to_skip = {'venv','__pycache__','static','templates','database'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]
    if database in available_databases:
        databse = database
    else:
        os.mkdir(database)
        
    txt = request.form['query']
    query = txt.split()

    op = Operation(query)
    operation_name, operation_index, operation_type = op.first_query()
    table_name = op.last_query()

    if operation_type == 'ddl':
        ddl = DdlOperation(query, operation_index, database)
        ddl.perform_operation()
    elif operation_type == 'dml':
        dml = DmlOperation(query, operation_index, database)
        dml.perform_operation()
    else:
        return "Enter a valid operation"

    return redirect(url_for('index'))  # Redirect back to the main page after operation

if __name__ == '__main__':
    app.run(debug=True)
