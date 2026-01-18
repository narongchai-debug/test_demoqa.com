from clients.account_client import AccountClient
from config.settings import VALID_USERNAME, VALID_PASSWORD, WRONG_USERNAME, WRONG_PASSWORD
import allure

account_api = AccountClient()

def assert_success_response(body):
    with allure.step("Verify response body"):
        assert {"token", "expires", "status", "result"}.issubset(body)
        assert isinstance(body["token"], str) and body["token"].strip()
        assert isinstance(body["expires"], str) and body["expires"].strip()
        assert isinstance(body["status"], str) and body["status"].strip()
        assert isinstance(body["result"], str) and body["result"].strip()

def assert_invalid_response(body):
    with allure.step("Verify response body"):
        assert {"token", "expires", "status", "result"}.issubset(body)
        assert body["token"] is None
        assert body["expires"] is None
        assert isinstance(body["status"], str) and body["status"].strip()
        assert isinstance(body["result"], str) and body["result"].strip()

#TC_API_06
@allure.feature("Account API")
@allure.story("Generate Token")
@allure.title("gen token success")
def test_generate_token_success():

    with allure.step("Send request to Generate token"):
        res = account_api.generate_token(VALID_USERNAME, VALID_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 200, f"Response: {res.text}"

    body = res.json()
    assert_success_response(body)

#TC_API_07
@allure.feature("Account API")
@allure.story("Generate Token")
@allure.title("gen token invalid username")
def test_generate_token_failed_invalid_username():
    with allure.step("Send request to Generate token"):
        res = account_api.generate_token(WRONG_USERNAME, VALID_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 200, f"Response: {res.text}"

    body = res.json()
    assert_invalid_response(body)

#TC_API_08
@allure.feature("Account API")
@allure.story("Generate Token")
@allure.title("gen token invalid password")
def test_generate_token_failed_invalid_password():
    invalid_pw = WRONG_PASSWORD

    with allure.step("Send request to Generate token"):
        res = account_api.generate_token(VALID_USERNAME, invalid_pw)
    with allure.step("Verify response status"):
        assert res.status_code == 200, f"Response: {res.text}"

    body = res.json()
    assert_invalid_response(body)

#TC_API_09
@allure.feature("Account API")
@allure.story("Generate Token")
@allure.title("gen token missing username")
def test_generate_token_failed_missing_username():
    with allure.step("Send request to Generate token"):
        res = account_api.generate_token("", password= VALID_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 400, f"Response: {res.text}"

    body = res.json()
    with allure.step("Verify response body"):
        assert {"code", "message"}.issubset(body)
        assert isinstance(body["code"], str) and body["code"].strip()
        assert isinstance(body["message"], str) and body["code"].strip()

#TC_API_10
@allure.feature("Account API")
@allure.story("Generate Token")
@allure.title("gen token missing password")
def test_generate_token_failed_missing_password():
    with allure.step("Send request to Generate token"):
        res = account_api.generate_token(username= VALID_USERNAME)
    with allure.step("Verify response status"):   
        assert res.status_code == 400, f"Response: {res.text}"

    body = res.json()
    with allure.step("Verify response body"):
        assert {"code", "message"}.issubset(body)
        assert isinstance(body["code"], str) and body["code"].strip()
        assert isinstance(body["message"], str) and body["code"].strip()



        