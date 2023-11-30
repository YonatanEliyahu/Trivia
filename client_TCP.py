import socket
from chatlib_files import chatlib
from chatlib_files.chatlib import MSG_MAX_SIZE

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


OPTIONS = {'s': "get my score",
           'h': "get highscore table",
           'l': "get logged users list",
           'p': "take a trivia question",
           'q': "Quit"}


# HELPER SOCKET METHODS

def build_and_send_message(conn: socket, code: str, data: str=""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    """
    formated_msg = chatlib.build_message(code, data)
    conn.send(formated_msg.encode())
    print(f"[CLIENT] {formated_msg}")


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
        return cmd, data
    except:
        return None, None


def connect() -> socket:
    """
    Creates a socket obj that will use to communicate between two ip address with TCP protocol,
    and connects to the pre-defined SERVER_IP and SERVER_PORT
    """
    print(f"connecting to {SERVER_IP} port {SERVER_PORT}")
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect((SERVER_IP, SERVER_PORT))
    return c_socket


def error_and_exit(conn: socket, error_msg: str = "ERROR"):
    """
    In case of an error, the function will print the error msg,
    and then logout, close the socket and determinate the program.
    """
    print(error_msg.upper())
    try:
        logout(conn)
    finally:
        conn.close()
        exit(1)


def login(conn: socket):
    """
    Receives a username and password,
    then parses the data using chatlib.
    send the data to the server and wait for response.
    """
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = f'{username}{chatlib.DATA_DELIMITER}{password}'
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        cmd, data = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:  # logged in successfully
            print(f"{username} logged in successfully ")
            return
        print(f"{data}\n couldn't log in to {username}, please try again")


def logout(conn: socket):
    """
    logging out the client from the server.
    """
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def build_send_recv_parse(conn: socket, code: str, data: str = "") -> (str, str):
    """
    Parses and send the message using build_and_send_message to a given socket,
    and returns the response of the server to that message.
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
        ^^the returned values description is taken from
          recv_message_and_parse documentation.
    """
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)  # returns cmd, data


def get_score(conn: socket):
    """
    Prints the client score.
    """
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score_req"])
    if code != chatlib.PROTOCOL_SERVER["your_score_msg"]:
        print("getting score failed.")
    else:
        try:
            print(f"SCORE: {int(data)}")
        except:
            print("getting score failed.")


def get_highscore(conn: socket):
    """
    Prints the all client scores.
    """
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore_req"])
    if code != chatlib.PROTOCOL_SERVER["highscore_msg"]:
        print("getting score failed.")
    else:
        print(f"HIGHSCORE TABLE:\n{data}")


def print_question_get_answer(qust: list) -> int:
    """
    Prints the given question.
    Parameters: qust (list object)
    Returns: ans
    """
    while True:
        ans = input(f"Q: {qust[1]}\n"
                    f"\t1. {qust[2]}\n"
                    f"\t2. {qust[3]}\n"
                    f"\t3. {qust[4]}\n"
                    f"\t4. {qust[5]}\n")
        if ans.isdigit() and 1 <= int(ans) <= 4:
            return str(ans)
        else:
            print("Invalid input. Please enter a number between 1 and 4.")


def play_question(conn: socket):
    """
    Question case handler.
    """
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"])
    if code == chatlib.PROTOCOL_SERVER["no_quest_msg"]:
        print("no available question at this moment, do you want to try anything else?")
        return
    elif code != chatlib.PROTOCOL_SERVER["send_question_msg"]:
        print("failed to get a new question from server, please try again")
        return
    else:  # code ==chatlib.PROTOCOL_SERVER["send_question_msg"]
        data = chatlib.split_data(data, 5)
        if data[0] == chatlib.ERROR_RETURN:
            print("failed to get a new question from server, please try again")
            return
    answer = print_question_get_answer(data) # return value between 1 and 4
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer_msg"], str(answer))
    if code == chatlib.PROTOCOL_SERVER["correct_ans_msg"]:
        print("CORRECT!!")
        return
    elif code == chatlib.PROTOCOL_SERVER["wrong_ans_msg"]:
        print(f"WRONG ANSWER! THE CORRECT ANSWER IS {data}")
        return
    # code == chatlib.PROTOCOL_SERVER["error_msg"] or code == None:
    error_and_exit(conn)


def get_logged_users(conn: socket):
    """
    Prints the list of logged users.
    """
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_data_req"])
    if code != chatlib.PROTOCOL_SERVER["logged_data_msg"]:
        print("Failed to get logged users list.")
    else:
        data = data.split(",")
        print("LOGGED USERS:")
        for user in data:
            print(f'\t{user}')


def main():
    conn = connect()
    login(conn)
    options = '\n'.join([f'\t{key} - {value}' for key, value in OPTIONS.items()])  # creates a formatted str of the given options
    while True:
        choice = input(f"Please choose one of the following options:\n{options}\n")
        if len(choice) != 1 or choice not in OPTIONS.keys():
            continue
        elif choice == 's':
            get_score(conn)
        elif choice == 'h':
            get_highscore(conn)
        elif choice =='l':
            get_logged_users(conn)
        elif choice =='p':
            play_question(conn)
        elif choice == 'q':
            break

    logout(conn)
    conn.close()


if __name__ == '__main__':
    main()
