import os
import csv

class DmlOperation:
    def __init__(self, query, operation_index, database):
        self.query = query
        self.operation_index = operation_index
        self.database = database

    def extract_att(self):
        att_name = []
        for index, value in enumerate(self.query):
            if value.upper() in {'SELECT', 'INSERT', 'UPDATE', 'DELETE'}:
                continue
            elif value == ',':
                continue
            elif value.upper() == "FROM":
                break
            else:
                att_name.append(value)
        return att_name

    def select_operation(self):
        table_name = os.path.join(self.database, self.query[-1] + '.csv')

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))

        if self.query[1] == '*':
            for row in content:
                print(row)
        else:
            extracted_attribute = self.extract_att()
            header = content[0]
            indices = [header.index(attr) for attr in extracted_attribute]

            for row in content[1:]:
                print([row[index] for index in indices])
        print("Select operation completed successfully")

    def insert_operation(self):
        def inserting_data(insert_tbl_name, insert_tbl_data, query, database):
            table_name = os.path.join(database, query[2] + '.csv')

            def chunk_data(data, chunk_size):
                for i in range(0, len(data), len(chunk_size)):
                    yield data[i:i + len(chunk_size)]

            with open(table_name, 'a', newline='') as file:
                writer = csv.writer(file)
                for chunk in chunk_data(insert_tbl_data, insert_tbl_name):
                    writer.writerow(chunk)
            print("Data inserted successfully")

        table_name = self.query[3]
        insert_tbl_name = []
        insert_tbl_data = []
        if self.query[3] == '(':
            current_query = 0
            for i in range(4, len(self.query)):
                if self.query[i] == ')':
                    current_query = i
                    break
                elif self.query[i] == ',':
                    continue
                else:
                    insert_tbl_name.append(self.query[i])
            next_query = current_query + 3
            for i in range(next_query, len(self.query)):
                if self.query[i] == ')':
                    break
                elif self.query[i] == ',':
                    continue
                else:
                    insert_tbl_data.append(self.query[i])
            inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.database)

        elif self.query[3] == 'VALUES':
            insert_tbl_name = ['*']
            for i in range(5, len(self.query)):
                if self.query[i] == ')':
                    break
                elif self.query[i] == ',':
                    continue
                else:
                    insert_tbl_data.append(self.query[i])
            inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.database)

    def update_operation(self):
        table_name = os.path.join(self.database, self.query[1] + '.csv')
        column_to_update = self.query[3]
        new_value = self.query[5]
        condition_column = self.query[7]
        condition_value = self.query[9]

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))

        header = content[0]
        column_index = header.index(column_to_update)
        condition_index = header.index(condition_column)

        for row in content[1:]:
            if row[condition_index] == condition_value:
                row[column_index] = new_value

        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(content)
        print("Update operation completed successfully")

    def delete_operation(self):
        table_name = os.path.join(self.database, self.query[2] + '.csv')
        condition_column = self.query[4]
        condition_value = self.query[6]

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))

        header = content[0]
        condition_index = header.index(condition_column)

        updated_content = [header] + [row for row in content[1:] if row[condition_index] != condition_value]

        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_content)
        print("Delete operation completed successfully")

    def perform_operation(self):
        if self.operation_index == 5:
            self.select_operation()
        elif self.operation_index == 6:
            self.insert_operation()
        elif self.operation_index == 7:
            self.update_operation()
        elif self.operation_index == 8:
            self.delete_operation()
