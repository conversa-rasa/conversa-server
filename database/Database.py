import sqlite3


class Database:

    def __init__(self, database_path):
        self.database_path = database_path
        print(self.database_path)
        try:
            print
            self.connection = sqlite3.connect(
                database_path, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except Exception as error:
            print(error)

    def init_database(self, password):
        try:
            self.cursor.execute(
                'CREATE TABLE IF NOT EXISTS conversa_data ("password" VARCHAR(45) NULL)')

            self.cursor.execute('INSERT INTO conversa_data (password) VALUES (:password)', {
                "password": password})
            self.connection.commit()

            return True
        except:
            return False

    def get_all_conversation_sessions(self):
        try:
            self.cursor.execute(
                'SELECT sender_id, timestamp FROM events GROUP BY sender_id ORDER BY timestamp DESC')
            return self.cursor.fetchall()
        except:
            return False

    def get_conversation(self, conversation_id):
        self.cursor.execute('SELECT data, timestamp FROM events WHERE sender_id = :id ORDER BY timestamp ASC', {
            "id": conversation_id})
        return self.cursor.fetchall()

    def login(self, password):
        self.cursor.execute('SELECT password FROM conversa_data WHERE password = :password', {
            "password": password})
        return self.cursor.fetchall()
