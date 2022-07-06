import os

os.environ["CLIENT_ID"] = "2bstaanlqnifan365lh6h3e96t"

from flask import Flask
from functions.quiz.create import quiz_create_file
from functions.quiz.delete import quiz_delete_file
from functions.quiz.edit import quiz_edit_file
from functions.quiz.get import quiz_get_file
from functions.quiz.list import quiz_list_file

from functions.user.auth import user_auth_file

app = Flask(__name__)
app.register_blueprint(quiz_create_file)
app.register_blueprint(quiz_delete_file)
app.register_blueprint(quiz_edit_file)
app.register_blueprint(quiz_get_file)
app.register_blueprint(quiz_list_file)

app.register_blueprint(user_auth_file)

if __name__ == "__main__":
    app.run()
