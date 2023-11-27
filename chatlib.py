# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_data_req": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SEND_ANSWER",
    "my_score_req": "MY_SCORE",
    "highscore_req": "HIGHSCORE"
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_data_msg": "LOGGED_ANSWER",
    "send_question_msg": "YOUR_QUESTION",
    "correct_ans_msg": "CORRECT_ANSWER",
    "wrong_ans_msg": "WRONG_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "highscore_msg": "ALL_SCORE",
    "error_msg": "ERROR",
    "no_qest_msg": "NO_QUESTIONS"
}

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if cmd is None:
        return ERROR_RETURN
    if len(cmd) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
        return ERROR_RETURN
    cmd_with_padding = cmd + (16 - len(cmd)) * ' '
    data_size = f"{len(data):04d}"
    full_msg = f"{cmd_with_padding}|{data_size}|{data}"
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    data_lst = data.split(DELIMITER)
    if len(data_lst) != 3:
        return ERROR_RETURN, ERROR_RETURN
    try:
        # Attempt to convert data_lst[1] to int
        msg_size = int(data_lst[1])
    except:
        return ERROR_RETURN, ERROR_RETURN
    if msg_size != len(data_lst[2]):
        return ERROR_RETURN, ERROR_RETURN
    return data_lst[0].strip(), data_lst[2]


def split_data(msg, expected_delimiters):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    res = msg.split(DATA_DELIMITER)
    if len(res) != expected_delimiters + 1:
        return [ERROR_RETURN]
    return res


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(msg_fields)
