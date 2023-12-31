import socket
import threading
import logging
import API_handler
import trivia_DB
from models.User_model import User
from models.Question_model import Question
from chatlib_files import chatlib
from chatlib_files.chatlib import MSG_MAX_SIZE
from random import shuffle as shuffle
from trivia_DB import load_question_table_from_db
from trivia_DB import load_user_data_from_db
from trivia_DB import update_user_data_in_db
from trivia_DB import create_user_data_in_db

# GLOBALS
users: [str, User] = {}  # maps username to a user object
questions: [int, Question] = {}  # maps question_id to Question object
logged_users: [int, str] = {}  # a dictionary of client file descriptor to usernames
connections: [int, socket] = {}  # list of connected client file descriptor to socket object

threads = []  # list of running client threads

allowed_login_chars = set(chr(i) for i in range(ord('a'), ord('z') + 1)).union(
    set(chr(i) for i in range(ord('A'), ord('Z') + 1))).union(
    {'!', '@', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'})  # set of allowed chars in username and password

# Set up logging to a file
logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] - %(message)s')

# Define a global flag to signal server shutdown
shutdown_server = False

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# SOCKET CREATOR
def setup_socket() -> socket:
    """
    Creates new listening socket and returns it
    loads the users from database
    Returns: the socket object
    """
    logging.info("Starting up server ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create new tcp socket
    sock.bind((SERVER_IP, SERVER_PORT))  # bind the socket to known port and ip add.
    sock.listen()  # set the server to listen mode
    logging.info("Server is up and listening ...")

    return sock


# HELPER SOCKET METHODS
def build_and_send_message(conn: socket, code: str, data: str = ""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    """
    formatted_msg = chatlib.build_message(code, data)  # build formated srting
    conn.send(formatted_msg.encode())  # send message to client
    logging.info(f"[SERVER] {formatted_msg}")


def recv_message_and_parse(conn: socket) -> (str, str):
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    try:
        full_msg = conn.recv(MSG_MAX_SIZE)  # recv message from client
        cmd, data = chatlib.parse_message(full_msg.decode())
        if conn.fileno() not in logged_users.keys():
            logging.info(f"[CLIENT] {full_msg}")
        else:
            logging.info(f"[{logged_users[conn.fileno()].upper()}] {full_msg}")
        return cmd, data
    except:
        return None, None


# Data Loader

def load_databases():
    """
    Load users,question dictionaries from database for the server functionality.
    """
    global users
    global questions
    users = load_user_data_from_db()
    questions = load_question_table_from_db()


# QUESTION HANDLING

def get_random_question(conn: socket) -> (int, str, int):
    """
    Gets socket connection and returns a random available question
    returns random question number
    if no question available for the current user, will return 0

    """
    global questions
    global logged_users
    global users
    this_username = logged_users[conn.fileno()]
    # get all the questions that the user wasn't asked before
    optional_questions = [(key, value) for key, value in questions.items()
                          if key not in users[this_username].get_questions_asked()]
    if len(optional_questions) == 0:  # no question available at this moment to this user
        return 0, None, 0
    shuffle(optional_questions)
    question_num, question_data = optional_questions[0]
    return question_num


def handle_question_message(conn: socket):
    """
    Gets socket connection and checks if the user has unanswered questions,
        -if there are unanswered questions, the user gets a question and waiting for the user response,
            after the response the server will check the correctness of the answer and will send feedback.

        - it there isn't unanswered question, the servers sends chatlib.PROTOCOL_SERVER["no_quest_msg"] to the user.

    the function returns an indicator of success or failure
    """

    global users
    global logged_users

    this_username = logged_users[conn.fileno()]
    question_num = get_random_question(conn)
    if question_num == 0:
        # no question is available
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["no_quest_msg"])
        return
    try:
        formatted_question = questions[question_num].chatlib_supporting_str(question_num)
        correct_ans = questions[question_num].get_correct_ans()

        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["send_question_msg"], formatted_question)  # send question
        users[this_username].ask_question(question_num)  # add question to user list
        cmd, data = recv_message_and_parse(conn)  # recv answer from user
        if cmd != chatlib.PROTOCOL_CLIENT["send_answer_msg"]:
            raise ConnectionError
        data = int(data)  # may raise TypeError
        if data == correct_ans:
            users[this_username].update_score()  # add five points to the user
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_ans_msg"])
        else:  # wrong answer
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_ans_msg"], str(correct_ans))
        return

    # both exceptions will be handled in the calling function
    except (ConnectionError, TypeError):
        raise


# MESSAGE HANDLING

def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    """
    global users
    global logged_users
    user_info = chatlib.split_data(data, 1)
    if user_info[0] == chatlib.ERROR_RETURN:
        send_error(conn, "username or password are incorrect")
        return
    if len(user_info[0]) == 0 or len(user_info[1]) == 0:
        send_error(conn, "username or password are missing")
        return
    elif user_info[0] in users.keys():
        if user_info[0] in logged_users.values():
            send_error(conn)  # user already connected
            return

        if users[user_info[0]].check_password(user_info[1]):
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"])
            logged_users[conn.fileno()] = user_info[0]
            logging.info(f"{user_info[0]} logged in successfully..")
            return  # logged in successfully
    # failed to log in
    send_error(conn, "username or password are incorrect")


def handle_signup_message(conn, data):
    """
    Gets socket and message data of signup message. Checks if user is available.
    If not - sends error and finished. If all ok, sends OK message and adds user to users list and DB
    Recieves: socket, message code and data
    """
    global users
    user_info = chatlib.split_data(data, 1)
    if user_info[0] == chatlib.ERROR_RETURN:
        send_error(conn, "username or password are incorrect")
        return
    if len(user_info[0]) < 6 or len(user_info[0]) > 15 or len(user_info[1]) < 6 or len(user_info[1]) > 15:
        send_error(conn, "username or password are too short/long")
        return
    for c in str(user_info[0]) + str(user_info[1]):
        if c not in allowed_login_chars:
            send_error(conn, f"username or password are incorrect - {c}")
            return
    if user_info[0] in users.keys():
        send_error(conn, "username already exists")
        return
    users[user_info[0]] = User(user_info[0], user_info[1])
    logging.info(f"{user_info[0]} signed up successfully..")
    try:
        create_user_data_in_db(user_info[0], user_info[1])
    except:  # DB failure
        del users[user_info[0]]
        send_error(conn, f"username or password are incorrect")
        return

    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["signup_ok_msg"])


def handle_logout_message(conn: socket):
    """
    Closes the given socket, and if there is a logged user related to this connection,
     it will handle his logout and will update his data in the DB
    """
    global logged_users
    # Check if the user is logged in before attempting to delete
    if conn.fileno() in logged_users:
        logging.info(f"logging [{logged_users[conn.fileno()].upper()}] out at {conn.getpeername()}...")

        user = users[logged_users[conn.fileno()]]
        update_user_data_in_db(user)
        del logged_users[conn.fileno()]

    else:
        logging.info(f"closing connection at {conn.getpeername()}...")

    del connections[conn.fileno()]
    conn.close()


def handle_logged_users_message(conn: socket):
    """
    sends a list of all the logged-in users
    """
    global logged_users
    users_str = ','.join([f'{user}' for user in logged_users.values()])

    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_data_msg"], users_str)


def handle_getscore_message(conn: socket, req_type: int = 0):
    """
    Handles the client's request for score-related information.
    0 for getting the current user's score, 1 for requesting the highscore table.

    Example:
    - For getting the current user's score:
      handle_getscore_message(conn, req_type=0)

    - For requesting the highscore table:
      handle_getscore_message(conn, req_type=1)
    """
    global users
    global logged_users
    if req_type == 0:  # get my score
        this_username = logged_users[conn.fileno()]
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"],
                               str(users[this_username].get_score()))
    else:  # get highscore table
        scores = '\n'.join(
            [f'\t{user.get_username()}: {user.get_score()}' for user in
             sorted(users.values(), key=lambda user: user.get_score(), reverse=True)])
        # creates a formatted str of the score table DESC order
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["highscore_msg"], scores)


def send_error(conn: socket, error_msg: str = ERROR_MSG):
    """
    Send error message with given message
    Receives: socket, message error string from called function
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)
    logging.error(error_msg)


def handle_client_message(conn: socket, cmd: str, data: str):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    """
    global logged_users
    if cmd is None and data is None:
        send_error(conn)
        handle_logout_message(conn)
        raise ConnectionResetError

    elif cmd == chatlib.PROTOCOL_CLIENT["signup_msg"]:
        handle_signup_message(conn, data)

    elif cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)

    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)

    elif cmd == chatlib.PROTOCOL_CLIENT["my_score_req"]:
        handle_getscore_message(conn)

    elif cmd == chatlib.PROTOCOL_CLIENT["highscore_req"]:
        handle_getscore_message(conn, 1)

    elif cmd == chatlib.PROTOCOL_CLIENT["logged_data_req"]:
        handle_logged_users_message(conn)

    elif cmd == chatlib.PROTOCOL_CLIENT["get_question_msg"]:
        try:
            handle_question_message(conn)
        except TypeError:
            send_error(conn)
        except ConnectionError:
            send_error(conn)
            handle_logout_message(conn)
            raise ConnectionResetError


def handle_client(client_socket):
    """
    Handles communication with a connected client.
    Continuously receives and processes messages from the client using the 'recv_message_and_parse' function.
    Calls 'handle_client_message' to process the received command and data.

    Exceptions:
    - Catches socket errors and ConnectionResetError to handle client disconnection.
    - Prints a message when a client disconnects and breaks out of the loop.
    """
    while True:
        try:
            cmd, data = recv_message_and_parse(client_socket)
            handle_client_message(client_socket, cmd, data)
        except (socket.error, ConnectionResetError):
            logging.error("Client disconnected")
            break


def kick_user_by_pick():
    """
    Kicks a user out of the server based on user input.

    - Prints a list of currently logged-in users.
    - Asks the server manager to pick a user to kick.
    - Sends a logout message to the selected user's socket.
    """
    logging.info("Performing server management task: Kicking user...")
    if len(logged_users) == 0:
        print("No clients to kick")
        return
    users_str = '\n'.join([f'{i}. {user}' for i, user in enumerate(logged_users.values(), start=1)])
    pick = input(f"Please pick a user to kick: \n{users_str}\n")
    if pick == None:
        print("Error")
        return
    if pick not in logged_users.values():
        print(f"No such user named {pick}")
        return
    # send message to client
    for key in logged_users.keys():
        if pick == logged_users[key]:
            handle_logout_message(connections[key])
            logging.info(f"[SERVER] kicked {pick} out of the server")
            return


def kick_all_users():
    """
    Kicks all currently logged-in users out of the server.

    - Retrieves a list of sockets of logged-in users.
    - Sends a logout message to each logged-in user's socket.
    """
    logged_users_socket_lst = list(connections.values())

    for sock in logged_users_socket_lst:
        handle_logout_message(sock)


def load_more_questions():
    """
    Loads more questions from an API and adds them to the trivia database.

    - Retrieves the current highest question ID.
    - Calls 'API_handler.load_question_with_api' to get new questions.
    - Filters out questions that are already in the database.
    - Adds the new questions to the trivia database.
    """
    global questions
    logging.info(f"[SERVER] loading data from API to DB\n")
    start = max(questions.keys()) + 1
    new_questions = API_handler.load_question_with_api(start)
    # This line checks if the content of each question (value) in new_questions is not present in the values of the questions dictionary.
    # The all function is used to check this condition for all questions in questions.values()'
    new_questions = {key: value for key, value in new_questions.items() if all(value != q for q in questions.values())}
    trivia_DB.add_questions_to_DB(new_questions)
    questions = load_question_table_from_db()


def handle_server_shutdown():
    """
    Initiates the server shutdown process.

    - Sets the 'shutdown_server' flag to True.
    - Kicks all currently logged-in users out of the server.
    - Logs the server shutdown event.
    """
    global shutdown_server
    print("Shutting down the server...")
    shutdown_server = True
    kick_all_users()
    logging.info(f"[SERVER] SHUTDOWN\n")


def handle_server_manager_commands(server_conn: socket):
    """
    Functionality to handle server management commands.
    This function runs in a separate thread.

    Raises:
    - SystemExit: Raised to close the current thread.
    """
    global threads
    while True:
        # Your logic to handle server management commands
        command = input("Enter server management command (load, kick, shutdown): ")
        if command == "load":
            load_more_questions()
        elif command == "kick":
            kick_user_by_pick()
        elif command == "shutdown":
            handle_server_shutdown()
            server_conn.close()
            for t in threads:
                t.join()
            raise SystemExit  # close current thread
        else:
            print("Unknown command. Try again.")


def main():
    """
    The main function to start the Trivia Server.

    - Prints a welcome message.
    - Sets up the server socket using 'setup_socket'.
    - Loads databases using 'load_databases'.
    - Spawns two threads:
      - 'manager_commands_thread' for handling server management commands using 'handle_server_manager_commands'.
      - 'client_handler_thread' to handle each connected client using 'handle_client'.
    - Waits for both threads to finish before cleaning up resources and closing the server.

    Global Variables:
    - connections: A dictionary to store client connections.
    - threads: A list to store active threads.
    - shutdown_server: A flag to signal the server shutdown.

    Raises:
    - Exception: Handles various exceptions that may occur during server operation.
    """
    global connections
    global threads
    print("Welcome to Trivia Server!")
    server_socket = setup_socket()
    load_databases()
    manager_commands_thread = threading.Thread(target=handle_server_manager_commands, args=(server_socket,))
    manager_commands_thread.start()

    while not shutdown_server:
        try:
            client_socket, client_address = server_socket.accept()
            connections[client_socket.fileno()] = client_socket
            logging.info("Client connected")

            client_handler_thread = threading.Thread(target=handle_client, args=(client_socket,))
            threads.append(client_handler_thread)
            client_handler_thread.start()
        except:
            print(f"server is down")


if __name__ == '__main__':
    main()
