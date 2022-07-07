# Quiz Builder API
This API uses Python (Flask) as the backend, DynamoDB as the database, and Cognito as the authentication service.

## API Specification
The API specification is written in OpenAPI version 3, located at [openapi.yaml](https://git.toptal.com/screening/Suphan-Fayong/-/blob/main/openapi.yaml)

## Backend
The backend is written in Python with Flask. It is located in [functions](https://git.toptal.com/screening/Suphan-Fayong/-/tree/main/functions), consisting of 5 modules:
- **common** - common functions including authentication and error handling
- **question** - question endpoints: create, delete, edit
- **quiz** - quiz endpoints: create, delete, edit, get, list, publish
- **submission** - submission endpoints: create, get, list
- **user** - user endpoints: auth, confirm, signup

## Database
The database is running on Amazon DynamoDB. It consists of 3 tables:
- **Question table**
  - Primary key: question_id
  - Index: quiz_id
- **Quiz table**
  - Primary key: quiz_id
  - Index: user_id
- **Submission table**
  - Primary key: submission_key
  - 1st Index: quiz_id
  - 2nd Index: (user_id, quiz_id)

## Authentication
The authentication module utilizes Amazon Cognito.
- **Sign-up** - Sign up using an email (username) and a password. Password validation rules can be set in the Cognito console. After signed up, a confirmation code will be sent to the email for checking email ownership.
- **Confirm** - Confirm the email using a combination of the email (username) and the confirmation code.
- **Auth** - Sign in using an email (username) and a password. A pair of access token and refresh token will be returned. The access token is needed for using any endpoints in the API. After an access token expires, a user can authenticate again using email/password, or a refresh token.

## Test
Tests include every case mentioned in the user requirements and more. It is located in [test](https://git.toptal.com/screening/Suphan-Fayong/-/tree/main/test). It can be run using Pytest. Detail can be found on README in its folder.
### Run the tests
`pytest test/*.py`

## Deployment
The Flask backend needs to be deployed on a (virtual) machine. A permission to access DynamoDB and Cognito is required.
- If the VM is Amazon EC2, a permission is set by an [IAM role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html).
- If the VM is elsewhere, a permission is set using a pair of [access key ID and secret access key](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).
### Install packages
`pip3 install -r requirements.txt`
### Run the service
`python3 app.py`

A development version has been deployed on an EC2 instance. Its endpoint can be found in `API_HOST` in [config.py](https://git.toptal.com/screening/Suphan-Fayong/-/blob/main/test/config.py).
