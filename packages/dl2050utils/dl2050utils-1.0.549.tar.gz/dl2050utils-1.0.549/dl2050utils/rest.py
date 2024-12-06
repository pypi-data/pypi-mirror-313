"""
    rest.py
    Sets up the Asynchronous Server Gateway Interface (ASGI) Server backend

    Start an univorn server based on a set of downstream services: AppLog, Notify, DB, MQ, Auth and App.

    Serves all the routes included in three groups:
        1) Auth routes defined in the Auth instance
        2) Base routes defined in the App instance for general services
        3) Custom Application routes passed to the App instance from upper layer

    Errors are handled in layers
        1)  EXCEPTION in ASGI internal:
            Bugs inside backend module, should never arise
            HTTP return code: 500
            TEXT response set to traceback if debug mode is on
        2)  EXCEPTION in Middleware or endpoint:
            Bugs inside Middleware or Application modules, should never arise especially in Middleware
            HTTP return code: 400
            JSON response: {status:'ERROR', error_type:'EXCEPTION', error_msg:<err_msg>}
        3)  REST ERROR in accessing Endpoints:
            Request Errors with bad formed routes or missing or wrong arguments
            HTTP return code: 400
            JSON response: {status:'ERROR', error_type:'REST', error_msg:<err_msg>}
        3)  SERVICE ERROR in downstream services:
            Errors in well formed accesses to downstram services like DB, should never happer
            HTTP return code: 400
            JSON response: {status:'ERROR', error_type:'SERVICE', error_msg:<err_msg>}
        4) APP ERROR in App services:
            Errors in well formed accesses to App services, like missing users. Common and normnal.
            HTTP return code: 400
            JSON response: {status:'ERROR', error_type:'APP', error_msg:<err_msg>}
            Alternatively App services may return a normal response with extra information to deal with the error.
        5) Normal responses:
            HTTP return code: 200
            JSON response: {status:'OK', [msg:...,], ...}
"""

import asyncio
import traceback
import time
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette_jwt import JWTAuthenticationBackend
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from dl2050utils.core import oget
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.com import Notify, read_address_book
from dl2050utils.db import DB
from dl2050utils.mq import MQ
from dl2050utils.auth import Auth
from dl2050utils.restutils import HTTPException
from dl2050utils.restapp import App

# starlette_jwt
# https://github.com/amitripshtos/starlette-jwt/blob/master/starlette_jwt/middleware.py

DEBUG = True


class ASGI_Server:
    """ASGI Server setup and configuration.

    Initializes and runs the ASGI server, setting up middleware, routes, and exception handling.

    Attributes:
        service (str): Name of the service.
        path (str): URL path for the application.
        routes (list): List of routes for the application.
        appstartup (callable): Callable for application startup.
        perm (dict): Permissions for routes.
        qs (Queue): Message queue instance.
        port (int): Port number for the server.
        exception_handlers (dict): Handlers for various exceptions.
        middleware (list): List of middleware used in the server.
        routes (list): List of combined routes for Auth and App.
    """

    def __init__(self, service, path, routes, appstartup, perm, qs):
        """Initializes the ASGI server with services and middleware.

        Args:
            service (str): Service name for configuration.
            path (str): URL path prefix for routes.
            routes (list): Application routes.
            appstartup (callable): Startup function for the application.
            perm (dict): Permission configuration for routes.
            qs (Queue): Message queue instance.
        """
        if service is None:
            raise RuntimeError(f"ASGI_Server Service name not specified")
        cfg = config_load(service)
        cfg["service"] = service
        LOG = AppLog(cfg)
        NOTIFY = Notify(cfg=cfg, address_book=read_address_book())
        dbname = oget(cfg, ["db", "dbname"], "postgres")
        db = DB(cfg=cfg, log=LOG, dbname=dbname)
        mq = MQ(LOG, db, qs, cfg)
        auth = Auth(cfg, LOG, NOTIFY, db)
        app = App(cfg, LOG, NOTIFY, db, mq, auth, path, routes, appstartup, perm)
        self.LOG, self.db, self.mq, self.auth, self.app = LOG, db, mq, auth, app
        self.port = oget(cfg, ["rest", "port"], 5000)
        self.exception_handlers = {
            HTTPException: self.http_exception,
            404: self.http_exception,
            Exception: self.server_error_exception,
            500: self.server_error_exception,
        }
        auth_secret = cfg["rest"]["auth_secret"]
        self.middleware = [
            Middleware(RestStartMiddleware),
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                expose_headers=["*"],
            ),
            Middleware(
                AuthenticationMiddleware,
                backend=JWTAuthenticationBackend(
                    secret_key=auth_secret, prefix="Bearer", username_field="uid"
                ),
            ),
            Middleware(RestEndMiddleware, LOG=self.LOG, auth=auth),
        ]
        self.routes = auth.get_routes() + app.get_routes()

    async def http_exception(self, request, exc):
        """Handles HTTP exceptions, returning a formatted error response.

        Args:
            request (Request): The incoming request.
            exc (Exception): The exception raised.

        Returns:
            JSONResponse: JSON response with error details.
        """
        request.state.error = True
        error_type = exc.error_type if hasattr(exc, "error_type") else "REST"
        res = {"status": "ERROR", "error_type": error_type, "error_msg": exc.detail}
        return JSONResponse(res, status_code=exc.status_code)

    async def server_error_exception(self, request, exc):
        """Handles server errors with logging and error responses.

        Args:
            request (Request): The incoming request.
            exc (Exception): The exception raised.

        Returns:
            JSONResponse: JSON response with error details.
        """
        self.LOG(4, 0, label="REST", label2="SERVER_EXCEPTION", msg=exc.detail)
        return JSONResponse(
            {"status": "SERVER_EXCEPTION", "error_msg": exc.detail},
            status_code=exc.status_code,
        )

    async def startup(self):
        """Starts up all required services, including DB, MQ, Auth, and App.

        Raises:
            RuntimeError: If any service startup fails.

        Returns:
            bool: False if all services start successfully.
        """
        if await self.db.startup():
            raise ("DB startup error")
        await asyncio.sleep(15)
        if await self.mq.startup():
            self.LOG(3, 0, label="REST", label2="STARTUP", msg="MQ not available")
        if await self.auth.startup():
            raise ("Auth startup error")
        if await self.app.startup():
            raise ("App startup error")
        self.LOG(2, 0, label="REST", label2="STARTUP", msg=f"OK (port {self.port})")
        return False

    async def shutdown(self):
        """Logs and performs necessary shutdown tasks for the server."""
        self.LOG(2, 0, label="REST", label2="SHUTDOWN")

    def run(self, port=None):
        """Runs the ASGI server on the specified port.

        Args:
            port (int, optional): Port to run the server. Defaults to self.port.
        """
        rest = Starlette(
            debug=DEBUG,
            exception_handlers=self.exception_handlers,
            middleware=self.middleware,
            on_startup=[self.startup],
            on_shutdown=[self.shutdown],
            routes=self.routes,
        )
        port = port or self.port
        uvicorn.run(rest, port=port, host="0.0.0.0", log_level="critical")


class RestStartMiddleware(BaseHTTPMiddleware):
    """Middleware to initialize request state.

    Sets initial state attributes before request processing.

    Attributes:
        app (Starlette): The ASGI app instance.
    """

    def __init__(self, app):
        """Initializes RestStartMiddleware.

        Args:
            app (Starlette): The ASGI application instance.
        """
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Processes request by setting initial state and timing.

        Args:
            request (Request): The incoming request.
            call_next (callable): The next middleware or endpoint in the chain.

        Returns:
            Response: The final response after request processing.
        """
        request.state.error = False
        request.state.t0 = time.time()
        return await call_next(request)


class RestEndMiddleware(BaseHTTPMiddleware):
    """Middleware to finalize and log request details.

    Attributes:
        LOG (AppLog): Logger instance for logging events.
        auth (Auth): Authentication instance for request registration.
    """

    def __init__(self, app, LOG=None, auth=None):
        """Initializes RestEndMiddleware with logging and authentication.

        Args:
            app (Starlette): The ASGI application instance.
            LOG (AppLog, optional): Logger instance. Defaults to None.
            auth (Auth, optional): Authentication instance. Defaults to None.
        """
        super().__init__(app)
        self.LOG, self.auth = LOG, auth

    async def dispatch(self, request, call_next):
        """Processes request, logs, and handles errors.

        Args:
            request (Request): The incoming request.
            call_next (callable): The next middleware or endpoint in the chain.

        Returns:
            Response: The final response after request processing.
        """
        url = request.url.path
        uid = -1 if request.user.display_name == "" else request.user.display_name
        try:
            response = await call_next(request)
        except Exception as exc:
            error_msg = str(exc)
            log_msg = (
                {"error_msg": error_msg, "trace": traceback.format_exc()}
                if DEBUG
                else error_msg
            )
            t = time.time() - request.state.t0
            self.LOG(4, t, label="REST EXCEPTION", label2=url, msg=log_msg)
            return JSONResponse(
                {"status": "ERROR", "error_type": "EXCEPTION", "error_msg": error_msg},
                status_code=400,
            )
        if not request.state.error:
            t = time.time() - request.state.t0
            await self.auth.register_requests(url, uid, t)
            self.LOG(2, t, label="REST", label2=url, msg={"userid": uid})
        return response
