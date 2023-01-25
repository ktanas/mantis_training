class SessionHelper:

    def __init__(self,app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd

        # Open home page - mantisbt login screen
        self.app.open_home_page()

        # Login to the Mantis Bug Tracker
        wd.find_element("name", "username").click()
        wd.find_element("name", "username").clear()
        wd.find_element("name", "username").send_keys("%s" % username)
        wd.find_element("name", "password").click()
        wd.find_element("name", "password").clear()
        wd.find_element("name", "password").send_keys("%s" % password)
        wd.find_element("css selector", 'input[type="submit"]').click()
        #wd.find_element("id", "LoginForm").submit()

    def logout(self):
        wd = self.app.wd
        wd.find_element("link text", "Logout").click()
        # wd.find_element("link text", "Wyloguj").click()

    def logout_is_visible(self):
        wd = self.app.wd
        return len(wd.find_elements("link text", "Logout")) > 0

    def is_logged_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element("id", "logged-in-user").text

    def ensure_logout(self):
        wd = self.app.wd
        if self.logout_is_visible():
            self.logout()

    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.logout_is_visible():
            if self.is_logged_as(username):
                return
            else:
                self.logout()
        self.login(username, password)
