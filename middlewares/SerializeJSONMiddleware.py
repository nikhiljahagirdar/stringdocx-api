from fastapi import Request, Response, status
from fastapi.responses import JSONResponse


class SerializeJSONMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(
                    (k.decode("latin-1"), v.decode("latin-1"))
                    for k, v in message.get("headers", [])
                )
                if "application/json" not in headers.get("content-type", ""):
                    response = JSONResponse(
                        {"detail": "Response content-type must be application/json"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                    await response(scope, receive, send)
                    return
            await send(message)

        request = Request(scope, receive=receive)
        if request.method in ("POST", "PUT", "PATCH"):
            if request.headers.get("content-type") != "application/json":
                response = JSONResponse(
                    {"detail": "Request content-type must be application/json"},
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send_wrapper)
