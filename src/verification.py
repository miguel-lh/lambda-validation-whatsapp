# Si el numero ya esta verificado
def process_already_verified(conn, number, contrato_id) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT verified
            FROM whatsapp_verification_whatsappverification
            WHERE phone_number = %s and contrato_id = %s
        """,
            (
                number,
                contrato_id,
            ),
        )

        result = cur.fetchone()

        verified = result[0]

        return verified


# Verifica si el codigo es correcto
def verify_code(conn, number, code, contrato_id) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT otp_code
            FROM whatsapp_verification_whatsappverification
            WHERE phone_number = %s and contrato_id = %s
        """,
            (
                number,
                contrato_id,
            ),
        )

        result = cur.fetchone()

        # No está en proceso de verificación
        if not result:
            return False

        if code != result[0]:
            return False

        cur.execute("""
            UPDATE whatsapp_verification_whatsappverification
            SET verified = TRUE
            WHERE phone_number = %s AND contrato_id = %s
        """,
            (
                number,
                contrato_id,
            ),
        )
        conn.commit()

        return True
