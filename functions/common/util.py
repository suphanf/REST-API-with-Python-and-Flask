def get_question_map(db, quiz_id):
    results = db.query(TableName="Question",
        IndexName="quiz_id-index",
        KeyConditionExpression="quiz_id = :quiz_id",
        ExpressionAttributeValues={
            ":quiz_id": { "S": quiz_id }
        }
    )

    question_map = {}
    for item in results["Items"]:
        question_map[item["question_id"]["S"]] = {
            "question_id": item["question_id"]["S"],
            "text": item["text"]["S"],
            "is_multiple": item["is_multiple"]["BOOL"],
            "choices": list(map(lambda x: x["S"], item["choices"]["L"])),
            "answers": sorted(list(map(int, item["answers"]["NS"])))
        }

    return question_map
