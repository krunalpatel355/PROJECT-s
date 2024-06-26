class Operation:
    def __init__(self, query):
        self.query = query

    def first_query(self):
        if self.query[0].upper() == "CREATE":
            return self.query[0], 1, 'ddl'
        elif self.query[0].upper() == "ALTER":
            return self.query[0], 2, 'ddl'
        elif self.query[0].upper() == "DROP":
            return self.query[0], 3, 'ddl'
        elif self.query[0].upper() == "TRUNCATE":
            return self.query[0], 4, 'ddl'
        elif self.query[0].upper() == "SELECT":
            return self.query[0], 5, 'dml'
        elif self.query[0].upper() == "INSERT":
            return self.query[0], 6, 'dml'
        elif self.query[0].upper() == "UPDATE":
            return self.query[0], 7, 'dml'
        elif self.query[0].upper() == "DELETE":
            return self.query[0], 8, 'dml'

    def last_query(self):
        table_name = self.query[-1]
        return table_name
