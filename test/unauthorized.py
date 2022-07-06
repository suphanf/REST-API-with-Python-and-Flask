import json
import requests
from config import API_HOST

def assert_unauthorized(response):
     assert response.status_code == 401
     assert json.loads(response.text)["message"] == "Unauthorized"

def test_quiz_create():
     assert_unauthorized(requests.post(f"{API_HOST}/quizzes"))

def test_quiz_delete():
     assert_unauthorized(requests.delete(f"{API_HOST}/quizzes/quiz_id"))

def test_quiz_edit():
     assert_unauthorized(requests.put(f"{API_HOST}/quizzes/quiz_id"))

def test_quiz_get():
     assert_unauthorized(requests.get(f"{API_HOST}/quizzes/quiz_id"))

def test_quiz_list():
     assert_unauthorized(requests.get(f"{API_HOST}/quizzes"))

def test_quiz_publish():
     assert_unauthorized(requests.post(f"{API_HOST}/quizzes/quiz_id/publish"))

def test_question_create():
     assert_unauthorized(requests.post(f"{API_HOST}/quizzes/quiz_id/questions"))

def test_question_delete():
     assert_unauthorized(requests.delete(f"{API_HOST}/quizzes/quiz_id/questions/question_id"))

def test_question_edit():
     assert_unauthorized(requests.put(f"{API_HOST}/quizzes/quiz_id/questions/question_id"))

def test_submission_create():
     assert_unauthorized(requests.post(f"{API_HOST}/quizzes/quiz_id/submissions"))

def test_submission_get():
     assert_unauthorized(requests.get(f"{API_HOST}/submissions/submission_id"))

def test_submission_list():
     assert_unauthorized(requests.get(f"{API_HOST}/submissions"))
