from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from fixture.session import SessionHelper
from selenium.webdriver.support.ui import Select
from utilities import project_utilities


class Application:

    def __init__(self, browser="", base_url="", username="", password=""):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "edge":
            self.wd = webdriver.Edge()
        else:
            raise ValueError("Unrecognized browser %s" % browser)

        self.wd.implicitly_wait(5)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.session = SessionHelper(self, username, password)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def delay(self, time):
        wd = self.wd
        wd.implicitly_wait(time)

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)
        return wd

    def open_contact_home_page(self):
        wd = self.wd
        if (len(wd.find_elements("link text", "Send e-Mail")) == 0
            or len(wd.find_elements("link text", "Delete")) == 0
            or len(wd.find_elements("link text", "Add to")) == 0):
                wd.find_element("link text", "home").click()

    def enter_text_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element("name", field_name).click()
            wd.find_element("name", field_name).clear()
            wd.find_element("name", field_name).send_keys("%s" % text)

    def enter_selectable_field_value(self, field_name, xpath, chosen_value):
        wd = self.wd
        if chosen_value is not None:
            wd.find_element("name", field_name).click()
            Select(wd.find_element("name", field_name)).select_by_visible_text("%s" % chosen_value)
            wd.find_element("xpath", xpath).click()

    def go_to_new_contact_editor_page(self):
        wd = self.wd
        wd.find_element("link text", "add new").click()

    def enter_manage_view(self):
        wd = self.wd
        wd.find_element("link text", "Manage").click()
        # wd.find_element("link text", "Zarządzanie").click()

    def enter_manage_projects_view(self):
        wd = self.wd
        wd.find_element("link text", "Manage Projects").click()
        # wd.find_element("link text", "Zarządzanie projektami").click()

    def go_to_add_projects_screen(self):
        wd = self.wd
        wd.find_element("css selector", "[value=\"Create New Project\"]").click()
        # wd.find_element("css selector", "[value=\"Stwórz nowy projekt\"]").click()

    def go_to_project_edition_screen(self, edited_project_name):
        wd = self.wd
        wd.find_element("link text", edited_project_name).click()

    def delete_project(self):
        wd = self.wd
        wd.find_element("css selector", "[value=\"Delete Project\"]").click()
        # wd.find_element("css selector", "[value=\"Usuń projekt\"]").click()

    def enter_project_data(self, project_name, status, IGC, view_state, description):
        # Enter project data when creating a new project
        wd = self.wd
        self.enter_text_field_value("name", project_name)
        self.enter_selectable_field_value("status",
                                          "//option[@value='%s']" % project_utilities.status_dict[status],
                                          status)
        if wd.find_element("id", "project-inherit-global").is_selected() != IGC:
            wd.find_element("id", "project-inherit-global").click()

        self.enter_selectable_field_value("view_state",
                                          "//option[@value='%s']" % project_utilities.view_state_dict[view_state],
                                          view_state)

        self.enter_text_field_value("description", description)

        wd.find_element("css selector", "[value=\"Add project\"]").click()
        # wd.find_element("css selector", "[value=\"Dodaj projekt\"]").click()

        WebDriverWait(wd, 5).until(expected_conditions.presence_of_element_located(By.CSS_SELECTOR("[value=\"Create new project\"]")))
        # WebDriverWait(wd, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"[value=\"Stwórz nowy projekt\"]")))

    def enter_edited_project_data(self, project_name, status, IGC, view_state, description):
        # Enter new data values when editing an existing project
        wd = self.wd
        self.enter_text_field_value("name", project_name)
        self.enter_selectable_field_value("status",
                                          "//option[@value='%s']" % project_utilities.status_dict[status],
                                          status)

        if wd.find_element("id", "project-inherit-global").is_selected() != IGC:
            wd.find_element("id", "project-inherit-global").click()

        self.enter_selectable_field_value("view_state",
                                          "//option[@value='%s']" % project_utilities.view_state_dict[view_state],
                                          view_state)

        self.enter_text_field_value("description", description)

        wd.find_element("css selector", "[value=\"Update project\"]").click()
        # wd.find_element("css selector", "[value=\"Aktualizuj projekt\"]").click()

        WebDriverWait(wd, 5).until(expected_conditions.presence_of_element_located(By.CSS_SELECTOR("[value=\"Create new project\"]")))
        # WebDriverWait(wd, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"[value=\"Stwórz nowy projekt\"]")))

    def get_project_list(self):
        wd = self.wd
        self.enter_manage_view()
        self.enter_manage_projects_view()

        project_list = []
        i = 0

        for el in wd.find_elements("tag name", "tr"):
            cells = el.find_elements("tag name", "td")
            print("len(cells)=%s" % len(cells))
            if len(cells)==5:
                name        = cells[0].text
                status      = cells[1].text
                enabled     = str(cells[2].text == "X")
                view_state  = cells[3].text
                description = cells[4].text

                if i>0:
                    project_list.append([name,status,enabled,view_state,description])
                i=i+1
        return project_list

    def is_element_present(self, how, what):
        try:
            self.wd.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            alert = self.wd.switch_to.alert
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.wd.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tear_down(self):
        self.wd.quit()
