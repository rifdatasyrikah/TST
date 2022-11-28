# sign, encode, decode, return JWT

import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#return generated tokens
def token_response(token: str):
    return {
        "access token" : token
    }

#function used for signing the JWT string
def signJWT(userID: str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        if decoded_token['expiry'] >= time.time():
            return decoded_token
        else:
            return None
    except:
        return {}