from functools          import wraps
from os                 import environ
from fastapi            import Depends, Security, HTTPException, Request
from fastapi.security   import APIKeyHeader


from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info

api_key_header   = APIKeyHeader(name="Authorization", auto_error=False)


def route_with_auth(router, method, path, **kwargs):
    if 'dependencies' not in kwargs:
        kwargs['dependencies'] = []
    kwargs['dependencies'].append(Depends(auth_the_user))

    def decorator(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            return func(*func_args, **func_kwargs)

        router_method = getattr(router, method.lower())
        return router_method(path, **kwargs)(wrapper)

    return decorator

def auth_the_user(request: Request, api_key: str = Security(api_key_header)):
    if api_key is None:
        if 'api_key' in request.cookies:
            api_key = request.cookies.get('api_key')
    if not verify_token(api_key):
        raise HTTPException(status_code=401, detail="Unauthorized***")
    return api_key

def verify_token(token: str) -> bool:
    auth_result     = False
    odin_auth_token = environ.get('ODIN_AUTH_TOKEN')
    if odin_auth_token:
        auth_result = token == odin_auth_token
    return auth_result