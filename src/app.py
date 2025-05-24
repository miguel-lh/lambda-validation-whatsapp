import json
from .db import get_db_connection
from .responses import error_response, success_response
from .verification import verify_code


def lambda_handler(event, context):
    if "body" in event:
        try:
            # Asegura que sea un dict
            body = (
                json.loads(event["body"])
                if isinstance(event["body"], str)
                else event["body"]
            )
        except json.JSONDecodeError:
            return error_response(400, f"Entrada Erronea {event}")
    else:
        # Si viene directo (por consola de pruebas en AWS)
        body = event

    print(body)

    number: str = body.get("phone-number")
    code: str = body.get("code")
    contrato_id: str = body.get("contrato")

    if not number:
        return error_response(400, "Falta el 'phone-number' en la solicitud")

    if not code:
        return error_response(400, "Falta el 'code' en la solicitud")

    if not contrato_id:
        return error_response(400, "Falta el 'contrato' en la solicitud")

    try:
        conn = get_db_connection()
        is_correct = verify_code(conn, number, code, contrato_id)

        if not is_correct:
            return error_response(
                400,
                "El código no es correcto o el número no está en un proceso de verificación",
            )

        return success_response("El código es correcto")
    except Exception as e:
        print(e)
        return error_response(500, "Server Error")
    finally:
        if "conn" in locals() and conn:
            conn.close()
