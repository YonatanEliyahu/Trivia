import sqlite3
from API_handler import load_question_with_api
from models.User_model import User
from models.Question_model import Question

DB_NAME = 'trivia_DB.db'

users_dict = {"test": User("test", "test", 0), "Yonatan": User("Yonatan", "Eliyahu", 100)}


def connect_to_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor


def close_db_connection(conn):
    conn.commit()
    conn.close()


def create_question_table():
    """
    Creates a table named 'questions' in the database to store question data.
    """
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
        for q_num, question in questions_api_dict.items():
            answers = question.get_answers()
            cursor.execute(
                'INSERT INTO questions (id, question,answer1,answer2,answer3,answer4,currectAnswer) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    q_num, question.get_question(), answers[0], answers[1], answers[2],
                    answers[3], question.get_correct_ans()))
    except:
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def load_question_table_from_db():
    """
    Loads a table named 'questions' from the database and store the questions in a dict[int:Question].
    """
    conn, cursor = connect_to_db()

    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()

    questions_dict = {}
    for q in questions:
        questions_dict[q[0]] = Question(question=q[1], answers=[q[2], q[3], q[4], q[5]], correct=q[6])

    # Commit and close the connection
    close_db_connection(conn)
    return questions_dict


def create_users_table():
    """
    Creates a table named 'users_data' in the database to store users data.
    """
    conn, cursor = connect_to_db()
    # Create a table to store your data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_data (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    try:
        for user in users_dict.values():
            try:
                cursor.execute(
                    'INSERT INTO users_data (username, password, score) '
                    'VALUES (?, ?, ?)', (user.get_username(), user.get_password(), user.get_score()))
            except sqlite3.IntegrityError:  # user is already in the table, try next user
                pass
    except Exception as e:
        # Handle other exceptions if needed
        print(f"An error occurred: {e}")
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def create_user_question_relation_table():
    """
    Creates a table named 'user_question_relation' in the database to store users asked questions(one to many relation).
    """
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

    try:
        for user in users_dict.values():
            for questions_id in user.get_questions_asked():
                try:
                    cursor.execute(
                        'INSERT INTO user_question_relation (username, question_id) '
                        'VALUES (?, ?)', (user.get_username(), questions_id))
                except sqlite3.IntegrityError:  # data is already in the table, try next line
                    pass
    except Exception as e:
        # Handle other exceptions if needed
        print(f"An error occurred: {e}")
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def add_questions_to_DB(questions_dict: dict):
    """
    Adds a new questions (dict[int:Question]) to table 'questions' in the database.
    question must be checked in advanced that any of them doesn't appear in the table.
    """
    conn, cursor = connect_to_db()
    try:
        for q_num, question in questions_dict.items():
            answers = question.get_answers()
            cursor.execute(
                'INSERT INTO questions (id, question,answer1,answer2,answer3,answer4,currectAnswer) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    q_num, question.get_question(), answers[0], answers[1], answers[2],
                    answers[3], question.get_correct_ans()))
    except:
        pass
    finally:
        # Commit and close the connection
        close_db_connection(conn)


def load_user_data_from_db():
    """
    Loads a table named 'users_data' from the database and store the users in a dict[str:User].
    """
    conn, cursor = connect_to_db()

    cursor.execute('SELECT * FROM users_data')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM user_question_relation')
    user_questionID = cursor.fetchall()

    users_res_dict = {}
    for user_info in users:
        new_user = User(user_info[0], user_info[1], user_info[2])
        users_res_dict[user_info[0]] = new_user
    for row in user_questionID:
        users_res_dict[row[0]].ask_question(row[1])

    # Commit and close the connection
    close_db_connection(conn)
    return users_res_dict


def create_user_data_in_db(username: str, password: str):
    """
    Adds a new user to table 'users_data' in the database.
    user must be checked in advanced that he isn't in the database.
    """
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


def update_user_data_in_db(user: User):
    """
    Updates user in 'users_data' table in the database.
    user must be checked in advanced that he is in the database.
    """
    conn, cursor = connect_to_db()
    try:
        cursor.execute('''
            UPDATE users_data
            SET score = ?
            WHERE username = ?
        ''', (user.get_score(), user.get_username()))
    except sqlite3.IntegrityError:
        # Handle the case where user doesn't exist
        return

    for question_id in user.get_questions_asked():
        try:
            cursor.execute(
                'INSERT INTO user_question_relation (username, question_id) '
                'VALUES (?, ?)', (user.get_username(), question_id))
        except sqlite3.IntegrityError:
            # Handle the case where the relation already exists
            pass

    # Commit and close the connection
    close_db_connection(conn)


if __name__ == "__main__":
    create_question_table()
    create_users_table()
    create_user_question_relation_table()
