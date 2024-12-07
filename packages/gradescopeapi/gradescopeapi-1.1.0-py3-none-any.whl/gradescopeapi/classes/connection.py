import requests

from gradescopeapi.classes._helpers._login_helpers import (
    get_auth_token_init_gradescope_session,
    login_set_session_cookies,
)

from gradescopeapi.classes.account import Account


class GSConnection:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.account = None

    def login(self, email, password):
        # go to homepage to parse hidden authenticity token and to set initial "_gradescope_session" cookie
        auth_token = get_auth_token_init_gradescope_session(self.session)

        # login and set cookies in session. Result bool on whether login was success
        login_success = login_set_session_cookies(
            self.session, email, password, auth_token
        )
        if login_success:
            self.logged_in = True
            self.account = Account(self.session)
        else:
            raise ValueError("Invalid credentials.")
