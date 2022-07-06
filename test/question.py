import json
import requests
from config import API_HOST
from user import get_http_auth_header

def valid_question():
    return {
        "text": "Question Number X",
        "is_multiple": False,
        "choices": [
            "A. The first choice",
            "B. The second choice",
            "C. The third choice"
        ],
        "answers": [2]
    }

def test_valid_questions():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200

    question["is_multiple"] = True
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200

    question["answers"] = [1, 2]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_question_text():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    del question["text"]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["text"] = ""
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_question_choices():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    del question["choices"]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["choices"] = []
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # A question must have at least 2 choices
    question = valid_question()
    question["choices"] = ["A."]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # A question can have at most 5 choices
    question = valid_question()
    question["choices"] += ["D.", "E.", "F."]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_question_answers():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    del question["answers"]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["answers"] = []
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["answers"] = ["X"]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["answers"] = [1.1]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # An answer is out of range
    question = valid_question()
    question["answers"] = [-1]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # An answer is out of range
    question = valid_question()
    question["answers"] = [3]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # A single-answer question must have one answer.
    question = valid_question()
    question["answers"] = [1, 2]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    # An answer is out of range
    question = valid_question()
    question["is_multiple"] = True
    question["answers"] = [2, 3]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_question_multiple():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    del question["is_multiple"]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    question = valid_question()
    question["is_multiple"] = "X"
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_max_number_of_questions():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    for _ in range(10):
        question = valid_question()
        response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
        assert response.status_code == 200

    # A quiz can have at most 10 questions. The 11th question will be rejected.
    question = valid_question()
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 422

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200
