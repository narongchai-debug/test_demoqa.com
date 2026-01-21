from config.settings import API_BASE_URL
import pytest, uuid, time
from clients.account_client import AccountClient

@pytest.fixture(scope="session")
def fixed_user():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "@Test12345"
    account_api = AccountClient()

    #Create user
    time.sleep(3)
    res = account_api.create_user(username, password)
    assert res.status_code == 201, f"Create user failed: {res.text}"
    user_id = res.json()["userID"]

    time.sleep(2)
    res = account_api.generate_token(username, password)
    assert res.status_code == 200, f"Generate Token failed: {res.text}"
    token = res.json()["token"]

    yield {
        "userName": username,
        "password": password,
        "userId": user_id,
        "token": token
    }
    
@pytest.fixture(scope="function")
def random_user():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "@Test12345"
    account_api = AccountClient()

    time.sleep(5)
    #Create new user
    res = account_api.create_user(username, password)
    assert res.status_code == 201, f"Create Failed: {res.text}"
    user_id = res.json()["userID"]

    #Generate token
    res = account_api.generate_token(username, password)
    assert res.status_code == 200, f"GenerateToken failed: {res.text}"
    token = res.json()["token"]

    return {
        "userName": username,
        "password": password,
        "userId": user_id,
        "token": token
    }

@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL