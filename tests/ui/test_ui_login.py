from pages.login_page import LoginPage
import allure

@allure.feature("UI")
@allure.story("UI Login")
@allure.title("ui login")
def test_login(driver):
    loginPage = LoginPage(driver)
    username = "qa2025"
    password = "@TestQA2025"

    loginPage.open_page()
    loginPage.login(username, password)

def test_login_invalid_username(driver):
    loginPage = LoginPage(driver)
    invalid_username = "invalid1234"
    password = "@TestQA2025"

    loginPage.open_page()
    loginPage.login_invalid_username(invalid_username, password)