import json


def error_response(status, message):
    return {"statusCode": status, "body": json.dumps({"error": message})}


def success_response(message):
    return {"statusCode": 200, "body": json.dumps({"message": message})}
