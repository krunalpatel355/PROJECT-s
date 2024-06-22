import os







def first_query(main_query):
    FIRST = 0
    if main_query[FIRST] == "CREATE":
        return main_query[FIRST], 1
    elif main_query[FIRST] == "ALTER":
        return main_query[FIRST], 2
    elif main_query[FIRST] == "DROP":
        return main_query[FIRST], 3
    elif main_query[FIRST] == "TRUNCATE":
        return main_query[FIRST], 4


def last_query(main_query):
    LAST = len(main_query) - 1
    table_name = main_query[LAST]
    return table_name


def attribute_name(attribute_names):
    att_name = []

    for index, value in enumerate(attribute_names):

        if attribute_names[index] == 'CREATE' or attribute_names[index] == 'create' or attribute_names[
            index] == 'ALTER' or attribute_names[index] == 'alter' or attribute_names[index] == 'DROP' or \
                attribute_names[index] == 'drop' or attribute_names[index] == 'TRUNCATE' or attribute_names[index] == 'truncate':
            continue
        elif attribute_names[index] == ',':
            continue
        elif attribute_names[index] == "FROM" or attribute_names[index] == "from":
            break
        else:
            att_name.append(attribute_names[index])
    return att_name


def select_operation(table_name,attribute_names):
    pass
    
def insert_operation(table_name,attribute_names):
    pass

def update_operation(table_name,attribute_names):
    pass

def delete_operation(table_name,attribute_names):
    pass

def perform_operation(operation_index,table_name,attribute_names):
    
    if operation_index == 1:
        select_operation(table_name,attribute_names)
    elif operation_index == 2:
        insert_operation(table_name,attribute_names)
    elif operation_index == 3:
        update_operation(table_name,attribute_names)
    elif operation_index == 4:
        delete_operation(table_name,attribute_names)













def first_query(main_query):
    FIRST = 0
    if main_query[FIRST] == "SELECT":
        return main_query[FIRST], 1
    elif main_query[FIRST] == "INSERT":
        return main_query[FIRST], 2
    elif main_query[FIRST] == "UPDATE":
        return main_query[FIRST], 3
    elif main_query[FIRST] == "DELETE":
        return main_query[FIRST], 4


def last_query(main_query):
    LAST = len(main_query) - 1
    table_name = main_query[LAST]
    return table_name


def attribute_name(attribute_names):
    att_name = []

    for index, value in enumerate(attribute_names):

        if attribute_names[index] == 'SELECT' or attribute_names[index] == 'select' or attribute_names[
            index] == 'UPDATE' or attribute_names[index] == 'update' or attribute_names[index] == 'INSERT' or \
                attribute_names[index] == 'insert' or attribute_names[index] == 'DELETE' or attribute_names[index] == 'delete':
            continue
        elif attribute_names[index] == ',':
            continue
        elif attribute_names[index] == "FROM" or attribute_names[index] == "from":
            break
        else:
            att_name.append(attribute_names[index])
    return att_name


def select_operation(table_name,attribute_names):
    pass
    
def insert_operation(table_name,attribute_names):
    pass

def update_operation(table_name,attribute_names):
    pass

def delete_operation(table_name,attribute_names):
    pass

def perform_operation(operation_index,table_name,attribute_names):
    
    if operation_index == 1:
        select_operation(table_name,attribute_names)
    elif operation_index == 2:
        insert_operation(table_name,attribute_names)
    elif operation_index == 3:
        update_operation(table_name,attribute_names)
    elif operation_index == 4:
        delete_operation(table_name,attribute_names)










def main():

    LOOP = True

    directories = [d for d in os.listdir('.') if os.path.isdir(d)]
    print(directories)
    DATABASE = input("select or create new dic if not exist ::")

    if DATABASE in directories:
        DATABASE = DATABASE
    else:
        os.mkdir(DATABASE)

    while LOOP:

        txt = "SELECT hello , welcome FROM emp"
        query = txt.split()


        operation_name, operation_index = first_query(query)
        table_name = last_query(query)
        attribute_names = attribute_name(query)
        print(f"\n operation = {operation_name} \n column names = {attribute_names} \n table name = {table_name}")

        print("\n performing operation...",)
        perform_operation(operation_index,table_name,attribute_names)



        LOOP = False


main()
