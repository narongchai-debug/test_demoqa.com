from clients.bookstore_client import BookStoreClient
import allure

bookStore = BookStoreClient()

def assert_valid_response(body):
    assert {"isbn", "title", "subTitle", "author", "publish_date"}.issubset(body)
    assert isinstance(body["isbn"], str) and body["isbn"].strip()
    assert isinstance(body["title"], str) and body["title"].strip()
    assert isinstance(body["subTitle"], str) and body["subTitle"].strip()
    assert isinstance(body["author"], str) and body["author"].strip()
    assert isinstance(body["publish_date"], str) and body["publish_date"].strip()

@allure.feature("Book Store API")
@allure.story("Get all books")
@allure.title("get all books success")
def test_get_books():
    res = bookStore.get_all_books()
    assert res.status_code == 200, f"Response: {res.text}"
    body = res.json()
    assert {"books"}.issubset(body)

@allure.feature("Book Store API")
@allure.story("Get book")
@allure.title("get book success")
def test_get_book_valid_isbn():
    res = bookStore.get_book_by_isbn("9781593277574")
    assert res.status_code == 200, f"Response: {res.text}"
    body = res.json()
    assert_valid_response(body)

@allure.feature("Book Store API")
@allure.story("Get book")
@allure.title("get book invalid isbn")
def test_get_book_invalid_isbn():
    res = bookStore.get_book_by_isbn("12345678910")
    assert res.status_code == 400, f"{res.text}"
    body = res.json()
    assert {"code", "message"}.issubset(body)
    assert isinstance(body["code"], str) and body["code"].strip()
    assert isinstance(body["message"], str) and body["message"].strip()
