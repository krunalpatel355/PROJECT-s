from flask import Flask, render_template, request, redirect, url_for
from operation import Operation
from ddl_operation import DdlOperation
from dml_operation import DmlOperation

app = Flask(__name__)

# Your existing database code for selecting or creating databases can be integrated here
# Example:
@app.route('/')
def index():
    database = select_database()  # Implement your select_database function here
    return render_template('index.html', database=database)

# Implement routes and functions for handling various SQL operations
# Example:
@app.route('/query', methods=['POST'])
def handle_query():
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
