import pytest, uuid, os
from config.settings import BASE_URL, API_BASE_URL

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from api.clients.account_client import AccountClient


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL

@pytest.fixture(scope="function")
def driver():
    options = Options()

    if os.getenv("CI"):  # GitHub Actions จะมี CI=true
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
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
