import json
from .db import get_db_connection
from .responses import error_response, success_response
from .verification import verify_code, process_already_verified
from .contrato_slug_check import process_contrato_slug_check, process_slug_format


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
    contrato_slug: str = body.get("contrato")

    if not number:
        return error_response(400, "Falta el 'phone-number' en la solicitud")

    if not code:
        return error_response(400, "Falta el 'code' en la solicitud")

    if not contrato_slug:
        return error_response(400, "Falta el 'contrato' en la solicitud")

    try:
        conn = get_db_connection()

        is_slug_format = process_slug_format(contrato_slug)
        if not is_slug_format:
            return error_response(400, "El contrato no tiene un formato válido.")
        
        contrato_id = process_contrato_slug_check(conn, contrato_slug)
        if not contrato_id:
            return error_response(400, "El contrato no existe.")

        # is_verified = process_already_verified(conn, number, contrato_id)
        # if is_verified:
        #     return error_response(
        #         200,
        #         f"El número '{number}' con contrato '{contrato_slug}' ya fue verificado",
        #     )

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
