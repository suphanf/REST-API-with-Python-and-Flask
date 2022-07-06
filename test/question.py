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

def check_invalid_create(auth, quiz_id, question):
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 400

def check_invalid_edit(auth, quiz_id, question, question_id):
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth, json=question)
    assert response.status_code == 400

def create_quiz(auth):
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200
    question_id = json.loads(response.text)["question_id"]

    return quiz_id, question_id

def delete_quiz(auth, quiz_id):
    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_valid_questions():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    # A valid question
    question = valid_question()
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200
    question_id = json.loads(response.text)["question_id"]

    # A valid question
    question["is_multiple"] = True
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth, json=question)
    assert response.status_code == 200

    # A valid question
    question["answers"] = [1, 2]
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth, json=question)
    assert response.status_code == 200

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth)
    assert response.status_code == 200

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_question_text():
    auth = get_http_auth_header()
    quiz_id, question_id = create_quiz(auth)

    question = valid_question()
    del question["text"]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["text"] = ""
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    delete_quiz(auth, quiz_id)

def test_question_choices():
    auth = get_http_auth_header()
    quiz_id, question_id = create_quiz(auth)

    question = valid_question()
    del question["choices"]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["choices"] = []
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # A question must have at least 2 choices
    question = valid_question()
    question["choices"] = ["A."]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # A question can have at most 5 choices
    question = valid_question()
    question["choices"] += ["D.", "E.", "F."]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    delete_quiz(auth, quiz_id)

def test_question_answers():
    auth = get_http_auth_header()
    quiz_id, question_id = create_quiz(auth)

    question = valid_question()
    del question["answers"]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["answers"] = []
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["answers"] = ["X"]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["answers"] = [1.1]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # An answer is out of range
    question = valid_question()
    question["answers"] = [-1]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # An answer is out of range
    question = valid_question()
    question["answers"] = [3]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # A single-answer question must have one answer.
    question = valid_question()
    question["answers"] = [1, 2]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    # An answer is out of range
    question = valid_question()
    question["is_multiple"] = True
    question["answers"] = [2, 3]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    delete_quiz(auth, quiz_id)

def test_question_multiple():
    auth = get_http_auth_header()
    quiz_id, question_id = create_quiz(auth)

    question = valid_question()
    del question["is_multiple"]
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    question = valid_question()
    question["is_multiple"] = "X"
    check_invalid_create(auth, quiz_id, question)
    check_invalid_edit(auth, quiz_id, question, question_id)

    delete_quiz(auth, quiz_id)

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
