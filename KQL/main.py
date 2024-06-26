from operation import Operation
from ddl_operation import DdlOperation
from dml_operation import DmlOperation

def select_database():
    import os
    folders_to_skip = {'venv'}
    available_databases = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip]
    print("current databases:", available_databases)

    database = input("select or create new database if not exist: ")
    if database in available_databases:
        return database
    else:
        os.mkdir(database)
        return database

def main():
    database = select_database()
    txt = input("Enter your query: ")
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
        print("Enter a valid operation")

if __name__ == "__main__":
    main()
