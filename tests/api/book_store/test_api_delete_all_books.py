from clients.bookstore_client import BookStoreClient
from config.settings import VALID_ISBN
import allure

bookStore = BookStoreClient()

def assert_invalid_response(body):
    assert {"code", "message"}.issubset(body)
    isinstance(body["code"], str) and body["code"].strip()
    isinstance(body["message"], str) and body["message"].strip()

@allure.feature("Book Store API")
@allure.story("Delete all books")
@allure.title("delete all books success")
def test_delete_all_books(random_user):
    uid = random_user["userId"]
    token = random_user["token"]

    #Add book for delete
    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.delete_all_books(uid, token)
    assert res.status_code == 204, f"delete all books failed: {res.text}"

@allure.feature("Book Store API")
@allure.story("Delete all books")
@allure.title("delete all books invalid uid")
def test_delete_all_books_invalid_uid(random_user):
    uid = random_user["userId"]
    invalid_uid = "invalid1234"
    token = random_user["token"]

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.delete_all_books(invalid_uid, token)
    assert res.status_code == 401, f"delete all books failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Delete all books")
@allure.title("delete all books unauth")
def test_delete_all_books_not_authorized(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_token = "invalid-12345"

    res = bookStore.add_book(uid, VALID_ISBN, token)
    assert res.status_code == 201, f"add book failed: {res.text}"

    res = bookStore.delete_all_books(uid, invalid_token)
    assert res.status_code == 401, f"delete all books failed: {res.text}"
    body = res.json()  
    assert_invalid_response(body)