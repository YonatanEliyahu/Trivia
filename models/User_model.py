class User:
    def __init__(self, username: str, password: str, score: int = 0):
        self.__username: str = username
        self.__password: str = password
        self.__score: int = score
        self.__questions_asked: list = []

    def __str__(self):
        return f"{self.__username}: {self.__score}"

    def ask_question(self, question: int):
        self.__questions_asked.append(question)

    def update_score(self, points: int = 5):
        self.__score += points

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_score(self) -> int:
        return self.__score

    def get_questions_asked(self) -> list:
        return self.__questions_asked

    def check_password(self, password: str) -> bool:
        return self.__password == password

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            # Compare based on username
            return self.__username == other.__username
        elif isinstance(other, str):
            # Compare based on username with a string
            return self.__username == other
        return False

    def __lt__(self, other):  # used for sorting comparison
        return self.__score < other.score
