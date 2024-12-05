# © Copyright 2024 Hewlett Packard Enterprise Development LP
import argparse
import contextlib
import functools
import getpass
import hashlib
import json
import pathlib
import urllib.parse
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
    cast,
)

import filelock
import requests

import aioli.common.api.errors
import aiolirest
from aioli import cli
from aioli.common import api, util
from aioli.common.api import certs

Credentials = NamedTuple("Credentials", [("username", str), ("password", str)])

PASSWORD_SALT = "GubPEmmotfiK9TMD6Zdw"


def salt_and_hash(password: str) -> str:
    if password:
        return hashlib.sha512((PASSWORD_SALT + password).encode()).hexdigest()
    else:
        return password


class UsernameTokenPair:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token


def default_load_user_password(
    requested_user: Optional[str],
    password: Optional[str],
    token_store: "TokenStore",
) -> Tuple[Optional[str], Optional[str]]:
    # Always prefer an explicitly provided user/password.
    if requested_user:
        return requested_user, password

    # Next highest priority is user/password from environment.
    # Watch out! We have to check for AIOLI_USER and AIOLI_PASS, because containers will
    # have AIOLI_USER set, but that doesn't overrule the active user in the TokenStore, because
    # if the TokenStore in the container has an active user, that means the user has explicitly
    # ran `aioli user login` inside the container.
    if (
        util.get_aioli_username_from_env() is not None
        and util.get_aioli_password_from_env() is not None
    ):
        return util.get_aioli_username_from_env(), util.get_aioli_password_from_env()

    # Last priority is the active user in the token store.
    return token_store.get_active_user(), password


def get_rest_config(host: str) -> aiolirest.Configuration:
    cert = certs.get_cert_path()
    if cert is not None and cert is not False:
        config = aiolirest.Configuration(host=host, ssl_ca_cert=cert)
    else:
        config = aiolirest.Configuration(host=host)

    if cert is False:
        config.verify_ssl = False

    url_parsed = urllib.parse.urlparse(host)
    proxies = requests.utils.getproxies()  # type: ignore[attr-defined]
    proxy_url = proxies.get("https") if host.startswith("https") else proxies.get("http", None)
    if proxy_url is not None:
        if not requests.utils.proxy_bypass(url_parsed.netloc):  # type: ignore[attr-defined]
            config.proxy = proxy_url

    return config


class Authentication:
    def __init__(
        self,
        master_address: Optional[str] = None,
        requested_user: Optional[str] = None,
        password: Optional[str] = None,
        cert: Optional[certs.Cert] = None,
    ) -> None:
        self.master_address = master_address or util.get_default_controller_address()
        self.token_store = TokenStore(self.master_address)

        self.session = self._init_session(requested_user, password, cert)

    def _init_session(
        self,
        requested_user: Optional[str],
        password: Optional[str],
        cert: Optional[certs.Cert],
    ) -> UsernameTokenPair:
        # Get session_user and password given the following priority:
        # 1. User passed in with flag (requested_user)
        # 2. User from environment if AIOLI_PASS is set.
        # 3. Active user from the token store.
        session_user, password = default_load_user_password(
            requested_user, password, self.token_store
        )

        if session_user is None:
            raise aioli.common.api.errors.UnauthenticatedException(username="")

        # Check the token store if this session_user has a cached token. If so, check with the
        # master to verify it has not expired. Otherwise, let the token be None.
        token = self.token_store.get_token(session_user)
        if token is not None and not _is_token_valid(self.master_address, token, cert):
            self.token_store.drop_user(session_user)
            token = None

        # Special case: use token provided from the container environment if:
        # - No token was obtained from the token store already,
        # - There is a token available from the container environment, and
        # - No user was explicitly requested, or the requested user matches the token available
        #   in the container environment.
        if (
            token is None
            and util.get_aioli_username_from_env() is not None
            and util.get_aioli_user_token_from_env() is not None
            and requested_user in (None, util.get_aioli_username_from_env())
        ):
            session_user = util.get_aioli_username_from_env()
            assert session_user
            token = util.get_aioli_user_token_from_env()

        if token is not None:
            return UsernameTokenPair(session_user, token)

        if password is None:
            password = getpass.getpass("Password for user '{}': ".format(session_user))

        try:
            token = do_login(self.master_address, session_user, salt_and_hash(password), True, cert)
        except api.errors.ForbiddenException:
            raise

        self.token_store.set_token(session_user, token)

        return UsernameTokenPair(session_user, token)

    def is_user_active(self, username: str) -> bool:
        return self.token_store.get_active_user() == username

    def get_session_user(self) -> str:
        """
        Returns the session user for the current session. If there is no active
        session, then an UnauthenticatedException will be raised.
        """
        return self.session.username

    def get_session_token(self, must: bool = True) -> str:
        """
        Returns the authentication token for the session user. If there is no
        active session, then an UnauthenticatedException will be raised.
        """
        if self.session is None:
            if must:
                raise api.errors.UnauthenticatedException(username="")
            else:
                return ""
        return self.session.token


def do_login(
    controller_address: str,
    username: str,
    password: str,
    isHashed: bool,
    cert: Optional[certs.Cert] = None,
) -> str:
    host: str = controller_address
    host = util.prepend_protocol(host)

    client = aiolirest.ApiClient(get_rest_config(host))
    request = aiolirest.LoginRequest(username=username, password=password, isHashed=isHashed)
    response = aiolirest.AuthenticationApi(client).login_post(request=request)

    token = response.token

    return str(token)


class LogoutAuthentication(Authentication):
    """
    An api-compatible Authentication object that is basically exactly a UserTokenPair.

    TODO(MLG-215): delete Authentication class and write a function that returns a UsernameTokenPair
    in its place, and let do_request() take UsernameTokenPair as input.
    """

    def __init__(self, session_user: str, session_token: str) -> None:
        self.session_user = session_user
        self.session_token = session_token

    def get_session_user(self) -> str:
        return self.session_user

    def get_session_token(self, must: bool = True) -> str:
        return self.session_token


def logout(
    controller_address: Optional[str],
    requested_user: Optional[str],
    cert: Optional[certs.Cert],
) -> None:
    """
    Logout if there is an active session for this master/username pair, otherwise do nothing.

    Additionally, if the user happens to be the active user, drop the active user from the
    TokenStore.
    """

    controller_address = controller_address or util.get_default_controller_address()
    token_store = TokenStore(controller_address)

    session_user, _ = default_load_user_password(requested_user, None, token_store)

    if session_user is None:
        return

    if session_user == token_store.get_active_user():
        token_store.clear_active()

    session_token = token_store.get_token(session_user)

    if session_token is None:
        return

    token_store.drop_user(session_user)

    null_namespace = argparse.Namespace()

    with cli.setup_session(args=null_namespace, controller=controller_address) as session:
        api_instance = aiolirest.AuthenticationApi(session)
        api_instance.logout_post()


def logout_all(master_address: Optional[str], cert: Optional[certs.Cert]) -> None:
    master_address = master_address or util.get_default_controller_address()
    token_store = TokenStore(master_address)

    users = token_store.get_all_users()

    for user in users:
        logout(master_address, user, cert)

    token_store.clear_active()


def _is_token_valid(controller_address: str, token: str, cert: Optional[certs.Cert]) -> bool:
    """
    Find out whether the given token is valid by attempting to use it
    on the "api/v1/me" endpoint.
    """
    host: str = controller_address
    host = util.prepend_protocol(host)

    configuration = get_rest_config(host)
    configuration.api_key["ApiKeyAuth"] = "Bearer " + token
    client = aiolirest.ApiClient(configuration)
    users_api = aiolirest.UsersApi(client)

    try:
        users_api.users_me_get()
    except (api.errors.UnauthenticatedException, api.errors.APIException):
        return False
    return True


class TokenStore:
    """
    TokenStore is a class for reading/updating a persistent store of user authentication tokens.
    TokenStore can remember tokens for many users for each of many masters.  It can also remembers
    one "active user" for each master, which is set via `aioli user login`.

    All updates to the file follow a read-modify-write pattern, and use file locks to protect the
    integrity of the underlying file cache.
    """

    def __init__(self, master_address: str, path: Optional[pathlib.Path] = None) -> None:
        self.master_address = master_address
        self.path = path or util.get_config_path().joinpath("auth.json")
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # Decide on paths for a lock file and a temp files (during writing)
        self.temp = pathlib.Path(str(self.path) + ".temp")
        self.lock = str(self.path) + ".lock"

        with filelock.FileLock(self.lock):
            store = self._load_store_file()

        self._reconfigure_from_store(store)

    def _reconfigure_from_store(self, store: dict) -> None:
        substore = store.get("masters", {}).get(self.master_address, {})
        self._active_user = cast(str, substore.get("active_user"))
        self._tokens = cast(Dict[str, str], substore.get("tokens", {}))

    def get_active_user(self) -> Optional[str]:
        return self._active_user

    def get_all_users(self) -> List[str]:
        return list(self._tokens)

    def get_token(self, user: str) -> Optional[str]:
        token = self._tokens.get(user)
        if token is not None:
            assert isinstance(token, str), "invalid cache; token must be a string"
        return token

    def delete_token_cache(self) -> None:
        with filelock.FileLock(self.lock):
            if self.path.exists():
                self.path.unlink()

    def drop_user(self, username: str) -> None:
        with self._persistent_store() as substore:
            tokens = substore.setdefault("tokens", {})
            if username in tokens:
                del tokens[username]

    def set_token(self, username: str, token: str) -> None:
        with self._persistent_store() as substore:
            tokens = substore.setdefault("tokens", {})
            tokens[username] = token

    def set_active(self, username: str) -> None:
        with self._persistent_store() as substore:
            tokens = substore.setdefault("tokens", {})
            if username not in tokens:
                raise api.errors.UnauthenticatedException(username=username)
            substore["active_user"] = username

    def clear_active(self) -> None:
        with self._persistent_store() as substore:
            substore.pop("active_user", None)

    @contextlib.contextmanager
    def _persistent_store(self) -> Iterator[Dict[str, Any]]:
        """
        Yields the appropriate store[self.master_address] that can be modified, and the modified
        result will be written back to file.

        Whatever updates are made will also be updated on self automatically.
        """
        with filelock.FileLock(self.lock):
            store = self._load_store_file()
            substore = store.setdefault("masters", {}).setdefault(self.master_address, {})

            # No need for try/finally, because we don't update the file after failures.
            yield substore

            # Reconfigure our cached variables.
            self._reconfigure_from_store(store)

            with self.temp.open("w") as f:
                json.dump(store, f, indent=4, sort_keys=True)
            self.temp.replace(self.path)

    def _load_store_file(self) -> Dict[str, Any]:
        """
        Read a token store from a file, shimming it to the most recent version if necessary.

        If a v0 store is found it will be reconfigured as a v1 store based on the master_address
        that is being currently requested.
        """
        try:
            if not self.path.exists():
                return {"version": 1}

            try:
                with self.path.open() as f:
                    store = json.load(f)
            except json.JSONDecodeError:
                raise api.errors.CorruptTokenCacheException()

            if not isinstance(store, dict):
                raise api.errors.CorruptTokenCacheException()

            version = store.get("version", 0)
            if version == 0:
                validate_token_store_v0(store)
                store = shim_store_v0(store, self.master_address)

            validate_token_store_v1(store)

            return cast(dict, store)

        except api.errors.CorruptTokenCacheException:
            # Delete invalid caches before exiting.
            self.path.unlink()
            raise


def shim_store_v0(v0: Dict[str, Any], master_address: str) -> Dict[str, Any]:
    """
    v1 schema is just a bit more nesting to support multiple masters.
    """
    v1 = {"version": 1, "masters": {master_address: v0}}
    return v1


def validate_token_store_v0(store: Any) -> bool:
    """
    Valid v0 schema example:

        {
          "active_user": "user_a",
          "tokens": {
            "user_a": "TOKEN",
            "user_b": "TOKEN"
          }
        }
    """

    if not isinstance(store, dict):
        raise api.errors.CorruptTokenCacheException()

    if len(set(store.keys()).difference({"active_user", "tokens"})) > 0:
        # Extra keys.
        raise api.errors.CorruptTokenCacheException()

    if "active_user" in store:
        if not isinstance(store["active_user"], str):
            raise api.errors.CorruptTokenCacheException()

    if "tokens" in store:
        tokens = store["tokens"]
        if not isinstance(tokens, dict):
            raise api.errors.CorruptTokenCacheException()
        for k, v in tokens.items():
            if not isinstance(k, str):
                raise api.errors.CorruptTokenCacheException()
            if not isinstance(v, str):
                raise api.errors.CorruptTokenCacheException()
    return True


def validate_token_store_v1(store: Any) -> bool:
    """
    Valid v1 schema example:

        {
          "version": 1,
          "masters": {
            "master_url_a": {
              "active_user": "user_a",
              "tokens": {
                "user_a": "TOKEN",
                "user_b": "TOKEN"
              }
            },
            "master_url_b": {
              "active_user": "user_c",
              "tokens": {
                "user_c": "TOKEN",
                "user_d": "TOKEN"
              }
            }
          }
        }

    Note that store["masters"] is a mapping of string url's to valid v0 schemas.
    """
    if not isinstance(store, dict):
        raise api.errors.CorruptTokenCacheException()

    if len(set(store.keys()).difference({"version", "masters"})) > 0:
        # Extra keys.
        raise api.errors.CorruptTokenCacheException()

    # Handle version.
    version = store.get("version")
    if version != 1:
        raise api.errors.CorruptTokenCacheException()

    if "masters" in store:
        masters = store["masters"]
        if not isinstance(masters, dict):
            raise api.errors.CorruptTokenCacheException()

        # Each entry of masters must be a master_url/substore pair.
        for key, val in masters.items():
            if not isinstance(key, str):
                raise api.errors.CorruptTokenCacheException()
            validate_token_store_v0(val)

    return True


# cli_auth is the process-wide authentication used for api calls originating from the cli.
cli_auth = None  # type: Optional[Authentication]


def required(func: Callable[[argparse.Namespace], Any]) -> Callable[..., Any]:
    """
    A decorator for cli functions.
    """

    @functools.wraps(func)
    def f(namespace: argparse.Namespace) -> Any:
        update_cli_auth(namespace)
        return func(namespace)

    return f


def must_cli_auth() -> Authentication:
    if not cli_auth:
        raise api.errors.UnauthenticatedException(username="")
    return cli_auth


def update_cli_auth(namespace: argparse.Namespace) -> None:
    global cli_auth
    cli_auth = Authentication(namespace.controller, namespace.user)
