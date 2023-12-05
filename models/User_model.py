class User:
    """
    Represents a user in the trivia system.

    Attributes:
    - username (str): The username of the user.
    - password (str): The password of the user.
    - score (int): The score of the user. Default is 0.
    - questions_asked (list): List of question IDs asked by the user.

    Methods:
    - __init__(self, username: str, password: str, score: int = 0): Initializes a new User.
    - __str__(self): Returns a formatted string representation of the user.
    - ask_question(self, question: int): Adds a question ID to the list of asked questions.
    - update_score(self, points: int = 5): Updates the user's score by adding points.
    - get_username(self) -> str: Gets the username of the user.
    - get_password(self) -> str: Gets the password of the user.
    - get_score(self) -> int: Gets the score of the user.
    - get_questions_asked(self) -> list: Gets the list of questions asked by the user.
    - check_password(self, password: str) -> bool: Checks if the provided password matches the user's password.
    - __eq__(self, other) -> bool: Compares two users based on username.
    - __lt__(self, other): Used for sorting comparison based on score.

    Raises:
    - ValueError: If invalid input is provided during user creation.
    """
    def __init__(self, username: str, password: str, score: int = 0):
        if username is None or password is None or score <0:
            raise ValueError("Invalid input for User creation")
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
