import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tools.api_helper import APIHelper

# Load sensitive data from the local .env file
load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run tests in headless mode",
    )


@pytest.fixture(scope="session")
def user_id():
    return os.getenv("X_USER_ID")


@pytest.fixture()
def api_helper(user_id):
    return APIHelper(x_user_id=user_id)


@pytest.fixture()
def web_driver(request, user_id):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://qae-assignment-tau.vercel.app/?user-id={user_id}")
    yield driver
    driver.quit()
