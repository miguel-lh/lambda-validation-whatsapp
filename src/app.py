import json
from .db import get_db_connection
from .responses import error_response, success_response
from .verification import verify_code


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"}),
        }

    number: str = body.get("phone-number")
    code: str = body.get("code")
    contrato: str = body.get("cotizacion")

    if not number:
        return error_response(400, "Falta el 'phone-number' en la solicitud")

    if not code:
        return error_response(400, "Falta el 'code' en la solicitud")

    if not contrato:
        return error_response(400, "Falta el 'contrato' en la solicitud")

    try:
        conn = get_db_connection()
        is_correct = verify_code(conn, number, code, contrato)

        if not is_correct:
            return error_response(
                400,
                "El codigo no es correcto o el número no esta en un proceso de verificación",
            )

        return success_response("El código es correcto")
    except Exception as e:
        print(e)
        return error_response(500, "Server Eror")
    finally:
        if "conn" in locals() and conn:
            conn.close()
