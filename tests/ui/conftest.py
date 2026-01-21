import pytest, uuid, os
from config.settings import BASE_URL, API_BASE_URL

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.profile_page import ProfilePage
from api.clients.account_client import AccountClient


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL

@pytest.fixture(scope="function")
def driver():
    if os.getenv("CI"):  # GitHub Actions จะมี CI=true
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

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
