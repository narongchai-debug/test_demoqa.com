from clients.account_client import AccountClient
import allure

account_api = AccountClient()

def assert_success_response(body):
    with allure.step("Verify response body"):
        assert {"userId", "username", "books"}.issubset(body)
        assert isinstance(body["userId"], str) and body["userId"].strip()
        assert isinstance(body["username"], str) and body["username"].strip()

def assert_invalid_response(body):
    with allure.step("Verify response body"):
        assert {"code", "message"}.issubset(body)
        assert isinstance(body["code"], str) and body["code"].strip()
        assert isinstance(body["message"], str) and body["message"].strip()

#TC_API_16
@allure.feature("Account API")
@allure.story("Get account")
@allure.title("get account success")
def test_get_account_success(fixed_user):
    uid = fixed_user["userId"]
    token = fixed_user["token"]
    with allure.step("Send request to get user"):
        res = account_api.get_user_by_uid(uid, token)
    with allure.step("Verify response status"):
        assert res.status_code == 200, f"Get account failed: {res.text}"

    body = res.json()
    assert_success_response(body)

#TC_API_17
@allure.feature("Account API")
@allure.story("Get account")
@allure.title("get account invalid uid")
def test_get_account_failed_invalid_uid(fixed_user):
    token = fixed_user["token"]
    with allure.step("Send request to get user"):
        res = account_api.get_user_by_uid("e123456", token)
    with allure.step("Verify response status"):
        assert res.status_code == 401, f"Response: {res.text}"

    body = res.json()
    assert_invalid_response(body)

#TC_API_18
@allure.feature("Account API")
@allure.story("Get account")
@allure.title("get account missing uid")
def test_get_account_failed_missing_uid(fixed_user):
    token = fixed_user["token"]
    with allure.step("Send request to get user"):
        res = account_api.get_user_by_uid(token= token)

    content_type = res.headers.get("Content-Type", "")
    with allure.step("Verify response body"):
        assert "application/json" in content_type.lower(), (
            f"Contract violation: expected JSON but got {content_type} (status={res.status_code}) (text: {res.text})"
        )

#TC_API_19
@allure.feature("Account API")
@allure.story("Get account")
@allure.title("get account unauth")
def test_get_account_failed_not_authorized(fixed_user):
    user_id = fixed_user["userId"]
    with allure.step("Send request to get user"):
        res = account_api.get_user_by_uid(uid=user_id)
    with allure.step("Verify response status"):
        assert res.status_code == 401, f"Response: {res.text}"

    body = res.json()
    assert_invalid_response(body)
