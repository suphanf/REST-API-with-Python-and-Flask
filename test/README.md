# Test cases

## question
- Check if adding or editing a valid question is successful
- Check if a question has an empty `text`
- Check if a question contains too many or too few `choices`
- Check if `answers` in a question are out-of-bound or invalid
- Check if `is_multiple` in a question is boolean
- Check if a quiz has the maximum number of `MAX_QUESTIONS` questions

## quiz
- Check if a `title` is not empty when creating a quiz
- Check if a `title` is not empty when editing a quiz
- Check if a user can list his/her own quizzes, but the others
- Check if publishing a quiz requires at least one question
- Check if a user is rejected when editing a published quiz or its questions
- Check if a user is rejected when trying to edit other people's quizzes

## score
- Check if individual scores and total scores are calculated correctly on various cases

## submission
- Check if a user is rejected when taking his/her own quiz
- Check if a user is rejected when taking an unpublished quiz
- Check if a user is rejected when taking a published quiz twice
- Check if a submission cannot be seen by one not the quiz's owner and not a quiz's taker
- Check if a user can list submissions by his/her own quiz, but not others
- Check if a user can list his/her own submissions
- Check if a submission does not contain actual `answers` fields

## unauthorized
- Check all unauthorized requests
