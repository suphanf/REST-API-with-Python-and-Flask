import os

os.environ["CLIENT_ID"] = "2bstaanlqnifan365lh6h3e96t"
os.environ["MAX_QUESTIONS"] = "10"
os.environ["MIN_CHOICES"] = "2"
os.environ["MAX_CHOICES"] = "5"
os.environ["MIN_ANSWERS"] = "1"
os.environ["MAX_ANSWERS"] = "5"

from flask import Flask
from functions.quiz.create import quiz_create_file
from functions.quiz.delete import quiz_delete_file
from functions.quiz.edit import quiz_edit_file
from functions.quiz.get import quiz_get_file
from functions.quiz.list import quiz_list_file
from functions.quiz.publish import quiz_publish_file

from functions.question.create import question_create_file
from functions.question.delete import question_delete_file
from functions.question.edit import question_edit_file

from functions.submission.create import submission_create_file
from functions.submission.get import submission_get_file
from functions.submission.list import submission_list_file

from functions.user.auth import user_auth_file
from functions.user.confirm import user_confirm_file
from functions.user.signup import user_signup_file

app = Flask(__name__)
app.register_blueprint(quiz_create_file)
app.register_blueprint(quiz_delete_file)
app.register_blueprint(quiz_edit_file)
app.register_blueprint(quiz_get_file)
app.register_blueprint(quiz_list_file)
app.register_blueprint(quiz_publish_file)

app.register_blueprint(question_create_file)
app.register_blueprint(question_delete_file)
app.register_blueprint(question_edit_file)

app.register_blueprint(submission_create_file)
app.register_blueprint(submission_get_file)
app.register_blueprint(submission_list_file)

app.register_blueprint(user_auth_file)
app.register_blueprint(user_confirm_file)
app.register_blueprint(user_signup_file)

if __name__ == "__main__":
    app.run()
