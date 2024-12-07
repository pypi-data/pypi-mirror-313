from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Request
import jwt
import time

class JWTBearer(HTTPBearer):
    def __init__(self, jwt_secret, jwt_algorithm: str = "HS256", auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication schem.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decode_jwt(jwtoken, self.jwt_secret, self.jwt_algorithm)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def decode_jwt(token: str, jwt_secret, jwt_algorithm = "HS256") -> dict:
    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm], options={
                                   "verify_aud": False, "verify_signature": True})
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}
