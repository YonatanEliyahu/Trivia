import requests
import json
import random

QUESTION_API_URL = "https://opentdb.com/api.php?amount=50&difficulty=easy&type=multiple"


def get_randomized_options(correct_option, incorrect_options):
    # Combine correct and incorrect options
    all_options = [correct_option] + incorrect_options

    # Randomize the order
    random.shuffle(all_options)

    # Find the index of the correct option in the randomized list
    correct_index = all_options.index(correct_option) + 1  # Adding 1 to make it 1-based index

    return all_options, correct_index


def load_question_with_api():
    r = requests.get(QUESTION_API_URL)
    # Assuming r.content is the JSON content you provided
    json_data = json.loads(r.content)
    question_dict = {}
    # Extracting questions
    for q_id, question in enumerate(json_data["results"], start=1):
        options, correct = get_randomized_options(question["correct_answer"], question["incorrect_answers"])
        question_dict[q_id] = {"question": question["question"], "answers": list(options), "correct": correct}
        print(f"{q_id} - {question_dict[q_id]}")

    return question_dict


def main():
    load_question_with_api()


if __name__ == '__main__':
    main()
