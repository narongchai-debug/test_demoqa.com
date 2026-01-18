from clients.account_client import AccountClient
from config.settings import VALID_USERNAME, VALID_PASSWORD, WRONG_USERNAME, WRONG_PASSWORD
import allure

account_api = AccountClient()

def assert_invalid_response_structure(body):
    with allure.step("Verify Response body"):
        assert {"code", "message"}.issubset(body)
        assert isinstance(body["code"], str) and body["code"].strip()
        assert isinstance(body["message"], str) and body["message"].strip()

#TC_API_11
@allure.feature("Account API")
@allure.story("Auth")
@allure.title("Auth success")
def test_authorized_success(fixed_user):
    username = fixed_user["userName"]
    password = fixed_user["password"]
    with allure.step("Send request to auth"):
        res = account_api.user_authorization(username, password)

    with allure.step("Verify response status"): 
        assert res.status_code == 200 and res.json() == True
    
#TC_API_12
@allure.feature("Account API")
@allure.story("Auth")
@allure.title("Auth failed invalid username")
def test_authorized_failed_invalid_username():
    with allure.step("Send request to auth"):
        res = account_api.user_authorization(WRONG_USERNAME, VALID_PASSWORD)
    
    with allure.step("Verify response status"): 
        assert res.status_code == 404

    body = res.json()
    assert_invalid_response_structure(body)

#TC_API_13
@allure.feature("Account API")
@allure.story("Auth")
@allure.title("Auth failed invalid password")
def test_authorized_failed_invalid_password():
    with allure.step("Send request to auth"):
        res = account_api.user_authorization(VALID_USERNAME, WRONG_PASSWORD)
    
    with allure.step("Verify response status"):
        assert res.status_code == 404

    body = res.json()
    assert_invalid_response_structure(body)

#TC_API_14
@allure.feature("Account API")
@allure.story("Auth")
@allure.title("Auth failed missing username")
def test_authorized_failed_missing_username():
    with allure.step("Send request to auth"):
        res = account_api.user_authorization("", VALID_PASSWORD)

    with allure.step("Verify response status"):
        assert res.status_code == 400

    body = res.json()
    assert_invalid_response_structure(body)

#TC_API_15
@allure.feature("Account API")
@allure.story("Auth")
@allure.title("Auth failed missing password")
def test_authorized_failed_missing_password():
    with allure.step("Send request to auth"):
        res = account_api.user_authorization(VALID_USERNAME, "")

    with allure.step("Send request to auth"):
        assert res.status_code == 400

    body = res.json()
    assert_invalid_response_structure(body)