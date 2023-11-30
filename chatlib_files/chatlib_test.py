import chatlib

TEST_COUNT = 19


class Color:
    FAIL = '\033[91m'
    SUCCESS = '\033[92m'
    REGULAR = '\033[0m'


def check_build(input_cmd, input_data, expected_output):
    print(f"{Color.REGULAR}Input: ", input_cmd, input_data, "\nExpected output: ", expected_output)
    try:
        output = chatlib.build_message(input_cmd, input_data)
    except Exception as e:
        output = "Exception raised: " + str(e)

    if output == expected_output:
        print(f"{Color.SUCCESS}.....\t SUCCESS")
        return 1
    else:
        print(f"{Color.FAIL}.....\t FAILED , output: ", output)
        return 0


def check_parse(msg_str, expected_output):
    print(f"{Color.REGULAR}Input: ", msg_str, "\nExpected output: ", expected_output)

    try:
        output = chatlib.parse_message(msg_str)
    except Exception as e:
        output = "Exception raised: " + str(e)

    if output == expected_output:
        print(f"{Color.SUCCESS}.....\t SUCCESS")
        return 1
    else:
        print(f"{Color.FAIL}.....\t FAILED, output: ", output)
        return 0


def main():
    counter = 0
    # BUILD

    # Valid inputs
    # Normal message
    counter += check_build("LOGIN", "aaaa#bbbb", "LOGIN           |0009|aaaa#bbbb")
    counter += check_build("LOGIN", "aaaabbbb", "LOGIN           |0008|aaaabbbb")
    # Zero-length message
    counter += check_build("LOGIN", "", "LOGIN           |0000|")

    # Invalid inputs
    # cmd too long
    counter += check_build("0123456789ABCDEFG", "", None)
    # msg too long
    counter += check_build("A", "A" * (chatlib.MAX_DATA_LENGTH + 1), None)

    # PARSE

    # Valid inputs
    counter += check_parse("LOGIN           |   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse(" LOGIN          |   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse("           LOGIN|   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse("LOGIN           |9   |aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse("LOGIN           |  09|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse("LOGIN           |0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    counter += check_parse("LOGIN           |9   | aaa#bbbb", ("LOGIN", " aaa#bbbb"))
    counter += check_parse("LOGIN           |   4|data", ("LOGIN", "data"))

    # Invalid inputs
    counter += check_parse("", (None, None))
    counter += check_parse("LOGIN           x	  4|data", (None, None))
    counter += check_parse("LOGIN           |	  4xdata", (None, None))
    counter += check_parse("LOGIN           |	 -4|data", (None, None))
    counter += check_parse("LOGIN           |	  z|data", (None, None))
    counter += check_parse("LOGIN           |	  5|data", (None, None))

    if counter == TEST_COUNT:
        print(f"{Color.SUCCESS}\nALL TEST PASSED SUCCESSFULLY.")
    else:
        print(f"{Color.FAIL}\n{TEST_COUNT - counter} TESTS FAILED.")


if __name__ == '__main__':
    main()
