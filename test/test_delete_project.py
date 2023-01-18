def test_delete_project(app):
    app.session.login("administrator", "root")

    old_project_list = app.get_project_list()

    x = -1
    i = 0
    for el in old_project_list:
        if el[0]=="Xyz120":
            x = i
        else:
            i = i + 1

    app.go_to_project_edition_screen("Xyz120")

    app.delete_project()
    app.delete_project()
    # delete_project method needs to be executed twice due to the fact that after clicking 'Delete Project' once,
    # an additional screen asking for confirmation of the deletion pops up

    new_project_list = app.get_project_list()

    assert len(new_project_list) == len(old_project_list) - 1

    del old_project_list[x]

    assert sorted(new_project_list) == sorted(old_project_list)

    app.session.logout()