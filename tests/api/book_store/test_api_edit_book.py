from config.settings import VALID_ISBN, NEW_ISBN
from clients.bookstore_client import BookStoreClient
import allure

bookStore = BookStoreClient()

def assert_valid_response(body):
    assert {"userId", "username", "books"}.issubset(body)
    isinstance(body["userId"], str) and body["userId"].strip()
    isinstance(body["username"], str) and body["username"].strip()
    isinstance(body["books"], list) and body, "Response not array or array empty"

def assert_invalid_response(body):
    assert {"code", "message"}.issubset(body)
    isinstance(body["code"], str) and body["code"].strip()
    isinstance(body["message"], str) and body["message"].strip()

@allure.feature("Book Store API")
@allure.story("Edit book")
@allure.title("edit book success")
def test_edit_book(random_user):
    uid = random_user["userId"]
    token = random_user["token"]

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.edit_book(VALID_ISBN, uid, NEW_ISBN, token)
    assert res.status_code == 200, f"edit book failed: {res.text}"
    body = res.json()
    assert_valid_response(body)

@allure.feature("Book Store API")
@allure.story("Edit book")
@allure.title("edit book invalid old isbn")
def test_edit_book_invalid_old_isbn(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_old_isbn = "12345678910"

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.edit_book(invalid_old_isbn, uid, NEW_ISBN, token)
    assert res.status_code == 400, f"edit book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Edit book")
@allure.title("edit book invalid new isbn")
def test_edit_book_invalid_new_isbn(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_new_isbn  = "123456789"

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.edit_book(VALID_ISBN, uid, invalid_new_isbn, token)
    assert res.status_code == 400, f"edit book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Edit book")
@allure.title("edit book invalid uid")
def test_edit_book_invalid_uid(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_uid = "invalid_12345"

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.edit_book(VALID_ISBN, invalid_uid, NEW_ISBN, token)
    assert res.status_code == 401, f"edit book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Edit book")
@allure.title("edit book unauth")
def test_edit_book_not_authorized(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_token = "invalid_12345"

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.edit_book(VALID_ISBN, uid, NEW_ISBN, invalid_token)  
    assert res.status_code == 401, f"edit book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)


