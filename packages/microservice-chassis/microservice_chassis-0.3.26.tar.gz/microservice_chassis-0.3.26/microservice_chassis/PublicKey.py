import httpx
import logging

# Configuración del logger
logger = logging.getLogger(__name__)


class PublicKeyResponse:
    def __init__(self, public_key: str):
        self.public_key = public_key


async def retrieve_public_key():
    logger.info("Retrieving public key")

    CLIENT_PUBLIC_KEY_URL = "http://haproxy:8080/client/auth/public-key"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(CLIENT_PUBLIC_KEY_URL)
            response.raise_for_status()

            # Cargar datos de la respuesta
            public_key_data = response.json().get("public_key")
            if not public_key_data:
                raise ValueError("Public key not found in response")

            logger.info("Public key retrieved successfully.")
            return public_key_data

    except httpx.RequestError as e:
        logger.error("Failed to retrieve public key: Request error - %s", e)
    except httpx.HTTPStatusError as e:
        logger.error("Failed to retrieve public key: HTTP error - %s", e)
    except Exception as e:
        logger.error("Failed to retrieve public key: %s", e)



# Ejemplo de uso
# public_key = await retrieve_public_key()
# print(public_key)  # Aquí podrías guardar o utilizar la clave como desees
