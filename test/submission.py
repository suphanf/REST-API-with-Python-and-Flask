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

def create_quiz(auth):
    response = requests.post(f"{API_HOST}/quizzes", headers=auth, json={
        "title": "Quiz's title"
    })
    assert response.status_code == 200
    quiz_id = json.loads(response.text)["quiz_id"]

    question = valid_question()
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/questions", headers=auth, json=question)
    assert response.status_code == 200

    return quiz_id

def delete_quiz(auth, quiz_id):
    response = requests.delete(f"{API_HOST}/quizzes/{quiz_id}", headers=auth)
    assert response.status_code == 200

def test_submit_own_quiz():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    # Cannot take his/her own quiz
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth, json=[[0]])
    assert response.status_code == 403

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    # Cannot take his/her own quiz
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth, json=[[0]])
    assert response.status_code == 403

    delete_quiz(auth, quiz_id)

def test_submit_unpublished_quiz():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    # Cannot take an unpublished quiz
    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 404

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    # Take a published quiz successfully
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 200

    delete_quiz(auth, quiz_id)

def test_submission_same_quiz_twice():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 200

    # A user cannot take the same quiz twice
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 403

    delete_quiz(auth, quiz_id)

def test_submission_unseen_by_others():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 200
    submission_id = json.loads(response.text)["submission_id"]
    
    response = requests.get(f"{API_HOST}/submissions/{submission_id}", headers=auth)
    assert response.status_code == 200

    response = requests.get(f"{API_HOST}/submissions/{submission_id}", headers=auth1)
    assert response.status_code == 200

    # A user cannot see other people's submissions if it is not his/her own quiz
    auth2 = get_http_auth_header(2)
    response = requests.get(f"{API_HOST}/submissions/{submission_id}", headers=auth2)
    assert response.status_code == 403

    delete_quiz(auth, quiz_id)

def test_submission_list_by_quiz_id():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 200
    submission_id1 = json.loads(response.text)["submission_id"]

    auth2 = get_http_auth_header(2)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth2, json=[[1]])
    assert response.status_code == 200
    submission_id2 = json.loads(response.text)["submission_id"]

    # List submission by quiz_id (the owner)
    response = requests.get(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth)
    assert response.status_code == 200
    submission_ids = list(map(lambda x: x["submission_id"], json.loads(response.text)))
    assert submission_id1 in submission_ids
    assert submission_id2 in submission_ids

    # List submission by quiz_id (not the owner)
    response = requests.get(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1)
    assert response.status_code == 403

    # List submission by quiz_id (not the owner)
    response = requests.get(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth2)
    assert response.status_code == 403

    delete_quiz(auth, quiz_id)

def test_submission_list_by_user_id():
    auth0 = get_http_auth_header()
    quiz_id0 = create_quiz(auth0)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id0}/publish", headers=auth0)
    assert response.status_code == 200

    auth1 = get_http_auth_header()
    quiz_id1 = create_quiz(auth1)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id1}/publish", headers=auth1)
    assert response.status_code == 200

    auth2 = get_http_auth_header(2)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id0}/submissions", headers=auth2, json=[[1]])
    assert response.status_code == 200
    submission_id0 = json.loads(response.text)["submission_id"]

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id1}/submissions", headers=auth2, json=[[2]])
    assert response.status_code == 200
    submission_id1 = json.loads(response.text)["submission_id"]

    # List submission by user_id
    response = requests.get(f"{API_HOST}/submissions", headers=auth2)
    assert response.status_code == 200
    submission_ids = list(map(lambda x: x["submission_id"], json.loads(response.text)))
    assert submission_id0 in submission_ids
    assert submission_id1 in submission_ids

    delete_quiz(auth0, quiz_id0)
    delete_quiz(auth1, quiz_id1)

def test_submission_fields():
    auth = get_http_auth_header()
    quiz_id = create_quiz(auth)

    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/publish", headers=auth)
    assert response.status_code == 200

    auth1 = get_http_auth_header(1)
    response = requests.post(f"{API_HOST}/quizzes/{quiz_id}/submissions", headers=auth1, json=[[0]])
    assert response.status_code == 200
    submission_id = json.loads(response.text)["submission_id"]

    response = requests.get(f"{API_HOST}/submissions/{submission_id}", headers=auth)
    assert response.status_code == 200
    submission = json.loads(response.text)

    # No correct answers are shown
    for u_answer in submission["user_answers"]:
        assert "question_text" in u_answer
        assert "chosen" in u_answer
        assert "score" in u_answer
        assert len(u_answer) == 3

    delete_quiz(auth, quiz_id)
