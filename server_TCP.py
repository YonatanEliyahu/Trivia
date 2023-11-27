import socket
import chatlib
from chatlib import MSG_MAX_SIZE as MSG_MAX_SIZE

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn: socket, code: str, data: str):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    """
    formated_msg = chatlib.build_message(code, data)
    conn.send(formated_msg.encode())
    print(f"[SERVER] {formated_msg}")


def recv_message_and_parse(conn: socket) -> (str, str):
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    try:
        full_msg = conn.recv(MSG_MAX_SIZE)
        cmd, data = chatlib.parse_message(full_msg.decode())
        print(f"[CLIENT] {full_msg}")
        return cmd, data
    except:
        return None, None


# Data Loaders #

def load_questions() -> dict:
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Returns: questions dictionary
    """
    questions_dict = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }
    return questions_dict


def load_user_database() -> dict:
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Returns: user dictionary
    """
    users_dict = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users_dict


# SOCKET CREATOR

def setup_socket() -> socket:
    """
    Creates new listening socket and returns it
    Returns: the socket object
    """
    print("Starting up server ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print("Server is up and listening ...")

    return sock


def send_error(conn: socket, error_msg: str):
    """
    Send error message with given message
    Receives: socket, message error string from called function
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


# MESSAGE HANDLING


def handle_getscore_message(conn, username =""):
    global users
    if username!="": #get my score
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], users[username]["score"])
    else: #get highscore table
        scores = '\n'.join(
            [f'\t{user}: {data["score"]}' for user, data in users.items()])  # creates a formatted str of the score table
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["highscore_msg"], scores)




def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users


# Implement code ...


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later


# Implement code ...


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later


# Implement code ...


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")


# Implement code ...


if __name__ == '__main__':
    main()
