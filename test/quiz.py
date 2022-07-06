import json
import requests
from config import API_HOST
from user import get_http_auth_header

def create_quiz(auth):
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    return quiz_id

def delete_quiz(auth, quiz_id):
    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_quiz_create():
    auth = get_http_auth_header()
    response = requests.post(f"{API_HOST}/quizzes", headers=auth)
    assert response.status_code == 400

    # A quiz's title cannot be empty
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": ""
    })
    assert response.status_code == 400

    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    response = requests.get(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert json.loads(response.text)["title"] == "Quiz's title"

    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_quiz_edit():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 400

    # A quiz's title cannot be empty
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}", headers=auth, json={
        "title": ""
    })
    assert response.status_code == 400

    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}", headers=auth, json={
        "title": "Quiz's new title"
    })
    assert response.status_code == 200

    response = requests.get(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert json.loads(response.text)["title"] == "Quiz's new title"

    delete_quiz(auth, quiz_id)

def test_quiz_list():
    auth = get_http_auth_header()
    quiz_ids = []
    for _ in range(3):
        quiz_ids.append(create_quiz(auth))

    # A user can list his/her own quizzes.
    response = requests.get(f"{API_HOST}/quizzes", headers=auth)
    actual_quiz_ids = list(map(lambda x: x["quiz_id"], json.loads(response.text)))
    for quiz_id in quiz_ids:
        assert quiz_id in actual_quiz_ids

    # A user cannot list other people's quizzes.
    auth1 = get_http_auth_header(1)
    response = requests.get(f"{API_HOST}/quizzes", headers=auth1)
    assert response.status_code == 200
    actual_quiz_ids = list(map(lambda x: x["quiz_id"], json.loads(response.text)))
    for quiz_id in quiz_ids:
        assert quiz_id not in actual_quiz_ids
    
    for quiz_id in quiz_ids:
        delete_quiz(auth, quiz_id)

def valid_question():
    return {
        "text": "Is it true?",
        "is_multiple": False,
        "choices": ["Yes", "No"],
        "answers": [0]
    }

def test_quiz_publish():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    # A user cannot publish an empty quiz.
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 422

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=valid_question())
    assert response.status_code == 200

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    delete_quiz(auth, quiz_id)

def test_published_quiz():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=valid_question())
    assert response.status_code == 200
    question_id = json.loads(response.text)["question_id"]

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    # Cannot edit the title in a published quiz
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}", headers=auth, json={
        "title": "Quiz's new title"
    })
    assert response.status_code == 422

    # Cannot add a question in a published quiz
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=valid_question())
    assert response.status_code == 422

    # Cannot edit a question in a published quiz
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth, json=valid_question())
    assert response.status_code == 422

    # Cannot delete a question in a published quiz
    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth)
    assert response.status_code == 422

    delete_quiz(auth, quiz_id)

def test_other_user_quiz():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=valid_question())
    assert response.status_code == 200
    question_id = json.loads(response.text)["question_id"]

    auth1 = get_http_auth_header(1)
    # Cannot edit other people's quiz
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}", headers=auth1, json={
        "title": "Quiz's new title"
    })
    assert response.status_code == 403

    # Cannot edit other people's quiz
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth1, json=valid_question())
    assert response.status_code == 403

    # Cannot edit other people's quiz
    response = requests.put(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth1, json=valid_question())
    assert response.status_code == 403

    # Cannot edit other people's quiz
    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}/questions/{question_id}", headers=auth1)
    assert response.status_code == 403

    delete_quiz(auth, quiz_id)
