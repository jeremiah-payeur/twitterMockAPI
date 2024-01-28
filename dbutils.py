import pymysql


class DBUtils:

    def __init__(self, user, password, database, host="localhost"):
        """ Future work: Implement connection pooling """
        self.con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.query = None
        self.cursor = None

    def close(self):
        """ Close or release a connection back to the connection pool """
        self.con.close()
        self.con = None
        if self.cursor is not None:
            self.cursor.close()

    def insert_one(self, query, values):
        """Inserts into database - leveraging prepared statements and not reassigning variables
        values should be a tuple and query should be a prepared statement (str)"""

        if self.query != query:
            self.query = query

            # ensures a duplicate cursor is not created
            if self.cursor is not None:
                self.cursor.close()
            self.cursor = self.con.cursor()

        self.cursor.execute(self.query, values)
        self.con.commit()

    def execute(self, proc, value):
        """"Executes a procedure in the database procedure should be string name and value should be tuple entry"""
        cursor = self.con.cursor()
        cursor.callproc(proc, value)
        all_info = cursor.fetchall()
        cursor.close()
        return all_info

    def execute_query(self, query):
        """Execute a query in sql given by user in a string"""
        cursor = self.con.cursor()
        cursor.execute(query)
        info = cursor.fetchall()
        cursor.close()
        return info
