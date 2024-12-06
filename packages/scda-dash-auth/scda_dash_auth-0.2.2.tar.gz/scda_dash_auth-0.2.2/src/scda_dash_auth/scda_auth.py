import logging
import os
import re
from typing import Optional, Tuple, Union
from urllib.parse import urlencode, urljoin

import dash
import dash_auth
import dash_auth.auth
import requests
from flask import Response, flash, redirect, request, session


class SCDAAuth(dash_auth.auth.Auth):
    """Implements auth via SCDA/QDT OpenID."""

    def __init__(
        self,
        app: dash.Dash,
        app_name: str,
        secret_key: str,
        auth_url: str,
        login_route: str = "/login",
        logout_route: str = "/logout",
        callback_route: str = "/callback",
        log_signin: bool = False,
        public_routes: Optional[list] = None,
        logout_page: Union[str, Response] = None,
        secure_session: bool = False,
    ):
        """
        Secure a Dash app through SCDA/QDT Auth service.

        Parameters
        ----------
        app : dash.Dash
            Dash app to secure
        app_name : str
            Name of the app registered in the SCDA/QDT Auth service
        secret_key : str
            Secret key used to sign the session for the app
        auth_url : str
            URL to the SCDA/QDT Auth service
        login_route : str, optional
            Route to login, by default "/login"
        logout_route : str, optional
            Route to logout, by default "/logout"
        callback_route : str, optional
            Route to callback for the current service. By default "/callback"
        log_signin : bool, optional
            Log sign-ins, by default False
        public_routes : Optional[list], optional
            List of public routes, by default None
        logout_page : Union[str, Response], optional
            Page to redirect to after logout, by default None
        secure_session : bool, optional
            Whether to ensure the session is secure, setting the flasck config
            SESSION_COOKIE_SECURE and SESSION_COOKIE_HTTPONLY to True,
            by default False

        """
        # NOTE: The public routes should be passed in the constructor of the Auth
        # but because these are static values, they are set here as defaults.
        # This is only temporal until a better solution is found. For now it
        # works.
        if public_routes is None:
            public_routes = []

        public_routes.extend(["/scda_login", "/scda_logout", "/callback"])

        super().__init__(app, public_routes = public_routes)

        self.app_name = app_name
        self.auth_url = auth_url
        self.login_route = login_route
        self.logout_route = logout_route
        self.callback_route = callback_route
        self.log_signin = log_signin
        self.logout_page = logout_page

        if not self.__app_name_registered():
            raise RuntimeError(
                f"App name {app_name} is not registered in the auth service. "
                f"Please register it at {self.auth_url}/register/apps"
            )

        if secret_key is not None:
            app.server.secret_key = secret_key

        if app.server.secret_key is None:
            raise RuntimeError(
                """
                app.server.secret_key is missing.
                Generate a secret key in your Python session
                with the following commands:
                >>> import os
                >>> import base64
                >>> base64.b64encode(os.urandom(30)).decode('utf-8')
                and assign it to the property app.server.secret_key
                (where app is your dash app instance), or pass is as
                the secret_key argument to SCDAAuth.__init__.
                Note that you should not do this dynamically:
                you should create a key and then assign the value of
                that key in your code/via a secret.
                """
            )
        if secure_session:
            app.server.config["SESSION_COOKIE_SECURE"] = True
            app.server.config["SESSION_COOKIE_HTTPONLY"] = True

        app.server.add_url_rule(
            login_route,
            endpoint = "scda_login",
            view_func = self.login_request,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            logout_route,
            endpoint = "scda_logout",
            view_func = self.logout,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            callback_route,
            endpoint = "callback",
            view_func = self.callback,
            methods = ["GET"],
        )

    def is_authorized(self) -> bool:
        authorized = False

        if "user" in session:
            authorized = True
            return authorized

        access_token_cookie = request.cookies.get("access_token", None)
        access_token_header = request.headers.get("Authorization", None)

        if not access_token_cookie:
            if not access_token_header:
                return authorized
            else:
                access_token = re.sub("Bearer ", "", access_token_header)
        else:
            access_token = access_token_cookie

        try:
            logged_in, token_payload = self.verify_token(access_token)
        except Exception as e:
            logging.exception(f"Error verifying token: {e}")
            return False

        if logged_in:
            try:
                authorized = self.check_user_authorization(
                    token_payload["user_info"]["id"], access_token
                )
                if not authorized:
                    session['needs_registration'] = True
                    flash(
                        "User is not authorized to access the app. "
                        "Please request access to the app in the SCDA/QDT Auth service."
                    )
                    return False
            except Exception as e:
                if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
                    flash(
                        "User not registered in the SCDA/QDT Auth service. "
                        "Please register the user in the SCDA/QDT Auth service."
                    )
                    return False
                elif isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 500:
                    flash(
                        "Internal server error when verifying user authorization. "
                        "Please try again later or contact the administrator."
                    )
                    return False
                else:
                    flash("Error checking user authorization, most likely due to permission issues.")
                    return False
            try:
                session["user"] = token_payload["user_info"]
            except RuntimeError:
                logging.warning("Session is unavailable. Cannot store user info.")

        return authorized

    def verify_token(self, token: str) -> Tuple[bool, dict]:
        try:
            response = requests.post(
                self.auth_url + "/verify_token",
                json = {
                    "access_token": token,
                    "token_type": "bearer",
                }
            )
            response.raise_for_status()
            is_verified = response.json()["is_verified"]
            return is_verified, response.json()["token_payload"]
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error verifying token: {e}")
            return False, None

    def registration_request(self) -> Response:
        registration_url = urljoin(self.auth_url, "/register/user")
        query_params = urlencode({'app': self.app_name})
        full_url = f"{registration_url}?{query_params}"
        return redirect(full_url)

    def login_request(self) -> Response:
        if session.get("needs_registration", False):
            session.pop("needs_registration")
            return self.registration_request()

        next_url = request.url_root
        auth_url_with_next = urljoin(self.auth_url, '/login')
        query_params = urlencode({'next': next_url})
        full_url = f"{auth_url_with_next}?{query_params}"
        return redirect(full_url)

    def logout(self):
        session.clear()
        base_url = self.app.config.get("url_base_pathname") or "/"
        page = self.logout_page or f"""
        <div style="display: flex; flex-direction: column;
        gap: 0.75rem; padding: 3rem 5rem;">
            <div>Logged out successfully</div>
            <div><a href="{base_url}">Go back</a></div>
        </div>
        """
        return page

    def callback(self):
        token = request.args.get("token")
        next_url = request.args.get("next", self.app.config["routes_pathname_prefix"])

        if not token:
            logging.error("No token received in callback.")
            return redirect(self.login_request())

        response = redirect(next_url)
        response.set_cookie(
            "access_token",
            token,
            httponly = True,
            max_age = 60 * 60 * 24 * 7,
            domain = None,
            path = "/",
        )

        return response

    def __app_name_registered(self) -> bool:
        url_app_path = f"/apps/name/{self.app_name}"
        url = urljoin(self.auth_url, url_app_path)
        try:
            response = requests.get(url)
            response.raise_for_status()
            app = response.json()
            return self.app_name == app.get("name")
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
                logging.exception(
                    f"App name {self.app_name} not registered in auth service. "
                    f"Did you register it? You can request a registration at {self.auth_url}/register/apps"
                )
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 500:
                logging.exception(
                    f"Internal server error when verifying app name. "
                    f"Please try again later or contact the administrator."
                )
                raise
            logging.exception(f"Unexpected error when verifying app name: {e}")

            return False

    def check_user_authorization(self, user_id: str, access_token: str) -> bool:
        url = urljoin(self.auth_url, f"/users/{user_id}/apps")
        try:
            response = requests.get(url, headers = {"Authorization": f"Bearer {access_token}"})
            response.raise_for_status()
            response_json = response.json()

            if self.app_name in [
                _app['name'] for _app in response_json.get('data', [])
            ]:
                return True
            else:
                logging.warning(
                    f"User {user_id} is not authorized to access the app {self.app_name}. "
                    f"Please request access to the app in the SCDA/QDT Auth service."
                )
                return False

        except requests.exceptions.RequestException as e:
            if e.response.status_code == 404:
                logging.exception(
                    f"User {user_id} is not registered in the auth service. "
                    f"Please register the user in the SCDA/QDT Auth service."
                )
            elif e.response.status_code == 500:
                logging.exception(
                    "Internal server error when verifying user authorization. "
                    "Please try again later or contact the administrator."
                )
            else:
                logging.exception(f"Error checking user authorization: {e}")

            raise

    def check_current_user_authorization(self) -> bool:
        """
        Check if the current user is authorized to access the app. This method
        expects the user to be logged in and the user info to be stored in the
        session.
        """
        url = urljoin(self.auth_url, "/users/me/apps")
        try:
            access_token = request.cookies.get("access_token", None)
            response = requests.get(url, headers = {"Authorization": f"Bearer {access_token}"})
            response.raise_for_status()
            return response.json().get("is_authorized", False)
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error checking user authorization: {e}")
            return False
