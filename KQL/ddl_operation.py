import os
import csv

class DdlOperation:
    def __init__(self, query, operation_index, database):
        self.query = query
        self.operation_index = operation_index
        self.database = database

    def create_operation(self):
        table_name = self.query[2]
        result_dict = {}

        for i in range(4, len(self.query) - 1, 3):
            if i + 1 < len(self.query):
                result_dict[self.query[i]] = self.query[i + 1]

        table_metadata_path = os.path.join(self.database, table_name + '.csv')
        with open(table_metadata_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(result_dict.keys())
            writer.writerow(result_dict.values())
        return "Table created successfully"

    def alter_operation(self):
        action = self.query[3]
        table_name = self.query[2]
        table_metadata_path = os.path.join(self.database, table_name + '.csv')

        if action == "ADD":
            nm = self.query[4]
            dt = self.query[5]

            with open(table_metadata_path, 'r') as file:
                content = list(csv.reader(file))

            content[0].append(nm)
            content[1].append(dt)

            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)
            return "Column added successfully"

        elif action == 'MODIFY':
            nm = self.query[4]
            dt = self.query[5]

            with open(table_metadata_path, 'r') as file:
                content = list(csv.reader(file))

            if nm in content[0]:
                index = content[0].index(nm)
                content[1][index] = dt

            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)
            return "Column modified successfully"

        elif action == 'RENAME' and self.query[4] == 'COLUMN':
            nm = self.query[5]
            nm2 = self.query[7]

            with open(table_metadata_path, 'r') as file:
                content = list(csv.reader(file))

            if nm in content[0]:
                index = content[0].index(nm)
                content[0][index] = nm2

            with open(table_metadata_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)
            return "Column renamed successfully"

        elif action == "RENAME" and self.query[4] == 'TO':
            nm2 = self.query[5]
            new_table_metadata_path = os.path.join(self.database, nm2 + '.csv')
            os.rename(table_metadata_path, new_table_metadata_path)
            return "Table renamed successfully"

    def drop_operation(self):
        table_name = self.query[2]
        if self.query[1].lower() == 'table':
            table_metadata_path = os.path.join(self.database, table_name + '.csv')
            if os.path.exists(table_metadata_path):
                os.remove(table_metadata_path)
                return "Table dropped successfully"
            else:
                return f"Table {table_name} does not exist."
        elif self.query[1].lower() == 'database':
            database_metadata_path = self.database
            if os.path.exists(database_metadata_path):
                os.rmdir(database_metadata_path)
                return "Database dropped successfully"
            else:
                return f"Database {self.database} does not exist."

    def truncate_operation(self):
        table_name = os.path.join(self.database, self.query[2] + '.csv')
        with open(table_name, 'w') as file:
            file.write("")
        return "Table truncated successfully"

    def perform_operation(self):
        if self.operation_index == 1:
            return self.create_operation()
        elif self.operation_index == 2:
            return self.alter_operation()
        elif self.operation_index == 3:
            return self.drop_operation()
        elif self.operation_index == 4:
            return self.truncate_operation()
