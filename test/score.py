import json
import requests
from config import API_HOST
from user import get_http_auth_header

def question_1():
    return {
        "text": "Moon is a star",
        "is_multiple": False,
        "choices": [
            "Yes",
            "No"
        ],
        "answers": [1]
    }

def question_2():
    return {
        "text": "Temperature can be measured in",
        "is_multiple": True,
        "choices": [
            "Kelvin",
            "Fahrenheit",
            "Gram",
            "Celsius",
            "Liters"
        ],
        "answers": [0, 1, 3]
    }

def submit_and_validate(answers, scores, total_score):
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "A quiz to validate score calculation"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question_1())
    assert response.status_code == 200

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question_2())
    assert response.status_code == 200

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=answers)
    assert response.status_code == 200

    submission_id = json.loads(response.text)["submission_id"]
    response = requests.get(f"{API_HOST}/submissions/{submission_id}", headers=auth1)
    submission = json.loads(response.text)
    for u_answer, score in zip(submission["user_answers"], scores):
        assert u_answer["score"] == score
    assert submission["total_score"] == total_score

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_skip_all():
    submit_and_validate([[], []], ["0", "0"], "0")

def test_question1_correct():
    submit_and_validate([[1], []], ["1", "0"], "1")

def test_question1_incorrect():
    submit_and_validate([[0], []], ["-1", "0"], "-1")

# If selected: Kelvin + Fahrenheit, score = 0.67
def test_question2_partial_correct():
    submit_and_validate([[], [0, 1]], ["0", "0.67"], "0.67")

# If selected: Kelvin + Fahrenheit + Celsius, score = 1
def test_question2_correct():
    submit_and_validate([[], [0, 1, 3]], ["0", "1"], "1")

# If selected: Kelvin + Fahrenheit + Gram, score = 0.17
def test_question2_mix():
    submit_and_validate([[], [0, 1, 2]], ["0", "0.17"], "0.17")

# If selected: Kelvin + Fahrenheit + Gram + Celsius + Liters, score = 0
def test_question2_cancel_out():
    submit_and_validate([[], [0, 1, 2, 3, 4]], ["0", "0"], "0")

# If selected: Gram + Liter, score = -1
def test_question2_incorrect():
    submit_and_validate([[], [2, 4]], ["0", "-1"], "-1")

def test_max_score():
    submit_and_validate([[1], [0, 1, 3]], ["1", "1"], "2")

def test_min_score():
    submit_and_validate([[0], [2, 4]], ["-1", "-1"], "-2")
