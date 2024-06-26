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

# Operations:  extracts query and selecti dml or ddl operation
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
        result_dict = {}

        first_index = self.query[3]
        last_index = self.query[len(self.query)-1]

        for i in range(4,len(self.query)-1,3):
            if i + 1 < len(self.query):
                result_dict[self.query[i]] = self.query[i+1]

        table_mata_data = str(self.DATABASE)+'/'+table_name+'.txt'        
        with open(str(table_mata_data), mode='w') as file:
            for key,value in result_dict.items():
                file.writelines(str(key+' '+value))
                file.writelines("\n")



        for i in range(4, len(self.query) - 1, 3):
            if i + 1 < len(self.query):
                result_dict[self.query[i]] = self.query[i + 1]

        # Ensure the database directory exists
        if not os.path.exists(self.DATABASE):
            os.makedirs(self.DATABASE)

        table_metadata_path = os.path.join(self.DATABASE, table_name + '.csv')
        with open(table_metadata_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            
            # Write the column names in the first row
            writer.writerow(result_dict.keys())
            
            # Write the column types in the second row
            writer.writerow(result_dict.values())

    def alter_operation(self):
        oprt = self.query[0]
        tbl = self.query[1]
        table_name = self.query[2]
        action = self.query[3]
        table_metadata_path = os.path.join(self.DATABASE, table_name + '.csv')

        # Ensure the database directory exists
        if not os.path.exists(self.DATABASE):
            os.makedirs(self.DATABASE)

        # Adding a new column
        if action == "ADD":
            nm = self.query[4]
            dt = self.query[5]

            # Read existing content
            with open(table_metadata_path, 'r') as file:
                reader = csv.reader(file, delimiter=' ')
                content = list(reader)

            # Add new column
            content[0].append(nm)
            content[1].append(dt)

            # Write updated content
            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                writer.writerows(content)

        # Modify an existing column's attribute in a table
        elif action == 'MODIFY':
            nm = self.query[4]
            dt = self.query[5]

            # Read existing content
            with open(table_metadata_path, 'r') as file:
                reader = csv.reader(file, delimiter=' ')
                content = list(reader)

            # Modify column type
            if nm in content[0]:
                index = content[0].index(nm)
                content[1][index] = dt

            # Write updated content
            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                writer.writerows(content)

        # Rename a column in a table
        elif action == 'RENAME' and self.query[4] == 'COLUMN':
            nm = self.query[5]
            nm2 = self.query[7]

            # Read existing content
            with open(table_metadata_path, 'r') as file:
                reader = csv.reader(file, delimiter=' ')
                content = list(reader)

            # Rename column
            if nm in content[0]:
                index = content[0].index(nm)
                content[0][index] = nm2

            # Write updated content
            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                writer.writerows(content)

        # Rename a table
        elif action == "RENAME" and self.query[4] == 'TO':
            nm = self.query[3]
            nm2 = self.query[5]
            new_table_metadata_path = os.path.join(self.DATABASE, nm2 + '.csv')
            os.rename(table_metadata_path, new_table_metadata_path)

    def drop_operation(self):
        
        self.DATABASE = 'emp'
        oprt = self.query[0]
        tbl = self.query[1]
        table_name = self.query[2]

        if tbl.lower() == 'table':
            table_metadata_path = os.path.join(self.DATABASE, table_name + '.csv')
            print(table_metadata_path)
            if os.path.exists(table_metadata_path):
                os.remove(table_metadata_path)
            else:
                print(f"Table {table_name} does not exist.")

        elif tbl.lower() == 'database':
            try:
                database_metadata_path = self.DATABASE
                if os.path.exists(database_metadata_path):
                    os.rmdir(database_metadata_path)
                else:
                    print(f"Database {self.DATABASE} does not exist.")
            except OSError as e:
                print(f"Error: {e}")

    def truncate_operation(self):

        self.DATABASE = 'emp'
        oprt = self.query[0]
        tbl = self.query[1]
        table_name = self.query[2]
        table_name = self.DATABASE + '/' + table_name + '.csv'
        print(table_name)
        with open((table_name), 'w') as file:
            file.write("")

    def perform_operation(self):

        if self.operation_index == 1:
            self.create_operation()
        elif self.operation_index == 2:
            self.alter_operation()
        elif self.operation_index == 3:
            self.drop_operation()
        elif self.operation_index == 4:
            self.truncate_operation()

class Dml_Operation():
    def __init__(self,query,operation_index,database):
        self.query = query
        self.operation_index = operation_index
        self.DATABASE = database

#this only extract attributes for select
    def extract_att(self):
        att_name = []

        for index, value in enumerate(self.query):

            if self.query[index] == 'SELECT' or self.query[index] == 'select' or self.query[
                index] == 'INSERT' or self.query[index] == 'insert' or self.query[index] == 'UPDATE' or \
                    self.query[index] == 'update' or self.query[index] == 'DELETE' or self.query[index] == 'delete':
                continue
            elif self.query[index] == ',':
                continue
            elif self.query[index] == "FROM" or self.query[index] == "from":
                break
            else:
                att_name.append(self.query[index])
        return att_name



    def select_operation(self):
        table_name = os.path.join(self.DATABASE, self.query[-1] + '.csv')

        with open(table_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            content = list(reader)

        if self.query[1] == '*':
            for row in content:
                print(row)
        else:
            extracted_attribute = self.extract_att()

            # Get the header row to determine column indices
            header = content[0]
            col_indices = [header.index(attr) for attr in extracted_attribute if attr in header]

            if not col_indices:
                print(f"None of the attributes {extracted_attribute} found in the table.")
                return

            # Print the selected columns for each row
            for row in content:
                selected_cols = [row[index] for index in col_indices]
                print(selected_cols)

 
    def insert_operation(self):
        
        def inserting_data(insert_tbl_name, insert_tbl_data, query, database):
            table_query = query
            DATABASE = database
            table_name = os.path.join(DATABASE, table_query[2] + '.csv')

            # Read the existing content to get the header
            with open(table_name, 'r', newline='') as file:
                reader = csv.reader(file)
                content = list(reader)
                header = content[0]

            # Map the provided data to the correct columns
            if insert_tbl_name != ['*']:
                column_indices = [header.index(col) for col in insert_tbl_name]
            else:
                column_indices = range(len(header))

            # Generate rows to insert
            def chunk_data(data, chunk_size):
                chunk_size = len(chunk_size)
                for i in range(0, len(data), chunk_size):
                    yield data[i:i + chunk_size]

            # Open the file in append mode
            with open(table_name, 'a', newline='') as file:
                writer = csv.writer(file)
                # Split the data into chunks and write each chunk as a row
                for chunk in chunk_data(insert_tbl_data, column_indices):
                    row = [''] * len(header)
                    for i, index in enumerate(column_indices):
                        row[index] = chunk[i]
                    writer.writerow(row)

        def insert_att_extract(self):
            table_name = self.query[3]
            insert_tbl_name = []
            insert_tbl_data = []
            if self.query[3] == '(':
                current_query = 0
            
                # Extract the column names
                for i in range(4, len(self.query)):
                    if self.query[i] == ')':
                        current_query = i
                        break
                    elif self.query[i] == ',':
                        continue
                    else:
                        insert_tbl_name.append(self.query[i])
                next_query = current_query + 3 
                
                # Extract the values
                for i in range(next_query, len(self.query)):
                    if self.query[i] == ')':
                        current_query = i
                        break
                    elif self.query[i] == ',':
                        continue
                    else:
                        insert_tbl_data.append(self.query[i])

                inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.DATABASE)

            elif self.query[3] == 'VALUES':
                insert_tbl_name = ['*']
                for i in range(5, len(self.query)):
                    if self.query[i] == ')':
                        break
                    elif self.query[i] == ',':
                        continue
                    else:
                        insert_tbl_data.append(self.query[i])

                inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.DATABASE)

        insert_att_extract(self)


    def update_operation(self):
        table_name = os.path.join(self.DATABASE, self.query[1] + '.csv')
        set_index = self.query.index('SET')
        where_index = self.query.index('WHERE') if 'WHERE' in self.query else len(self.query)

        # Extract columns to update and their new values
        update_cols = []
        update_values = []
        for i in range(set_index + 1, where_index, 3):
            update_cols.append(self.query[i])
            update_values.append(self.query[i + 2])

        # Extract the conditions
        conditions = {}
        if where_index < len(self.query):
            for i in range(where_index + 1, len(self.query), 3):
                conditions[self.query[i]] = self.query[i + 2]

        with open(table_name, 'r', newline='') as file:
            reader = csv.reader(file)
            content = list(reader)
            header = content[0]

        # Update the rows based on conditions
        for row in content[1:]:
            if all(row[header.index(col)] == val for col, val in conditions.items()):
                for col, val in zip(update_cols, update_values):
                    row[header.index(col)] = val

        # Write the updated content back to the CSV
        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([header] + content[1:])


    def delete_operation(self):
        table_name = os.path.join(self.DATABASE, self.query[2] + '.csv')
        where_index = self.query.index('WHERE') if 'WHERE' in self.query else len(self.query)

        # Extract the conditions
        conditions = {}
        if where_index < len(self.query):
            for i in range(where_index + 1, len(self.query), 3):
                conditions[self.query[i]] = self.query[i + 2]

        with open(table_name, 'r', newline='') as file:
            reader = csv.reader(file)
            content = list(reader)
            header = content[0]

        # Filter out the rows that meet the conditions
        new_content = [content[0]]  # include header
        for row in content[1:]:
            if not all(row[header.index(col)] == val for col, val in conditions.items()):
                new_content.append(row)

        # Write the filtered content back to the CSV
        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_content)

        




    def perform_operation(self):
        attribute_names = self.extract_att()
        
        if operation_index == 5:
            self.select_operation()
        elif operation_index == 6:
            self.insert_operation()
        elif operation_index == 7:
            self.update_operation()
        elif operation_index == 8:
            self.delete_operation()

 

#DATABASE = select_database()
DATABASE = "emp"




txt = "DELETE FROM table_name WHERE col3 = 1 "
query = txt.split()



op = Operation(query)

operation_name, operation_index ,operation_type = op.first_query()
table_name = op.last_query()

#print(f"\n operation = {operation_name} \n column names = {operation_type} \n table name = {table_name}")


if operation_type == 'ddl':
    ddl = Ddl_Operation(query,operation_index,DATABASE)
    ddl.perform_operation()
elif operation_type == 'dml':
    dml = Dml_Operation(query,operation_index,DATABASE)
    dml.perform_operation()
else:
    print("enter valid operation")