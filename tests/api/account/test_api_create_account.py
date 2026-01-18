from clients.account_client import AccountClient
from config.settings import VALID_USERNAME, VALID_PASSWORD, WRONG_USERNAME, WRONG_PASSWORD
import uuid, allure

account_api = AccountClient()

def assert_invalid_response_structure(body):
    with allure.step("Verify response status"):
        assert {"code", "message"}.issubset(body)
        isinstance(body["code"], str) and body["code"].strip()
        isinstance(body["message"], str) and body["message"].strip()

#TC_API_01
@allure.feature("Account API")
@allure.story("Create account")
@allure.title("Create account success")
def test_create_account_success():
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "@Test12345"

    with allure.step("Send request to create account"):
        res = account_api.create_user(username, password)
    with allure.step("Verify response status"):
        assert res.status_code == 201

    body = res.json()
    with allure.step("Verify response body"):
        assert {"userID", "username"}.issubset(body)
        assert isinstance(body.get("userID"), str) and body["userID"].strip()
        assert isinstance(body.get("username"), str) and body["username"].strip()

#TC_API_02
@allure.feature("Account API")
@allure.story("Create account")
@allure.title("create account dup username")
def test_create_account_dup_username():
    #qa2025 มีข้อมูลในระบบอยู่แล้ว
    with allure.step("Send request to create account"):
        res = account_api.create_user(VALID_USERNAME, VALID_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 406

    body = res.json()
    assert_invalid_response_structure(body)


#TC_API_03
@allure.feature("Account API")
@allure.story("Create account")
@allure.title("create account invalid password")
def test_create_account_invalid_password():
    #พาสเวิร์ด ไม่ตรงตามเงื่อนไขในการสมัคร
    with allure.step("Send request to create account"):
        res = account_api.create_user(WRONG_USERNAME, WRONG_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 400

    body = res.json()
    assert_invalid_response_structure(body)

#TC_API_04
@allure.feature("Account API")
@allure.story("Create account")
@allure.title("create account missing username")
def test_create_account_missing_username():
    #ไม่ใส่ username
    with allure.step("Send request to create account"):
        res = account_api.create_user("", VALID_PASSWORD)
    with allure.step("Verify response status"):
        assert res.status_code == 400

    body = res.json()
    assert_invalid_response_structure(body)

#TC_API_05
@allure.feature("Account API")
@allure.story("Create account")
@allure.title("create account missing password")
def test_create_account_missing_password():
    #ไม่ใส่ password
    with allure.step("Send request to create account"):
        res = account_api.create_user(VALID_USERNAME, "")
    with allure.step("Verify response status"):
        assert res.status_code == 400

    body = res.json()
    assert_invalid_response_structure(body)