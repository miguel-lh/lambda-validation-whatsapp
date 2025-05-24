# Verifica si el codigo es correcto


def verify_code(conn, number, code, cotizacion) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT otp_code FROM registros WHERE phone_number = %s and cotizacion = %s",
            (
                number,
                cotizacion,
            ),
        )

        result = cur.fetchone()

        # No está en proceso de verificación
        if not result:
            return False

        if code != result:
            return False

        return True
