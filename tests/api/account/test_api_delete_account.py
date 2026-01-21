from clients.account_client import AccountClient
import allure, time

def assert_common_response_structure(body):
    with allure.step("Verify response body"):
        assert {"code", "message"}.issubset(body)
        assert isinstance(body["code"], str) and body["code"].strip()
        assert isinstance(body["message"], str) and body["message"].strip()

#TC_API_20
@allure.feature("Account API")
@allure.story("Delete account Positive")
@allure.title("delete account success")
def test_delete_account_success(random_user):
    user_id = random_user["userId"]
    token = random_user["token"]
    account_api = AccountClient()

    with allure.step("Send request to delete account"):
        res = account_api.delete_user_by_uid(user_id, token)
    with allure.step("Verify response status"):
        assert res.status_code == 204, f"Error message: {res.text}" 

#TC_API_21
@allure.feature("Account API")
@allure.story("Delete account")
@allure.title("delete account invalid uid")
def test_delete_account_failed_invalid_uid(random_user):
    user_id = "invalid-uid"
    token = random_user["token"]
    account_api = AccountClient()

    with allure.step("Send request to delete account"):
        res = account_api.delete_user_by_uid(user_id, token)
    with allure.step("Verify response status"):
        assert res.status_code == 200, f"Error message: {res.text}"

    body = res.json()
    assert_common_response_structure(body)

#TC_API_22
@allure.feature("Account API")
@allure.story("Delete account")
@allure.title("delete account unauth")
def test_delete_account_failed_unauthorized(random_user):
    account_api = AccountClient()
    uid = random_user["userId"]
    invalid_token = "12345678910"

    with allure.step("Send request to delete account"):
        res = account_api.delete_user_by_uid(uid, invalid_token)
    with allure.step("Verify response status"):
        assert res.status_code == 401, f"Error message: {res.text}"
        
    body = res.json()
    assert_common_response_structure(body)

    




