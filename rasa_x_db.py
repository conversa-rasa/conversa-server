import sqlite3

con = sqlite3.connect(
    '/home/joan/Desktop/rasa_db/rasa.db', check_same_thread=False)
cur = con.cursor()


def get_all_conversation_sessions():
    cur.execute(
        'SELECT conversation_session.conversation_id, conversation_session.session_start, conversation.latest_input_channel FROM conversation_session, conversation WHERE conversation_session.conversation_id = conversation.sender_id GROUP BY conversation_session.conversation_id ORDER BY conversation_session.session_start DESC')
    return cur.fetchall()


def get_conversation(conversation_id):
    cur.execute('SELECT data FROM conversation_event WHERE conversation_id = :id ORDER BY timestamp ASC', {
                "id": conversation_id})
    return cur.fetchall()


def login(password):
    cur.execute('SELECT password FROM password WHERE password = :password', {
                "password": password})
    return cur.fetchall()
