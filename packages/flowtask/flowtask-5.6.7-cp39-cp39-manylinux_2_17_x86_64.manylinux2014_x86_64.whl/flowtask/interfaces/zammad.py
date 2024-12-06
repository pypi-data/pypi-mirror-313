from navigator.conf import (
    ZAMMAD_INSTANCE,
    ZAMMAD_TOKEN,
    ZAMMAD_DEFAULT_CUSTOMER,
    ZAMMAD_DEFAULT_GROUP,
    ZAMMAD_DEFAULT_CATALOG,
    ZAMMAD_ORGANIZATION,
    ZAMMAD_DEFAULT_ROLE,
)
from ..exceptions import ComponentError
from .http import HTTPService


class zammad(HTTPService):
    """zammad.

    Generic Interface for managing Zammad instances.
    """

    accept: str = "application/json"
    token_type: str = "Bearer"
    auth_type: str = "apikey"

    article_base: dict = {"type": "note", "internal": False}
    permissions_base: dict = {
        "name": "api_user_token",
        "label": "User Token",
        "permissions": ["api"],
    }

    def __init__(self, **kwargs):
        self.credentials: dict = {}
        HTTPService.__init__(self, **kwargs)
        self.auth = {self.token_type: ZAMMAD_TOKEN}

    async def get_user_token(self, **kwargs):
        """get_user_token.


        Usage: using X-On-Behalf-Of to getting User Token.

        """
        self.url = f"{ZAMMAD_INSTANCE}api/v1/user_access_token"
        self.method = "post"
        permissions: list = kwargs.pop("permissions", [])
        user = kwargs.pop("user", ZAMMAD_DEFAULT_CUSTOMER)
        token_name = kwargs.pop("token_name")
        self.headers["X-On-Behalf-Of"] = user
        self.accept = "application/json"
        ## create payload for access token:
        data = {
            **self.permissions_base,
            **{"name": token_name, permissions: permissions},
        }
        result, _ = await self.async_request(self.url, self.method, data, use_json=True)
        return result["token"]

    async def create_user(self, **kwargs):
        """create_user.

        Create a new User.

        TODO: Adding validation with dataclasses.
        """
        self.url = f"{ZAMMAD_INSTANCE}api/v1/users"
        self.method = "post"
        result = None
        error = None
        organization = kwargs.pop("organization", ZAMMAD_ORGANIZATION)
        roles = kwargs.pop("roles", [ZAMMAD_DEFAULT_ROLE])
        if not isinstance(roles, list):
            roles = ["Customer"]
        data = {"organization": organization, "roles": roles, **kwargs}
        try:
            result, error = await self.async_request(self.url, self.method, data=data)
            if error:
                raise ComponentError(f"Error creating Zammad User: {error}")
        except Exception as e:
            error = str(e)
        return result, error
