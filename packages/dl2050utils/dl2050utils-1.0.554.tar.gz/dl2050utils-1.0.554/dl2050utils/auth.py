"""
    auth.py
    Class for users authentication backend

    All REST and downstream service errors are handled through log_and_raise_service
    All Auth REST facing methods return rest_ok
        {status:'OK, [user_status:<user_status>], [auth_status:<auth_status>, auth_msg:<auth_error_msg>]}

    Internal methods:
        get_routes
        startup
        shutdown
        check_auth

    REST methods for users:
        auth_info
        check_user
        check_otp
        set_passwd
        login
        recover_passwd
        change_passwd
        register

    REST methods for admin:
        get_users
        update_user
        reset_user
        suspend_user
        delete_user
        change_org

    Links:
    https://www.starlette.io/authentication/
    https://github.com/amitripshtos/starlette-jwt

    TODO: Response for Auth errors like WRONG_PASSWD, SUSPENDED_FAILS is 200 with STATUS OK, should be HTTP Exception 401,403.
    TODO: Handle inputs with invalid JSON body -> change data = await request.json() to get_request_json(request) from restuitls
"""

from datetime import datetime, timezone
import bcrypt
from starlette.routing import Route
from dl2050utils.core import oget
from dl2050utils.com import send_otp
from dl2050utils.db import res_to_recs, rec_to_row
from dl2050utils.restutils import (
    log_and_raise_service,
    enforce_required_args,
    rest_ok,
    mk_key,
    mk_jwt_token,
)

# ####################################################################################################
# Defenitions and helper functions
# ####################################################################################################

MAX_FAILS = 5
MAX_REQUESTS = 1e6

# user_status
NOT_REGISTERED = 0
WAIT_SET_PASSWD = 1
SUSPENDED = 2
SUSPENDED_LICENCE = 3
SUSPENDED_FAILS = 4
SUSPENDED_REQUESTS = 5
ACTIVE = 10


def increase(d, f, reset=False):
    """Increments a field `f` in the user dictionary `d`. Updates `ts_access` and `ts_login` if login route.

    Args:
        d (dict): User dictionary to update.
        f (str): Field name to increment.
        reset (bool, optional): Resets field to zero if True. Defaults to False.
    """
    if d is None or f not in d:
        return
    if d[f] is None or reset:
        d[f] = 0
    d[f] += 1
    d["ts_access"] = datetime.now(timezone.utc)
    if f == "logins":
        d["ts_login"] = datetime.now(timezone.utc)


def get_age_in_seconds(ds):
    """Calculates time difference in seconds from `ds` to the current time.

    Args:
        ds (str): Date string in '%Y-%m-%d %H:%M:%S' format.

    Returns:
        int: Time difference in seconds.
    """
    s1 = int(datetime.now(timezone.utc).strftime("%s"))
    s2 = int(datetime.strptime(ds, "%Y-%m-%d %H:%M:%S").strftime("%s"))
    return s1 - s2


def get_user_info(user):
    """Extracts main user information for response.

    Args:
        user (dict): Dictionary containing user data.

    Returns:
        dict: Key user information including `uid`, `email`, `name`, `status`, etc.
    """
    return {
        "uid": user["id"],
        "email": user["email"],
        "short": user["short"],
        "name": user["name"],
        "status": user["ustatus"],
        "role": user["role"],
        "org": user["org"],
        "dep": user["org"],
    }


def check_passwd_strengh(passwd):
    """Checks if a password meets minimum length requirement.

    Args:
        passwd (str): Password to check.

    Returns:
        bool: True if password has at least 6 characters, False otherwise.
    """
    if type(passwd) != str:
        return False
    if len(passwd) < 6:
        return False
    return True


# ####################################################################################################
# Auth class
# ####################################################################################################


class Auth:
    """
    Class handling user authentication backend operations.

    Includes methods for user authentication, management, and authorization.
    """

    def __init__(self, cfg, LOG, NOTIFY, db):
        """
        Initializes the Auth class with configuration, logging, notifications, and database.

        Args:
            cfg (dict): Configuration settings.
            LOG (callable): Logging function.
            NOTIFY (callable): Notification function.
            db (object): Database connection object.
        """
        self.cfg, self.LOG, self.NOTIFY, self.db = cfg, LOG, NOTIFY, db

    # ####################################################################################################
    # Helper methods
    # ####################################################################################################

    def ret(self, auth_status=None, user_status=None, payload=None):
        """Helper to construct standardized response with auth and user statuses.

        Args:
            auth_status (str, optional): Authentication status.
            user_status (str, optional): User status.
            payload (dict, optional): Additional data to include in the response.

        Returns:
            dict: Standardized response using rest_ok.
        """
        d = {}
        if auth_status:
            d["auth_status"] = auth_status
        if user_status:
            d["user_status"] = user_status
        if type(payload) == dict:
            d = {**d, **payload}
        return rest_ok(d)

    async def db_update(self, tbl, kc, d, prefix=""):
        """Updates a record in the database and logs errors if they occur.

        Args:
            tbl (str): Table name to update.
            kc (str): Key column for identifying record.
            d (dict): Data to update.
            prefix (str, optional): Log prefix label.

        Raises:
            ServiceException: If the database update fails.
        """
        res = await self.db.update(tbl, kc, d)
        if res:
            log_and_raise_service(
                self.LOG, label="AUTH", label2=prefix, msg="DB update error"
            )

    async def enforce_find_user(self, d, label2=""):
        """Finds a user in the database by criteria and checks active status.

        Args:
            d (dict): Search criteria.
            label2 (str, optional): Additional label for logging.

        Returns:
            dict: User record if found and active.

        Raises:
            ServiceException: If user is not found or inactive.
        """
        user = await self.db.select_one("users", d)
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="User not found",
                status_code=401,
            )
        if user["ustatus"] != ACTIVE:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="User not active",
                status_code=403,
            )
        return user

    async def enforce_admin_perm(self, request, label2="", requires_su=True):
        """Checks if a user has administrative permissions.

        Args:
            request (Request): Incoming request object.
            label2 (str, optional): Label for logging.
            requires_su (bool, optional): Whether superuser permissions are required.

        Returns:
            tuple: User role and organization if permissions are valid.

        Raises:
            ServiceException: If permissions are insufficient.
        """
        user = await self.enforce_find_user(
            {"id": request.user.display_name}, label2=label2
        )
        role, org = user["role"], user["org"]
        roles = ["su"] if requires_su else ["su", "admin"]
        if user["ustatus"] != ACTIVE or role not in roles:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg=f"{label2}: User is not admin",
                status_code=403,
            )
        return role, org

    async def increase_fails(self, user, fail="LOGIN"):
        """Handles login failure tracking and user suspension if threshold exceeded.

        Args:
            user (dict): User record.
            fail (str, optional): Type of failure (e.g., LOGIN).

        Returns:
            bool: True if user was suspended due to excessive failures, False otherwise.

        Logs:
            Failure counts and suspension actions.
        """
        increase(user, "fails")
        if user["fails"] > MAX_FAILS:
            user["ustatus"] = SUSPENDED_FAILS
            self.LOG(
                4,
                0,
                label="AUTH",
                label2="increase_fails",
                msg=f"Too many {fail} fails for user {user['email']} - USER SUSPENDED",
            )
            await self.db_update("users", "email", user, "increase_fails")
            return True
        await self.db_update("users", "email", user, "increase_fails")
        self.LOG(
            3,
            0,
            label="AUTH",
            label2="increase_fails",
            msg=f"{fail} fail for user {user['email']}",
        )
        return False

    async def gen_otp(self, user):
        """Generates and send OTP to the user"""
        if self.otp_mode == "phone" and oget(user, ["phone"]) is None:
            log_and_raise_service(
                self.LOG, label="AUTH", label2="gen_otp", msg="Phone not defined"
            )
        otp = mk_key(n=4)
        self.LOG(
            2,
            0,
            label="AUTH",
            label2="gen_otp",
            msg={"email": user["email"], "OTP": otp},
        )
        err = send_otp(
            self.NOTIFY, self.otp_mode, self.product, user["email"], user["phone"], otp
        )
        if err is not None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2="gen_otp",
                msg="email error when sending OTP",
            )
        user["otp"], user["ts_passwd"], user["ustatus"] = (
            otp,
            datetime.now(timezone.utc),
            WAIT_SET_PASSWD,
        )
        await self.db_update("users", "email", user, "gen_otp")

    # ####################################################################################################
    # register_requests: called from REST for every request
    # ####################################################################################################

    async def register_requests(self, url, uid, t):
        """Used by App to register all requests and rate limit users"""
        if url in ["/api/auth/is_auth", "/api/get_meta"] or uid == -1:
            return
        await self.db.insert(
            "metrics",
            {"ts": datetime.now(timezone.utc), "uid": uid, "url": url, "t": t},
        )
        user = await self.db.select_one("users", {"id": uid})
        increase(user, "requests")
        if user["requests"] > MAX_REQUESTS:
            user["ustatus"] = SUSPENDED_REQUESTS
        await self.db_update("users", "email", user, "register_requests")

    # ####################################################################################################
    # Internal methods: used by App to manage Auth service
    # ####################################################################################################

    def get_routes(self):
        """ " Used by App to include Auth routes in the App routes"""
        return [
            Route("/api/auth/auth_info", endpoint=self.auth_info, methods=["GET"]),
            Route("/api/auth/check_user", endpoint=self.check_user, methods=["POST"]),
            Route("/api/auth/login", endpoint=self.login, methods=["POST"]),
            Route("/api/auth/check_otp", endpoint=self.check_otp, methods=["POST"]),
            Route("/api/auth/set_passwd", endpoint=self.set_passwd, methods=["POST"]),
            Route(
                "/api/auth/recover_passwd",
                endpoint=self.recover_passwd,
                methods=["POST"],
            ),
            Route(
                "/api/auth/change_passwd", endpoint=self.change_passwd, methods=["POST"]
            ),
            Route("/api/auth/get_users", endpoint=self.get_users, methods=["POST"]),
            Route("/api/auth/register", endpoint=self.register, methods=["POST"]),
            Route("/api/auth/update_user", endpoint=self.update_user, methods=["POST"]),
            Route("/api/auth/reset_user", endpoint=self.reset_user, methods=["POST"]),
            Route(
                "/api/auth/suspend_user", endpoint=self.suspend_user, methods=["POST"]
            ),
            Route("/api/auth/delete_user", endpoint=self.delete_user, methods=["POST"]),
            Route("/api/auth/su", endpoint=self.su, methods=["POST"]),
            Route("/api/auth/change_org", endpoint=self.change_org, methods=["POST"]),
        ]

    async def startup(self):
        """ " Used by App to configure and startup the Auth service"""
        try:
            self.product = self.cfg["app"]["product"]
            self.auth_secret = self.cfg["rest"]["auth_secret"]
            self.allow_register = oget(self.cfg, ["rest", "allow_register"], False)
            self.strong_passwd = oget(self.cfg, ["rest", "strong_passwd"], False)
            self.otp_timeout = oget(self.cfg, ["rest", "otp_timeout"], False)
            self.otp_mode = oget(self.cfg, ["rest", "otp_mode"], False)
        except Exception as e:
            self.LOG(4, 0, label="AUTH", label2="startup", msg={"error_msg": str(e)})
            return True
        self.LOG(
            2,
            0,
            label="AUTH",
            label2="startup",
            msg=f"OK (connected to DB:{self.db.dbname})",
        )
        return False

    async def shutdown(self):
        """ " Used by App to shutdown the Auth service"""
        self.LOG(2, 0, label="AUTH", label2="shutdown", msg="OK")
        return False

    # ####################################################################################################
    # Internal methods (returns dict, not JSON)
    # ####################################################################################################

    async def check_auth(self, request):
        """
        Used by App routes to check for valid users.
        Assumes that the JWT token was correctly decripted and the user passed the first level of Authenticatio.
        Then reads the email from the payload and checks in the database a valid uid,email pair.
        Finnaly checks if the user is ACTIVE.
        If all checks return the user info as dict (not json, since it is an internal method).
        Itherwise raises 401 or 403 with the corresponding error in error_msg field.
        """
        label2 = "check_auth"
        if not hasattr(request.user, "display_name") or not hasattr(
            request.user, "payload"
        ):
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="Invalid JWT token",
                status_code=401,
            )
        uid, payload = request.user.display_name, request.user.payload
        user = await self.db.select_one("users", {"id": uid})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=401,
            )
        if user["email"] != payload["email"]:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="User email mistatch",
                status_code=401,
            )
        if user["ustatus"] != ACTIVE:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="User not active",
                status_code=403,
            )
        return get_user_info(user)

    async def get_email_from_uid(self, uid):
        """Returns email from DB based on uid."""
        user = await self.db.select_one("users", {"id": uid})
        return user["email"]

    # ####################################################################################################
    # REST methods for users: all to return json
    # ####################################################################################################

    async def auth_info(self, request):
        """Returns Auth infos to be used on front-end flow."""
        d = {
            "allow_register": self.allow_register,
            "strong_passwd": self.strong_passwd,
            "otp_timeout": self.otp_timeout,
            "otp_mode": self.otp_mode,
        }
        return self.ret(payload=d)

    async def check_user(self, request):
        """
        Checks if a user if able to login, searching its status by user email given as input.
        To be used before asking for password in the login process.
        Innitiates the OTP process if the User exists and Auth is not configured for self register.
        Returns auth_status and users_status, searching by user email.
        Possible auth_status returns: 'USER_OK', 'WAIT_SET_PASSWD'.
        Possible exception messages: 'USER_NOT_REGISTERED', 'USER_SUSPENDED'
        """
        label2 = "check_user"
        # Replace with: data = await get_request_json(request, LOG=self.LOG, label=label2)
        data = await request.json()
        [email] = enforce_required_args(self.LOG, data, ["email"], label="AUTH", label2=label2, as_list=True)
        user = await self.db.select_one("users", {"email": email})
        if user is None:
            log_and_raise_service(self.LOG, label="AUTH", label2=label2, msg=f"USER_NOT_REGISTERED: {email}",
                status_code=401)
        if user["ustatus"] == ACTIVE:
            increase(user, "logins")
            await self.db_update("users", "email", user, "check_user")
            return self.ret(auth_status="USER_OK")
        if user["ustatus"] == WAIT_SET_PASSWD:
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] == NOT_REGISTERED and not self.allow_register:
            await self.gen_otp(user)
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] in [
            SUSPENDED,
            SUSPENDED_LICENCE,
            SUSPENDED_FAILS,
            SUSPENDED_REQUESTS,
        ]:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_SUSPENDED",
                status_code=403,
            )
        log_and_raise_service(
            self.LOG, label="AUTH", label2=label2, msg="UNKNOWN STATUS", status_code=403
        )

    async def check_otp(self, request):
        """
        Checks if a user has inputed the correct OTP, using as inputs the user email and the otp.
        To be used before asking for password in the set password process.
        Checks for OTP timeout, resending the OTP if timeout period has passed.
        Checks for number of OTP failures, suspending the user if the number is over the limit.
        Returns auth_status and user status if user not in WAIT_SET_PASSWD status.
        Possible auth_status returns: 'SET_PASSWD_DONE', 'OTP_OK'
        Possible exception messages: 'OTP_ERROR', 'USER_SUSPENDED', 'WAIT_SET_PASSWD_TIMEOUT, 'WAIT_SET_PASSWD_SUSPENDED'
        """
        label2 = "check_otp"
        data = await request.json()
        [email, otp] = enforce_required_args(
            self.LOG, data, ["email", "otp"], label="AUTH", label2=label2, as_list=True
        )
        user = await self.db.select_one("users", {"email": email})
        if user is None:
            log_and_raise_service(self.LOG, label="AUTH", label2=label2, msg="User not found", status_code=403)
        if user["ustatus"] == ACTIVE:
            return self.ret(auth_status="SET_PASSWD_DONE", user_status=user["ustatus"])
        if user["ustatus"] in [
            SUSPENDED,
            SUSPENDED_LICENCE,
            SUSPENDED_FAILS,
            SUSPENDED_REQUESTS,
        ]:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_SUSPENDED",
                status_code=403,
            )
        if otp != user["otp"]:
            self.LOG(
                3, 0, label="AUTH", label2=label2, msg=f"OTP error: {user['email']}"
            )
            if await self.increase_fails(user, "OTP"):
                log_and_raise_service(
                    self.LOG,
                    label="AUTH",
                    label2=label2,
                    msg="WAIT_SET_PASSWD_SUSPENDED",
                    status_code=403,
                )
            log_and_raise_service(
                self.LOG, label="AUTH", label2=label2, msg="OTP_ERROR", status_code=403
            )
        delta = get_age_in_seconds(user["ts_passwd"])
        if delta > self.otp_timeout:
            await self.gen_otp(user)
            self.LOG(
                3,
                0,
                label="AUTH",
                label2=label2,
                msg=f"OTP expired: {user['email']} (delta={delta})",
            )
            log_and_raise_service(
                self.LOG, label="AUTH", msg="WAIT_SET_PASSWD_TIMEOUT", status_code=401
            )
        return self.ret(auth_status="OTP_OK")

    async def set_passwd(self, request):
        """
        Set a new user password if OTP and password strengh are valid.
        Possible auth_status returns: 'SET_PASSWD_OK', 'SET_PASSWD_DONE',
        Possible exception messages: 'OTP_ERROR', 'PASSWD_NOT_STRONG', 'WAIT_SET_PASSWD_TIMEOUT,
                                     'USER_SUSPENDED', 'WAIT_SET_PASSWD_SUSPENDED'
        """
        label2 = "set_passwd"
        data = await request.json()
        [email, otp, passwd] = enforce_required_args(
            self.LOG,
            data,
            ["email", "otp", "passwd"],
            label="AUTH",
            label2=label2,
            as_list=True,
        )
        user = await self.db.select_one("users", {"email": email})
        if user is None:
            log_and_raise_service(self.LOG, label="AUTH", label2=label2, msg="USER_NOT_REGISTERED", status_code=403)
        if user["ustatus"] == ACTIVE:
            return self.ret(auth_status="SET_PASSWD_DONE")
        if user["ustatus"] in [
            SUSPENDED,
            SUSPENDED_LICENCE,
            SUSPENDED_FAILS,
            SUSPENDED_REQUESTS,
        ]:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_SUSPENDED",
                status_code=403,
            )
        if otp != user["otp"]:
            self.LOG(
                3, 0, label="AUTH", label2=label2, msg=f"OTP error: {user['email']}"
            )
            if await self.increase_fails(user, "OTP"):
                log_and_raise_service(
                    self.LOG,
                    label="AUTH",
                    label2=label2,
                    msg="WAIT_SET_PASSWD_SUSPENDED",
                    status_code=403,
                )
            log_and_raise_service(
                self.LOG, label="AUTH", label2=label2, msg="OTP_ERROR", status_code=403
            )
        delta = get_age_in_seconds(user["ts_passwd"])
        if delta > self.otp_timeout:
            self.LOG(
                3,
                0,
                label="AUTH",
                label2=label2,
                msg=f"OTP expired: {user['email']} (delta={delta})",
            )
            await self.gen_otp(user)
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="WAIT_SET_PASSWD_TIMEOUT",
                status_code=403,
            )
        if not check_passwd_strengh(passwd):
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="PASSWD_NOT_STRONG",
                status_code=403,
            )
        hashed = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        user["passwd"], user["ts_passwd"], user["otp"], user["ustatus"] = (
            hashed.decode(),
            datetime.now(timezone.utc),
            "",
            ACTIVE,
        )
        increase(user, "logins")
        await self.db_update("users", "email", user, "set_passwd")
        jwt_token = mk_jwt_token(user["id"], user["email"], self.auth_secret)
        return self.ret(
            auth_status="SET_PASSWD_OK",
            payload={"jwt_token": jwt_token, "user_info": get_user_info(user)},
        )

    async def login(self, request):
        """
        Inputs are the email and passwd.
        Performs the user login returning auth_status and jwt_token and user_info if successfull.
        Checks if the user is pre-registered and controls number of failures.
        Possible auth_status returns: 'AUTHORIZED', 'WAIT_SET_PASSWD'
        Possible exception messages: 'WRONG_PASSWD', 'USER_SUSPENDED', 'USER_NOT_REGISTERED'
        """
        label2 = "login"
        data = await request.json()
        [email, passwd] = enforce_required_args(
            self.LOG,
            data,
            ["email", "passwd"],
            label="AUTH",
            label2=label2,
            as_list=True,
        )
        user = await self.db.select_one("users", {"email": email})
        if user is None:
            self.LOG(
                3, 0, label="AUTH", label2=label2, msg=f"User not registered: {email}"
            )
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=401,
            )
        if user["ustatus"] == WAIT_SET_PASSWD:
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] == NOT_REGISTERED and not self.allow_register:
            await self.gen_otp(user)
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] != ACTIVE:
            self.LOG(
                3,
                0,
                label="AUTH",
                label2=label2,
                msg=f"User not active: {user['email']}",
            )
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_SUSPENDED",
                status_code=403,
            )
        if not bcrypt.checkpw(passwd.encode(), user["passwd"].encode()):
            self.LOG(
                3,
                0,
                label="AUTH",
                label2=label2,
                msg=f"WRONG PASSWORD: {user['email']}",
            )
            if await self.increase_fails(user, "LOGIN"):
                self.LOG(
                    3,
                    0,
                    label="AUTH",
                    label2=label2,
                    msg=f"Too many LOGIN FAILS: {user['email']} - USER SUSPENDED",
                )
                log_and_raise_service(
                    self.LOG,
                    label="AUTH",
                    label2=label2,
                    msg="USER_SUSPENDED",
                    status_code=403,
                )
            self.LOG(
                3, 0, label="AUTH", label2=label2, msg=f"LOGIN FAIL: {user['email']}"
            )
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="WRONG_PASSWD",
                status_code=403,
            )
        jwt_token = mk_jwt_token(user["id"], email, self.auth_secret)
        increase(user, "logins", True)
        user["fails"] = 0
        await self.db_update("users", "email", user, "login")
        return self.ret(
            auth_status="AUTHORIZED",
            payload={"jwt_token": jwt_token, "user_info": get_user_info(user)},
        )

    async def recover_passwd(self, request):
        """
        Set user mode in WAIT_SET_PASSWD and send new OTP
        Possible auth_status returns: 'WAIT_SET_PASSWD'
        Possible exception messages: 'USER_NOT_ACTIVE'
        """
        label2 = "recover_passwd"
        data = await request.json()
        [email] = enforce_required_args(
            self.LOG, data, ["email"], label="AUTH", label2=label2, as_list=True
        )
        user = await self.enforce_find_user({"email": email}, label2=label2)
        if user["ustatus"] == WAIT_SET_PASSWD:
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] != ACTIVE:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_ACTIVE",
                status_code=403,
            )
        user["ustatus"] = WAIT_SET_PASSWD
        await self.db_update("users", "email", user, label2)
        await self.gen_otp(user)
        return self.ret(auth_status="WAIT_SET_PASSWD")

    async def change_passwd(self, request):
        """
        Changes a logged in user password.
        User header must be valid (user must be active),
        Possible auth_status returns: 'CHANGE_PASSWD_OK', 'WAIT_SET_PASSWD'
        Possible exception messages: 'WRONG_PASSWD', 'USER_NOT_ACTIVE', 'PASSWD_NOT_STRONG', 'USER_SUSPENDED'
        """
        label2 = "change_passwd"
        user = await self.enforce_find_user(
            {"id": request.user.display_name}, label2=label2
        )
        if user["ustatus"] == WAIT_SET_PASSWD:
            return self.ret(auth_status="WAIT_SET_PASSWD")
        if user["ustatus"] != ACTIVE:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_ACTIVE",
                status_code=403,
            )
        data = await request.json()
        [passwd, new_passwd] = enforce_required_args(
            self.LOG,
            data,
            ["passwd", "new_passwd"],
            label="AUTH",
            label2=label2,
            as_list=True,
        )
        if not check_passwd_strengh(new_passwd):
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="PASSWD_NOT_STRONG",
                status_code=403,
            )
        if not bcrypt.checkpw(passwd.encode(), user["passwd"].encode()):
            self.LOG(
                3,
                0,
                label="AUTH",
                label2=label2,
                msg=f"WRONG PASSWORD: {user['email']}",
            )
            if await self.increase_fails(user, "LOGIN"):
                self.LOG(
                    3,
                    0,
                    label="AUTH",
                    label2=label2,
                    msg=f"Too many LOGIN FAILS: {user['email']} - USER SUSPENDED",
                )
                log_and_raise_service(
                    self.LOG,
                    label="AUTH",
                    label2=label2,
                    msg="USER_SUSPENDED",
                    status_code=403,
                )
            self.LOG(
                3, 0, label="AUTH", label2=label2, msg=f"LOGIN FAIL: {user['email']}"
            )
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="WRONG_PASSWD",
                status_code=403,
            )
        hashed = bcrypt.hashpw(new_passwd.encode(), bcrypt.gensalt())
        user["passwd"], user["otp"], user["ustatus"] = hashed.decode(), "", ACTIVE
        await self.db_update("users", "email", user, "change_passwd")
        return self.ret(auth_status="CHANGE_PASSWD_OK")

    async def register(self, request):
        """
        Registers a new user, either in self register mode or admin pre-register
        Possible auth_status returns: 'REGISTER_OK', 'WAIT_SET_PASSWD'
        Possible exception messages: 'USER_ALREADY_REGISTERED'
        """
        label2 = "register"
        data = await request.json()
        [email, org] = enforce_required_args(
            self.LOG, data, ["email", "org"], label="AUTH", label2=label2, as_list=True
        )
        if type(org) == dict:
            org = oget(org, ["id"])
        user2 = {
            "email": email,
            "role": "user",
            "org": org,
            "name": oget(data,['name']),
            "short": oget(data,['short']),
            "ts_insert": datetime.now(timezone.utc),
            "logins": 0,
            "fails": 0,
            "requests": 0,
        }
        user = await self.db.select_one("users", {"email": email})
        # Self registration
        if self.allow_register:
            if user is not None:
                log_and_raise_service(
                    self.LOG,
                    label="AUTH",
                    label2=label2,
                    msg="USER_ALREADY_REGISTERED",
                    status_code=401,
                )
            user2["ustatus"] = WAIT_SET_PASSWD
            # rec_to_row
            await self.db.insert("users", user2)
            await self.gen_otp(user)
            return self.ret(auth_status="WAIT_SET_PASSWD")
        # Registration of new user by admin or su
        await self.enforce_admin_perm(request, label2=label2, requires_su=True)
        if user is not None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_ALREADY_REGISTERED",
                status_code=401,
            )
        user2["ustatus"] = NOT_REGISTERED
        # rec_to_row
        await self.db.insert("users", user2)
        return self.ret(auth_status="REGISTER_OK")

    # ####################################################################################################
    # REST methods for admin: all to return json
    # ####################################################################################################

    async def get_users(self, request):
        """Get all users, possibly filtered by filters."""
        label2 = "get_users"
        data = await request.json()
        role, org = await self.enforce_admin_perm(request, label2=label2)
        data = await request.json()
        QARGS = ["cols", "filters", "sfilters", "sort", "ascending", "offset", "limit"]
        kwargs = {k: data[k] for k in data if k in QARGS}
        filters = kwargs["filters"] if "filters" in kwargs and kwargs["filters"] is not None else []
        if role == "admin": filters.append({"col": "org", "val": org})
        kwargs["filters"] = filters
        # res = await self.db.select('users', **kwargs)
        res = await self.db.select("users", lookups=[{"col": "org", "tbl": "orgs"}], **kwargs)
        res_to_recs(res, ["org"])
        if res is None or not "data" in res or not "nrows" in res:
            log_and_raise_service(self.LOG, label="AUTH", label2=label2, msg="DB access error")
        return rest_ok({"data": res["data"], "nrows": res["nrows"]})

    async def update_user(self, request):
        """Update user data."""
        label2 = "update_user"
        role, org = await self.enforce_admin_perm(request, label2=label2)
        data = await request.json()
        rec = rec_to_row(data)
        user = await self.db.select_one("users", {"id": rec["id"]})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=400,
            )
        if role == "admin" and user["org"] != org:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="NOT_AUTHORIZED",
                status_code=403,
            )
        # email update not allowed
        if "email" in rec:
            del rec["email"]
        await self.db_update("users", "id", rec, label2)
        return rest_ok()

    async def reset_user(self, request):
        """Reset user to SET_NEW_PASSWORD mode and reset fails."""
        label2 = "reset_user"
        role, org = await self.enforce_admin_perm(request, label2=label2)
        data = await request.json()
        rec = rec_to_row(data)
        user = await self.db.select_one("users", {"id": rec["id"]})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=400,
            )
        if role == "admin" and user["org"] != org:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="NOT_AUTHORIZED",
                status_code=403,
            )
        user["ustatus"], user["fails"], user["otp"] = 0, 0, None
        await self.db_update("users", "id", user, label2)
        return rest_ok()

    async def suspend_user(self, request):
        """Suspend a user changing ustatus to SUSPENDED or to SUSPENDED_LICENCE if rec['ustatus']==SUSPENDED_LICENCE."""
        label2 = "suspend_user"
        role, org = await self.enforce_admin_perm(request, label2=label2)
        data = await request.json()
        rec = rec_to_row(data)
        user = await self.db.select_one("users", {"id": rec["id"]})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=400,
            )
        if role == "admin" and user["org"] != org:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="NOT_AUTHORIZED",
                status_code=403,
            )
        ustatus = (
            int(rec["ustatus"])
            if "ustatus" in rec and int(rec["ustatus"]) == SUSPENDED_LICENCE
            else SUSPENDED
        )
        user["ustatus"] = ustatus
        await self.db_update("users", "id", user, label2)
        return rest_ok()

    async def delete_user(self, request):
        """Delete a user from DB."""
        label2 = "delete_user"
        role, org = await self.enforce_admin_perm(request, label2=label2)
        data = await request.json()
        rec = rec_to_row(data)
        user = await self.db.select_one("users", {"id": rec["id"]})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=400,
            )
        if role == "admin" and user["org"] != org:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="NOT_AUTHORIZED",
                status_code=403,
            )
        await self.db.delete("users", "id", rec["id"])
        return rest_ok()

    # ####################################################################################################
    # REST methods for su in debug mode
    # ####################################################################################################

    async def su(self, request):
        """Switch uid."""
        label2 = "su"
        _, _ = await self.enforce_admin_perm(request, label2=label2, requires_su=True)
        data = await request.json()
        [uid] = enforce_required_args(
            self.LOG, data, ["uid"], label="AUTH", label2=label2, as_list=True
        )
        user = await self.enforce_find_user({"id": uid}, label2=label2)
        jwt_token = mk_jwt_token(user["id"], user["email"], self.auth_secret)
        return rest_ok({"jwt_token": jwt_token, "user_info": get_user_info(user)})

    async def change_org(self, request):
        """Change su org."""
        label2 = "change_org"
        _, _ = await self.enforce_admin_perm(request, label2=label2, requires_su=True)
        user = await self.db.select_one("users", {"id": request.user.display_name})
        if user is None:
            log_and_raise_service(
                self.LOG,
                label="AUTH",
                label2=label2,
                msg="USER_NOT_REGISTERED",
                status_code=400,
            )
        data = await request.json()
        user["org"] = data["org"]
        jwt_token = mk_jwt_token(user["id"], user["email"], self.auth_secret)
        _ = await self.db.update("users", "id", user)
        return rest_ok({"jwt_token": jwt_token, "user_info": get_user_info(user)})
