from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from config.settings import VALID_ISBN
import allure, time

@allure.feature("UI")
@allure.story("UI Delete book")
@allure.title("ui delete book")
def test_delete_book(random_user, driver):
    title_book = "Understanding ECMAScript 6"
    username = random_user["userName"]
    password = random_user["password"]
    uid = random_user["userId"]
    token = random_user["token"]

    loginPage = LoginPage(driver)
    profile_page = ProfilePage(driver)

    res = profile_page.add_book(uid= uid, isbn=VALID_ISBN, token=token) #Title = Understanding ECMAScript 6
    assert res.status_code == 201, f"add book failed: {res.text}"

    #Go to Login page
    loginPage.open_page()
    loginPage.login(username, password)

    profile_page.open_page()

    profile_page.delete_book(title_book)
    profile_page.assert_book_deleted(title_book)
    time.sleep(2)
    profile_page.logout()

