from clients.bookstore_client import BookStoreClient
import allure

bookStore = BookStoreClient()

def assert_invalid_response(body):
    with allure.step("Verify response body"):
        assert {"code", "message"}.issubset(body)
        isinstance(body["code"], str) and body["code"].strip()
        isinstance(body["message"], str) and body["message"].strip()
    
def assert_valid_response(body):
    with allure.step("Verify response body"):
        assert {"books"}.issubset(body)
        isinstance(body["books"], list) and body, "Response array and not empty array"

@allure.feature("Book Store API")
@allure.story("Add book")
@allure.title("add book success")
def test_add_book(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    isbn = "9781593277574"

    with allure.step("Send request to add book"):
        res = bookStore.add_book(uid, isbn, token)
    with allure.step("Verify response status"):
        assert res.status_code == 201, f"add book failed: {res.text}"
    body = res.json()
    assert_valid_response(body)

@allure.feature("Book Store API")
@allure.story("Add book")
@allure.title("add book invalid uid")
def test_add_book_invalid_uid(random_user):
    invalid_uid = "12345678910"
    token = random_user["token"]
    isbn = "9781593277574"

    with allure.step("Send request to add book"):
        res = bookStore.add_book(invalid_uid, isbn, token)
    with allure.step("Verify response status"):
        assert res.status_code == 401, f"add book failed: {res.text}"

    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Add book")
@allure.title("add book invalid isbn")
def test_add_book_invalid_isbn(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_isbn = "123456-abcdef"

    with allure.step("Send request to add book"):
        res = bookStore.add_book(uid, invalid_isbn, token)
    with allure.step("Verify response status"):
        assert res.status_code == 400, f"add book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Add book")
@allure.title("add book unauth")
def test_add_book_not_authorized(random_user):
    uid = random_user["userId"]
    invalid_token = "123455678910_cat"
    isbn = "9781593277574"

    with allure.step("Send request to add book"):
        res = bookStore.add_book(uid, isbn, invalid_token)
    with allure.step("Verify response status"):
        assert res.status_code == 401, f"add book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)
