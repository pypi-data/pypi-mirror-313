from cachetools import TTLCache, cached
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import SecurityScopes
import logging
import os

import googleapiclient.errors
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import requests
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel


# TODO: (mm) relative import?
from processcube_sdk.configuration.config_accessor import ConfigAccessor


logger = logging.getLogger("processcube.fastapi")

# See https://developers.google.com/identity/protocols/oauth2/openid-connect#obtaininguserprofileinformation
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

CACHE_MAX_SIZE = os.environ.get('GOOGLE_AUTH_CLIENT_CACHE_MAX_SIZE', 100)
CACHE_TTL = os.environ.get('GOOGLE_AUTH_CLIENT_CACHE_TTL', 2 * 60 * 60)  # 2 hours

class AuthUser(BaseModel):
    id: str
    email: str
    domain: str

@cached(cache=TTLCache(maxsize=CACHE_MAX_SIZE, ttl=timedelta(seconds=CACHE_TTL), timer=datetime.now))
def get_userinfo_endpoint() -> str:
    response = requests.get(GOOGLE_DISCOVERY_URL)
    userinfo_url = response.json()["userinfo_endpoint"]

    return userinfo_url

def authenticate(oauth_token: str = Security(APIKeyHeader(name="Authorization"))) -> AuthUser:

    userinfo_url = get_userinfo_endpoint()  # Could be cached
    headers = {"Authorization": f"Bearer {oauth_token}"}
    response = requests.get(userinfo_url, headers=headers)

    if response.status_code == 200:
        userinfo = response.json()
        user = AuthUser(
            id=userinfo["sub"], 
            email=userinfo["email"], 
            domain=userinfo.get("hd")
        )

        if user.domain == '5minds.de':
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OAuth Token",
        )


async def get_current_user(user: AuthUser = Depends(authenticate)) -> AuthUser:
    return user

async def authorize(
    security_scopes: SecurityScopes = None, user: AuthUser = Depends(authenticate)
) -> AuthUser:
    """Checks if the authenticated user is authorized for the required scope and
    returns the User. Use as follows:
    ```
    async def myendpoint(current_user: User = Security(authorize, scopes=["myscope"])):
        pass
    ```
    If you're only interested in getting the `User` object, you can leave away the
    scopes or use `authenticate` instead.
    """
    if security_scopes.scopes:
        for scope in security_scopes.scopes:
            if is_member(email=user.email, group=scope):
                return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing authorization! Required scope: "
            f"{' or '.join(security_scopes.scopes)}",
        )
    else:
        return user

def is_member(email: str, group: str, **kwargs) -> bool:
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    scopes = [
        "https://www.googleapis.com/auth/admin.directory.group.readonly",
        "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
    ]
    if kwargs.get("http"):
        # HttpMock for unit test
        service = build("admin", "directory_v1", http=kwargs["http"])
    else:
        #credentials = Credentials.from_service_account_info(
        #    info=settings.google_service_account_info, scopes=scopes
        #)
        credentials = Credentials.from_service_account_file(config.get('fastapi', 'google_service_account_file'), scopes=scopes)

        delegated_credentials = credentials.with_subject(config.get('fastapi', 'google_delegate_email'))
        service = build("admin", "directory_v1", credentials=delegated_credentials)
    try:
        results = (
            service.members()
            .hasMember(
                groupKey=group,
                memberKey=email,
            )
            .execute()
        )
        return results["isMember"]
    except googleapiclient.errors.HttpError as e:
        logger.error(
            f"Failed to look up user '{email}' in group '{group}': "
            f"{e.reason} (Error {e.status_code})"
        )
        return False