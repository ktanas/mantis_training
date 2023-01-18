def test_add_new_project(app):
    app.session.login("administrator", "root")

    old_project_list = app.get_project_list()

    app.go_to_add_projects_screen()
    app.enter_project_data("Xyz130", "release", True, "public", "This is a very nice project!")
    # app.enter_project_data("Xyz130", "ukończony", True, "publiczny", "This is a very nice project!")

    new_project_list = app.get_project_list()

    assert len(new_project_list) == len(old_project_list) + 1

    x = old_project_list.index(["Xyz130", "release", True, "public", "This is a very nice project!"])
    old_project_list.insert(x, ["Xyz130", "release", True, "public", "This is a very nice project!"])
    # x = old_project_list.index(["Xyz130", "ukończony", True, "publiczny", "This is a very nice project!"])
    # old_project_list.insert(x, ["Xyz130", "ukończony", True, "publiczny", "This is a very nice project!"])

    assert sorted(new_project_list) == sorted(old_project_list)

    app.session.logout()
