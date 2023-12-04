import html

import requests
import json
import random
from html import unescape

QUESTION_API_URL = "https://opentdb.com/api.php?amount=50&difficulty=easy&type=multiple"


def get_randomized_options(correct_option: str, incorrect_options: list):
    """
       Randomize the order of options (including correct and incorrect ones) for a quiz question.
       Example:
       ```
       correct_option = "A"
       incorrect_options = ["B", "C", "D"]
       options, correct_index = get_randomized_options(correct_option, incorrect_options)
       print(options)  # Output: ['D', 'A', 'C', 'B']
       print(correct_index)  # Output: 2
       ```

       Note: The correct option is included in the randomized list, and the correct index is returned.
       """
    # Combine correct and incorrect options
    all_options = [correct_option] + incorrect_options

    # Randomize the order
    random.shuffle(all_options)

    # Find the index of the correct option in the randomized list
    correct_index = all_options.index(correct_option) + 1  # Adding 1 to make it 1-based index

    return all_options, correct_index


def load_question_with_api(starting_q_id: int = 1):
    """
    Load trivia questions from an external API and return a dictionary.

    Returns:
    - dict: A dictionary containing trivia questions, where keys are question IDs
            and values are dictionaries with question, answers, and correct index.

    Note: The correct option is determined by the 'get_randomized_options' function.
    """
    r = requests.get(QUESTION_API_URL)
    # Assuming r.content is the JSON content you provided
    json_data = json.loads(r.content)
    question_dict = {}

    # Extracting questions
    for q_id, question in enumerate(json_data["results"], start=starting_q_id):
        # Fixing HTML escape characters in the question and answers
        for key, value in question.items():
            question[key] = html.unescape(value)

        # Randomizing options and obtaining correct index
        options, correct = get_randomized_options(question["correct_answer"], question["incorrect_answers"])

        # Creating a dictionary entry for the question
        question_dict[q_id] = {"question": question["question"], "answers": list(options), "correct": correct}
        print(f"{q_id} - {question_dict[q_id]}")

    return question_dict


def main():
    load_question_with_api()


if __name__ == '__main__':
    main()
