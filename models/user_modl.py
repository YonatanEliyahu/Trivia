class User:
    def __init__(self, username: str, password: str, score: int = 0):
        self.__username = username
        self.__password = password
        self.__score = score
        self.__questions_asked = []

    def __str__(self):
        return f"{self.__username}: {self.__score}"

    def ask_question(self, question: int):
        self.__questions_asked.append(question)

    def update_score(self, points: int):
        self.__score += points

    def get_username(self):
        return self.__username

    def get_score(self):
        return self.__score

    def get_questions_asked(self):
        return self.__questions_asked

    def check_login_info(self, username: str, password: str) -> bool:
        return self.__username == username and self.__password == password

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            # Compare based on username
            return self.__username == other.__username
        elif isinstance(other, str):
            # Compare based on username with a string
            return self.__username == other
        return False
