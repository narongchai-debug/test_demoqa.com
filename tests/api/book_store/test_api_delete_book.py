from clients.bookstore_client import BookStoreClient
import allure

bookStore = BookStoreClient()

def assert_invalid_response(body):
    assert {"code", "message"}.issubset(body)
    isinstance(body["code"], str) and body["code"].strip()
    isinstance(body["message"], str) and body["message"].strip()

@allure.feature("Book Store API")
@allure.story("Delete book")
@allure.title("delete book success")
def test_delete_book(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    isbn = "9781593277574"
    res = bookStore.add_book(uid, isbn, token)
    assert res.status_code == 201, f"add book failed: {res.text}"
    assert {"books"}.issubset(res.json())

    res = bookStore.delete_book(isbn, uid, token)
    assert res.status_code == 204, f"delete book failed: {res.text}"
    
@allure.feature("Book Store API")
@allure.story("Delete book")
@allure.title("delete book invalid uid")
def test_delete_book_invalid_uid(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    isbn = "9781593277574"
    invalid_uid = "invalid123"

    res = bookStore.add_book(uid, isbn, token)
    assert res.status_code == 201, f"add book failed: {res.text}"
    assert {"books"}.issubset(res.json())

    res = bookStore.delete_book(isbn, invalid_uid, token)
    assert res.status_code == 401, f"delete book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Delete book")
@allure.title("delete book invalid isbn")
def test_delete_book_invalid_isbn(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    isbn = "9781593277574"
    invalid_isbn = "isbn is invalid"
    
    res = bookStore.add_book(uid, isbn, token)
    assert res.status_code == 201, f"add book failed: {res.text}"
    assert {"books"}.issubset(res.json())

    res = bookStore.delete_book(invalid_isbn, uid, token)
    assert res.status_code == 400, f"delete book failed: {res.text}"
    body = res.json()
    assert_invalid_response(body)

@allure.feature("Book Store API")
@allure.story("Delete book")
@allure.title("delete book unauth")
def test_delete_book_not_authorized(random_user):
    uid = random_user["userId"]
    token = random_user["token"]
    invalid_token = "12345678910"
    isbn = "9781593277574"

    res = bookStore.add_book(uid, isbn, token)
    assert res.status_code == 201, f"add book failed: {res.text}"
    assert {"books"}.issubset(res.json())

    res = bookStore.delete_book(isbn, uid, invalid_token)
    assert res.status_code == 401
    body = res.json()
    assert_invalid_response(body)
