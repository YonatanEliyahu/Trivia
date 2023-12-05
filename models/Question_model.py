class Question:
    """
    Represents a trivia question with multiple-choice answers.

    Attributes:
        __question (str): The text of the question.
        __answers (list): A list of possible answers.
        __correct (int): The index of the correct answer in the __answers list.
    """
    def __init__(self, question: str, answers: list, correct: int):
        if question is None or answers is [] or not (1 <= correct <= 4):
            raise ValueError("Invalid input for Question creation")
        self.__question: str = question
        self.__answers: list = answers
        self.__correct: int = correct

    def __str__(self):
        options = '\n'.join(f'\t{i}. {option}' for i, option in enumerate(self.__answers, start=1))
        return f"{self.__question}\n{options}\ncorrect: {self.__correct}"

    def chatlib_supporting_str(self, q_id):
        return f"{q_id}#{self.__question}#" + \
               str('#'.join(str(answer) for answer in self.__answers))
        # example 2313#How much is 2+2?#3#4#2#1

    def get_question(self) -> str:
        return self.__question

    def get_answers(self) -> list:
        return self.__answers

    def get_correct_ans(self) -> int:
        return self.__correct

    def check_ans(self, ans: int) -> bool:
        return self.__correct == ans

    def __eq__(self, other) -> bool:
        if isinstance(other, Question):
            # Compare based on username
            return self.__question == other.__question
        return False
