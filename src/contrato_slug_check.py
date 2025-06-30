import uuid


def process_contrato_slug_check(conn, contrato_slug):
    with conn.cursor() as cur:

        cur.execute(
            "SELECT id from checkout_custom_contrato where slug = %s", (contrato_slug,))
        result = cur.fetchone()
        if result:
            return result[0]
        return None


def process_slug_format(contrato_slug):
    try:
        uuid_obj = uuid.UUID(contrato_slug)
        return True
    except ValueError:
        return False
