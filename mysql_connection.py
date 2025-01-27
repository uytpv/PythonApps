import mysql.connector

class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute(self, query, values=None):
        if self.connection is None:
            self.connect()

        if values is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, values)

        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_all(self, query, values=None):
        if self.connection is None:
            self.connect()

        if values is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def fetch_one(self, query, values=None):
        if self.connection is None:
            self.connect()

        if values is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, values)

        return self.cursor.fetchone()

    def update(self, query, values=None):
        return self.execute(query, values)

    def delete(self, query, values=None):
        return self.execute(query, values)

    def insert(self, query, values=None):
        return self.execute(query, values)
