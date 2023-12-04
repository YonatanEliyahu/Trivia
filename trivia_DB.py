import sqlite3
from API_handler import load_question_with_api

DB_NAME = 'trivia_DB.db'

users_dict = {
    "test": {"password": "test", "score": 0, "questions_asked": []},
    "yossi": {"password": "123", "score": 50, "questions_asked": []},
    "master": {"password": "master", "score": 200, "questions_asked": []}
}

# questions_dict = {
#     1: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
#     2: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
#         "correct": 3}
# }


def connect_to_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor


def close_db_connection(conn):
    conn.commit()
    conn.close()


def create_question_table():
    conn, cursor = connect_to_db()
    # Create a table to store your data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer1 TEXT NOT NULL,
            answer2 TEXT NOT NULL,
            answer3 TEXT NOT NULL,
            answer4 TEXT NOT NULL,
            currectAnswer INTEGER NOT NULL
        )
    ''')

    # Insert data into the table
    questions_api_dict = load_question_with_api()
    try:
        for q_num, q_data in questions_api_dict.items():
            cursor.execute(
                'INSERT INTO questions (id, question,answer1,answer2,answer3,answer4,currectAnswer) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    q_num, q_data["question"], q_data["answers"][0], q_data["answers"][1], q_data["answers"][2],
                    q_data["answers"][3], q_data["correct"]))
    except:
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def load_question_table_from_db():
    conn, cursor = connect_to_db()

    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()

    questions_dict = {}
    for q in questions:
        question_data = {"question": q[1],
                         "answers": [q[2], q[3], q[4], q[5]],
                         "correct": q[6]}
        questions_dict[q[0]] = question_data

    # Commit and close the connection
    close_db_connection(conn)
    return questions_dict


def create_users_table():
    conn, cursor = connect_to_db()
    # Create a table to store your data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_data (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    # Insert data into the table
    try:
        for username, user_data in users_dict.items():
            cursor.execute(
                'INSERT INTO users_data (username, password,score) '
                'VALUES (?, ?, ?)', (username, user_data["password"], user_data["score"]))
    except:  # data already in table
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def create_user_question_relation_table():
    conn, cursor = connect_to_db()
    # Create a table to store user-question relations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_question_relation (
            username TEXT,
            question_id INTEGER,
            PRIMARY KEY (username, question_id),
            FOREIGN KEY (username) REFERENCES users_data(username),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # Insert data into the table
    try:
        for username in users_dict.key():
            for questions_id in users_dict[username]["questions_asked"]:
                cursor.execute(
                    'INSERT INTO user_question_relation (username, question_id) '
                    'VALUES (?, ?)', (username, questions_id))
    except:  # data already in table
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)

def add_questions_to_DB(questions_dict : dict):
    conn, cursor = connect_to_db()
    try:
        for q_num, q_data in questions_dict.items():
            cursor.execute(
                'INSERT INTO questions (id, question,answer1,answer2,answer3,answer4,currectAnswer) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    q_num, q_data["question"], q_data["answers"][0], q_data["answers"][1], q_data["answers"][2],
                    q_data["answers"][3], q_data["correct"]))
    except:
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def load_user_data_from_db():
    conn, cursor = connect_to_db()

    cursor.execute('SELECT * FROM users_data')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM user_question_relation')
    user_questionID = cursor.fetchall()

    users_res_dict = {}
    for user in users:
        user_data = {"password": user[1],
                     "score": user[2],
                     "questions_asked": []
                     }
        users_res_dict[user[0]] = user_data
    for row in user_questionID:
        users_res_dict[row[0]]["questions_asked"].append(row[1])

    # Commit and close the connection
    close_db_connection(conn)
    return users_res_dict


def create_user_data_in_db(username: str, password: str):
    conn, cursor = connect_to_db()
    try:
        cursor.execute(
            'INSERT INTO users_data (username, password,score) '
            'VALUES (?, ?, ?)', (username, password, 0))

    except sqlite3.IntegrityError:
        raise sqlite3.IntegrityError
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def update_user_data_in_db(user_data: tuple):
    conn, cursor = connect_to_db()

    cursor.execute('''
        UPDATE users_data
        SET score = ?
        WHERE username = ?
    ''', (user_data[1]['score'], user_data[0]))

    for question_id in user_data[1]["questions_asked"]:
        try:
            cursor.execute(
                'INSERT INTO user_question_relation (username, question_id) '
                'VALUES (?, ?)', (user_data[0], question_id))
        except sqlite3.IntegrityError:
            # Handle the case where the relation already exists
            pass

    # Commit and close the connection
    close_db_connection(conn)


if __name__ == "__main__":
    create_question_table()
    create_users_table()
    create_user_question_relation_table()
