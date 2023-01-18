def test_edit_existing_project(app):
    app.session.login("administrator", "root")

    old_project_list = app.get_project_list()

    x = -1
    i = 0
    for el in old_project_list:
        if el[0]=="Xyz121":
            x = i
        else:
            i = i + 1

    app.go_to_project_edition_screen("Xyz121")

    app.enter_edited_project_data("Xyz123", "stable", False, "private", "This is even nicer project!")
    # app.enter_edited_project_data("Xyz123", "stabilny", False, "prywatny", "This is even nicer project!")

    new_project_list = app.get_project_list()

    assert len(new_project_list) == len(old_project_list)

    old_project_list[x] = ["Xyz123", "stable", False, "private", "This is even nicer project!"]
    # old_project_list[x] = ["Xyz123", "stabilny", False, "prywatny", "This is even nicer project!"]
    # Actually, projects in Mantis Bug Tracker are listed alphabetically, by the project's name (which must be unique),
    # so the index (position in the list) of the project which was just edited could be different than in the old list.
    # However, in out rest we only use assertion on the sorted list, so there should be no problem there.

    assert sorted(new_project_list) == sorted(old_project_list)

    app.session.logout()
