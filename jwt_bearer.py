# request authorized or not

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt_handler import decodeJWT

#subclass, for persist authentication
class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error = auto_Error)

    #computer freed from process, io processes
    async def __call__(self, req : Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(req) # wait for that long process
        if credentials:
            if not credentials.scheme == "Bearer": #if credential scheme is not bearer scheme
                raise HTTPException(status_code=403, details="Invalid or Expired token!")
            else :
                return credentials.credentials
        else: 
            raise HTTPException(status_code=403, details="Invalid or Expired token!")
    
    #token valid or not
    def verify_jwt(self, jwtoken: str)   :
        isTokenValid : bool = False #false flag
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid