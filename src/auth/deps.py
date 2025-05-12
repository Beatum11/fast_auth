from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from datetime import datetime, timezone
from .utils import decode_token
from src.logger import logger
from src.db.redis import is_token_blocked


class TokenBearer(HTTPBearer):

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        http_creds = await super().__call__(request)

        try:
            token_data = decode_token(http_creds.credentials)
            
            exp_timestamp = datetime.fromtimestamp(token_data['exp'], tz=timezone.utc)

            if exp_timestamp < datetime.now(timezone.utc):
                logger.warning(f"Attempt to use expired token. Token ID: {token_data.get('jti')}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Expired token')
            
            if await is_token_blocked(token_data['jti']):
                logger.warning(f"Attempt to use blocked token. Token ID: {token_data['jti']}")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail='Token is blocked')

            return self.verify_token(token_data)
            
        except Exception as e:
            logger.error(f'Some error during token examination: {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Unexpected error: {e}')

    def verify_token(self, token_data: dict) -> dict:
        raise NotImplementedError("Subclasses must implement this method")
    


class RefreshTokenBearer(TokenBearer):

    def verify_token(self, token_data: dict) -> dict:
        if token_data['type'] == 'access':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Access token has been provided')
        return token_data    


class AccessTokenBearer(TokenBearer):
    
    def verify_token(self, token_data: dict) -> dict:
        if token_data['type'] == 'refresh':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Refresh token has been provided')
        
        return token_data