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

    def sum_column(self, data, index):
        return sum(float(row[index]) for row in data if row[index].replace('.', '', 1).isdigit())

    def avg_column(self, data, index):
        valid_data = [float(row[index]) for row in data if row[index].replace('.', '', 1).isdigit()]
        return sum(valid_data) / len(valid_data)

    def count_column(self, data, index):
        return len([row[index] for row in data if row[index]])

    def apply_where_clause(self, data, header):
        if "WHERE" in self.query:
            where_index = self.query.index("WHERE")
            condition = " ".join(self.query[where_index + 1:])
            condition_column, condition_operator, condition_value = self.parse_condition(condition)
            condition_index = header.index(condition_column)
            if condition_operator == '=':
                return [row for row in data if row[condition_index] == condition_value]
            elif condition_operator == '!=':
                return [row for row in data if row[condition_index] != condition_value]
            elif condition_operator == '>':
                return [row for row in data if float(row[condition_index]) > float(condition_value)]
            elif condition_operator == '<':
                return [row for row in data if float(row[condition_index]) < float(condition_value)]
            elif condition_operator == '>=':
                return [row for row in data if float(row[condition_index]) >= float(condition_value)]
            elif condition_operator == '<=':
                return [row for row in data if float(row[condition_index]) <= float(condition_value)]
        return data

    def parse_condition(self, condition):
        for operator in ['=', '!=', '>', '<', '>=', '<=']:
            if operator in condition:
                column, value = condition.split(operator)
                return column.strip(), operator, value.strip()
        return None, None, None

    def extract_table_name(self):
        if "FROM" in self.query:
            from_index = self.query.index("FROM")
            table_name = self.query[from_index + 1]
            return table_name
        else:
            raise ValueError("'FROM' clause is missing in the query")


    def select_operation(self):
        table_name = os.path.join(self.database, self.extract_table_name() + '.csv')

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))
        
        header = content[0]
        data = content[1:]
        data = self.apply_where_clause(data, header)  # Apply WHERE clause filtering

        fetched_result = []

        if self.query[1] == '*':
            fetched_result = [header] + data
        else:
            extracted_attribute = self.extract_att()
            indices = [header.index(attr.split('(')[-1].split(')')[0]) for attr in extracted_attribute]
            agg_functions = [attr.split('(')[0].upper() if '(' in attr else None for attr in extracted_attribute]
            
            result_row = []
            for i, func in enumerate(agg_functions):
                if func == 'SUM':
                    result_row.append(self.sum_column(data, indices[i]))
                elif func == 'AVG':
                    result_row.append(self.avg_column(data, indices[i]))
                elif func == 'COUNT':
                    result_row.append(self.count_column(data, indices[i]))
                else:
                    result_row.append([row[indices[i]] for row in data])
            fetched_result.append(result_row)
        
        return [header] + fetched_result


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
            return "Data inserted successfully"

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
            return inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.database)

        elif self.query[3] == 'VALUES':
            insert_tbl_name = ['*']
            for i in range(5, len(self.query)):
                if self.query[i] == ')':
                    break
                elif self.query[i] == ',':
                    continue
                else:
                    insert_tbl_data.append(self.query[i])
            return inserting_data(insert_tbl_name, insert_tbl_data, self.query, self.database)

    def update_operation(self):
        # Extract the table name
        table_name = os.path.join(self.database, self.query[1] + '.csv')
        
        # Extract the SET clause and the WHERE clause
        set_clause_start = self.query.index("SET") + 1
        where_clause_start = self.query.index("WHERE")
        
        # Extract the columns and values to update
        set_clause = " ".join(self.query[set_clause_start:where_clause_start])
        updates = set_clause.split(",")
        updates = [update.strip().split("=") for update in updates]
        
        # Extract the condition column and value
        condition_clause = " ".join(self.query[where_clause_start + 1:])
        condition_column, condition_value = condition_clause.split("=")
        condition_column = condition_column.strip()
        condition_value = condition_value.strip()

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))

        header = content[0]
        condition_index = header.index(condition_column)

        # Create a dictionary of updates
        updates_dict = {update[0].strip(): update[1].strip() for update in updates}

        # Update the rows based on the condition
        for row in content[1:]:
            if len(row) > condition_index and row[condition_index] == condition_value:
                for column, new_value in updates_dict.items():
                    column_index = header.index(column)
                    if len(row) > column_index:
                        row[column_index] = new_value

        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(content)
        
        return "Update operation completed successfully"

    def delete_operation(self):
        table_name = os.path.join(self.database, self.query[2] + '.csv')
        condition_column = self.query[4]
        condition_value = self.query[6]

        with open(table_name, 'r') as file:
            content = list(csv.reader(file))

        header = content[0]
        condition_index = header.index(condition_column)

        updated_content = [header]
        for row in content[1:]:
            if len(row) > condition_index and row[condition_index] != condition_value:
                updated_content.append(row)

        with open(table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_content)
        return "Delete operation completed successfully"




    def perform_operation(self):
        if self.operation_index == 5:
            return self.select_operation()
        elif self.operation_index == 6:
            return self.insert_operation()
        elif self.operation_index == 7:
            return self.update_operation()
        elif self.operation_index == 8:
            return self.delete_operation()
