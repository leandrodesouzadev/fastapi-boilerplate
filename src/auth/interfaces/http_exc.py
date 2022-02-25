from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid credentials"
    headers = {"WWW-authenticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)
