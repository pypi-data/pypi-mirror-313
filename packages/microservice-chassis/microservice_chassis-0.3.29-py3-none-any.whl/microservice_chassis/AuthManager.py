import jwt
import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class AuthService:
    algorithm = "RS256"  # Algoritmo predeterminado

    @staticmethod
    def generate_token(payload: dict, private_key: str, expiration: int = 3600):
        """Genera un token JWT con una expiración determinada."""
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode(payload, private_key, algorithm=AuthService.algorithm)

    @staticmethod
    def load_and_format_public_key(public_key_str: str):
        """Carga una clave pública en formato PEM, asegurando que sea válida."""
        # Convierte la clave pública en un objeto de clave pública
        public_key = serialization.load_pem_public_key(
            public_key_str.encode(),  # Convierte a bytes
            backend=default_backend()
        )
        return public_key


    @staticmethod
    def verify_token(token: str, public_key: str):
        """Verifica y decodifica un token JWT usando la clave pública."""
        try:
            pem_formatted_key = AuthService.load_and_format_public_key(public_key)
            return jwt.decode(token, pem_formatted_key, algorithms=[AuthService.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_authorization_header(authorization: str, public_key: str):
        """Verifica el encabezado de autorización."""
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"}
            )

        token = authorization.split(" ")[1] if len(authorization.split(" ")) == 2 else None
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid Authorization header format"}
            )

        try:
            token_data = AuthService.verify_token(token, public_key)
            if not token_data:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or expired token"}
                )
            return token_data
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )