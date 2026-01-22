from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL

class LoginPage:
    expectedUrl = "profile"
    username_field = (By.ID, "userName")
    password_field = (By.ID, "password")
    loginBtn = (By.ID, "login")

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        self.driver.get(BASE_URL + "/login")

    def enteredUsername(self, username: str):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.username_field)).send_keys(username)
    
    def enteredPassword(self, password: str):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.password_field)).send_keys(password)

    def login(self, username: set, password: str):
        self.enteredUsername(username)
        self.enteredPassword(password)
        
        login_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.loginBtn))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        self.driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(self.driver, 15).until(EC.url_contains(self.expectedUrl))
        assert self.expectedUrl in self.driver.current_url

    def login_invalid_username(self, username: str, password: str):
        self.enteredUsername(username)
        self.enteredPassword(password)
        
        login_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.loginBtn))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        self.driver.execute_script("arguments[0].click();", login_btn)

        error_msg = WebDriverWait(self.driver , 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="name"]'))
        )
        assert error_msg.text == "Invalid username or password!", f"ข้อความผิด: {error_msg.text}"

        
    