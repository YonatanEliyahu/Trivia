import sqlite3


def create_question_table():
    conn = sqlite3.connect('trivia_DB.db')
    cursor = conn.cursor()

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
    questions_dict = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }
    for q_num, q_data in questions_dict.items():
        cursor.execute(
            'INSERT INTO questions (id, question,answer1,answer2,answer3,answer4,currectAnswer) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)', (
            q_num, q_data["question"], q_data["answers"][0], q_data["answers"][1], q_data["answers"][2],
            q_data["answers"][3], q_data["correct"]))

    # Commit and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_question_table()
