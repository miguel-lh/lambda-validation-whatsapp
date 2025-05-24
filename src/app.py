import os
import boto3
from botocore.exceptions import ClientError
import json
import psycopg2


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"}),
        }

    if "phone-number" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'phone-number' in request body"}),
        }

    number: str = body.get("phone-number", None)

    if not number:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'phone-number' must be a non-empty number"}),
        }

    if "code" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'code' in request body"}),
        }

    code: str = body.get("code", None)

    if not code:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'code' must be a non-empty value"}),
        }

    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT")

    conn = None

    try:
        print(f"Conecting to database at {db_host}...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port,
        )

        cur = conn.cursor()
        print("Conection success")

        cur.execute(f"SELECT * FROM registros WHERE phone_number = '{number}';")

        db_number = cur.fetchone()

        if not db_number:
            cur.close()
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "message": "the number is not currently in a verification process."
                    }
                ),
            }

        verified = db_number[2]

        if verified:
            cur.close()
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "the number is already verified."}),
            }

        otp_code = db_number[1]

        if code != otp_code:
            cur.close()
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "The received code is incorrect."}),
            }

        # otp-code is correct
        cur.execute(
            "UPDATE registros SET verified = %s WHERE phone_number = %s",
            ("TRUE", f"{number}"),
        )

        conn.commit()
        cur.close()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Code is correct, phone-number verified."}),
        }

    except psycopg2.OperationalError as e:
        print(f"Error while connecting:")
        print(e)
        if e.diag:
            print(f"PGCODE: {e.diag.sqlstate}")
            print(f"PGERROR: {e.diag.message_primary}")
    except Exception as e:
        print(f"Unexpected error")
        print(e)
    finally:
        if conn:
            conn.close()
            print("Conection closed")
