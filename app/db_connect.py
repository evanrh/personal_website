from mysql.connector import Error
import mysql.connector as ms

class DB_Connection():
    def __init__(self, host, name, user, pwd):
        try:
            self.conn = ms.connect(host = host, 
                                   database = name,
                                   user = user,
                                   password = pwd)
        except Error as e:
            raise Error(e)

    def check_username(self, username):
        """ check_username = True iff username not in DB """
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username=\"{}\"".format(username))
        rows = cursor.rowcount
        cursor.close()
        return rows == 0

    def check_invite_code(self, invite_code):
        """ check_invite_code = True iff invite_code exists and does not have associated user """
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT invite_code, username FROM users WHERE invite_code=\"{}\""
                        .format(invite_code))
        row = cursor.fetchone()
        cursor.close()
        print(row)
        if row:
            return row[0] == invite_code and row[1] == ''
        else:
            return False

    def __del__(self):
        self.conn.close()
