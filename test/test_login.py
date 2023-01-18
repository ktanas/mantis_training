def test_login(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_as("administrator")
    app.session.logout()
