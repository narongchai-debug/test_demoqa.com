import pytest
import uuid
from config.settings import BASE_URL, API_BASE_URL

from api.clients.account_client import AccountClient
from selenium import webdriver
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver 
    #after tested
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver, random_user):
    login_page = LoginPage(driver)
    login_page.open_page()

    username = random_user["userName"]
    password = random_user["password"]
    uid = random_user["userId"]
    token = random_user["token"]
    login_page.login(username, password)
    return {
        "userId": uid,
        "token": token
    }

@pytest.fixture(scope="function")
def random_user():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "@Test12345"

    account_api = AccountClient()
    #Create new user
    res = account_api.create_user(username, password)
    assert res.status_code == 201, f"Create user failed: {res.text}"
    userId = res.json()["userID"]

    #Generate token
    res = account_api.generate_token(username, password)
    assert res.status_code == 200, f"GenerateToken failed: {res.text}"
    token = res.json()["token"]

    return {
        "userName": username,
        "password": password,
        "userId": userId,
        "token": token
    }
