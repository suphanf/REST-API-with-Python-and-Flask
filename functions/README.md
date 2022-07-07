# List of endpoints

## question
POST `/quizzes/{quiz_id}/questions`

Create a new question in a quiz. The quiz must belong to the user and is not published. There is a maximum number of questions for a quiz defined in `MAX_QUESTIONS`.

A question is composed of:
- **text** - The question's text
- **is_multiple** - Does a question have multiple correct answers?
- **choices** - A list of text for each choice
- **answers** - A list of correct answers by index starting at 0

DELETE `/quizzes/{quiz_id}/questions/{question}`

Delete a question in a quiz. The quiz must belong to the user and is not published.

PUT `/quizzes/{quiz_id}/questions/{question}`

Edit a question in a quiz. The quiz must belong to the user and is not published. A question has the same format as that in creating a question.

## quiz
POST `/quizzes`

Create a quiz. A quiz contains a non-empty title.

DELETE `/quizzes/{quiz_id}`

Delete or disable a quiz. The quiz must belong to the user. If the quiz is published, this function disables the quiz. If the quiz is not published, this function deletes the quiz.

PUT `/quizzes/{quiz_id}`

Edit a quiz with a new title. The quiz must belong to the user and is not published.

GET `/quizzes/{quiz_id}`

Get quiz's details. If the quiz belongs to the user, details contain correct answers. If the quiz does not belong to the user, the quiz must be a published one and details do not contain correct answers.

GET `/quizzes`

List quizzes created by the user requesting this endpoint.

POST `/quizzes/{quiz_id}/publish`

Publish a quiz. The quiz must belong to the user and contains at least one question.

## submission

POST `/quizzes/{quiz_id}/submissions`

Create a submission for a quiz. The quiz must be a published one and does not belong to the user.
A submission is a list of user answers. A user answer is a list of numbers indicating the choice's indexes the user picks.
This function also calcuates a score for each question and a total score for the quiz.

GET `submissions/{submission_id}`

Get submission's details. The user requesting this endpoint must the quiz's creator or the one creating this submission. The details contain chosen answers, but do not contain correct answers.

GET `/quizzes/{quiz_id}/submissions`

List submissions by a quiz_id. The quiz must belong to the user.

GET `/submissions`

List submissions created by the user requesting this endpoint.

## user

POST `/user/auth`

Authenticate a user. There are two modes: `USER_PASSWORD_AUTH` and `REFRESH_TOKEN`.

- **USER_PASSWORD_AUTH** - Authenticate using an email (username) and a password
- **REFRESH_TOKEN** - Authenticate using a refresh token

This function returns an access token and a refresh token. The access token is used in `Authorization` header in all endpoints except `/user`. The refresh token is used in `REFRESH_TOKEN` mode.

POST `/user/confirm`

Confirm the email ownership using an email (username) and a confirmation code.

POST `/user/signup`

Sign up a new user using an email (username) and a password. A confirmation code will be sent to the email to verify the email ownership.
