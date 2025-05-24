# Verifica si el codigo es correcto


def verify_code(conn, number, code, contrato_id) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT otp_code FROM registros WHERE phone_number = %s and contrato_id = %s",
            (
                number,
                contrato_id,
            ),
        )

        result = cur.fetchone()

        print(f"resultado: {result}")

        # No está en proceso de verificación
        if not result:
            return False

        if code != result[0]:
            return False

        return True
