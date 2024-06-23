import os
import csv

def select_database():
    folders_to_skip = {'venv'}
    AVALIABLE_DATABASES = [d for d in os.listdir('.') if os.path.isdir(d) and d not in folders_to_skip ]
    print("current databases : ",AVALIABLE_DATABASES)


    DATABASE = input("select or create new dic if not exist ::")
    if DATABASE in AVALIABLE_DATABASES:
        return DATABASE 
    else:
        os.mkdir(DATABASE)
        return DATABASE

class Operation:

    def __init__(self,query):
        self.query = query

    def first_query(self):
        print(self.query)
        FIRST = 0
        if self.query[FIRST] == "CREATE":
            return self.query[FIRST], 1 , 'ddl'
        elif self.query[FIRST] == "ALTER":
            return self.query[FIRST], 2 , 'ddl'
        elif self.query[FIRST] == "DROP":
            return self.query[FIRST], 3 , 'ddl'
        elif self.query[FIRST] == "TRUNCATE":
            return self.query[FIRST], 4 , 'ddl'
        elif self.query[FIRST] == "SELECT":
            return self.query[FIRST], 5 , 'dml'
        elif self.query[FIRST] == "INSERT":
            return self.query[FIRST], 6 , 'dml'
        elif self.query[FIRST] == "UPDATE":
            return self.query[FIRST], 7 , 'dml'
        elif self.query[FIRST] == "DELETE":
            return self.query[FIRST], 8 , 'dml'


    def last_query(self):
        LAST = len(self.query) - 1
        table_name = self.query[LAST]
        return table_name


class Ddl_Operation():
    def __init__(self,query,operation_index,database):
        self.query = query
        self.operation_index = operation_index
        self.DATABASE = database

    def create_operation(self):
        
        self.DATABASE = 'emp'
        oprt = self.query[0]
        tbl = self.query[1]
        table_name = self.query[2]

        first_index = self.query[3]
        last_index = self.query[len(self.query)-1]

        result_dict = {}

        for i in range(4,len(self.query)-1,3):
            if i + 1 < len(self.query):
                result_dict[self.query[i]] = self.query[i+1]

        table_mata_data = str(self.DATABASE)+'/'+table_name+'.txt'        
        with open(str(table_mata_data), mode='w') as file:
            for key,value in result_dict.items():
                file.writelines(str(key+' '+value))
                file.writelines("\n")

    def alter_operation(self):
        
        self.DATABASE = 'emp'
        oprt = self.query[0]
        tbl = self.query[1]
        table_name = self.query[2]

        action = self.query[3]

        #adding a new column
        if action == 'ADD':
            nm =  self.query[4]
            dt = self.query[5]

            table_mata_data = str(DATABASE)+'/'+table_name+'.txt'        
            with open(str(table_mata_data), mode='a') as file:
                file.writelines(str(nm+' '+dt))
        elif action = 'MODIFY':
                      







    def perform_operation(self):

        if self.operation_index == 1:
            self.create_operation()
        elif self.operation_index == 2:
            self.alter_operation()
        elif self.operation_index == 3:
            self.drop_operation()
        elif self.operation_index == 4:
            self.truncate_operation()




DATABASE = select_database()

txt = "ALTER TABLE table_name ADD col4 varchar"
query = txt.split()


op = Operation(query)

operation_name, operation_index ,operation_type = op.first_query()
table_name = op.last_query()

print(f"\n operation = {operation_name} \n column names = {operation_type} \n table name = {table_name}")




if operation_type == 'ddl':
    ddl = Ddl_Operation(query,operation_index,DATABASE)
    ddl.perform_operation()
elif operation_type == 'dml':
    dml = Dml_Operation()
else:
    print("enter valid operation")