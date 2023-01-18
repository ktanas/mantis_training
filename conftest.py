# -*- coding: utf-8 -*-
from fixture import application
import pytest
import json
import os.path

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as conf:
            target = json.load(conf)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    webadmin_config = load_config(request.config.getoption("--target"))['webadmin']

    if fixture is None or not fixture.is_valid():
        fixture = application.Application(browser=browser, base_url=web_config["base_url"],
                                          username=webadmin_config["username"], password=webadmin_config["password"])

    # fixture.session.ensure_login(username=webadmin_config["username"], password=webadmin_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.tear_down()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
