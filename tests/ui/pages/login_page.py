from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.settings import BASE_URL

class LoginPage:
    expectedUrl = "profile"
    username_field = (By.ID, "userName")
    password_field = (By.ID, "password")
    loginBtn = (By.ID, "login")

    def __init__(self, driver):
        self.driver = driver

    def _remove_ads(self):
        """Remove ads that frequently block elements on demoqa.com"""
        script = """
        var ads = document.querySelectorAll('#fixedban, footer, [id^="google_ads"]');
        for (var i = 0; i < ads.length; i++) {
            ads[i].style.display = 'none';
        }
        """
        self.driver.execute_script(script)

    def open_page(self, retries=3):
        for i in range(retries):
            try:
                self.driver.get(BASE_URL + "/login")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.username_field)
                )
                self._remove_ads()
                return
            except Exception:
                if i == retries - 1: raise
                self.driver.refresh()

    def enteredUsername(self, username: str):
        usernameInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.username_field))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", usernameInput)
        usernameInput.clear()
        usernameInput.send_keys(username)
    
    def enteredPassword(self, password: str):
        passwordInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.password_field))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", passwordInput)
        passwordInput.clear()
        passwordInput.send_keys(password)

    def login(self, username: str, password: str):
        self.enteredUsername(username)
        self.enteredPassword(password)
        
        login_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.loginBtn))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        self.driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(self.driver, 30).until(EC.url_contains(self.expectedUrl))
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

        
    