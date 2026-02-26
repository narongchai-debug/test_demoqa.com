from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from config.settings import BASE_URL
import requests, time

class ProfilePage:
    expectedUrl = "/login"
    logout_button = (By.ID, "submit");
     
    def __init__(self, driver):
        self.driver = driver
        self.session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist= 502,
            allowed_methods= "POST"
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _remove_ads(self):
        script = """
        var ads = document.querySelectorAll('#fixedban, footer, [id^="google_ads"]');
        for (var i = 0; i < ads.length; i++) {
            ads[i].style.display = 'none';
        }
        """
        self.driver.execute_script(script)

    def open_page(self):
        self.driver.get(BASE_URL + "/profile")
        self._remove_ads()

    def add_book(self, uid: str, isbn: str, token: str):
        payload = {
            "userId": uid,
            "collectionOfIsbns": [
                { "isbn": isbn }
            ]
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }
        return requests.post(BASE_URL + "/BookStore/v1/Books", headers=headers, json=payload)

    def delete_book(self, book_title: str, timeout: int = 20):
        self._remove_ads()
        # รอให้ปุ่มลบแสดงผลและคลิกได้

        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "delete-record-9781593277574"))
        ).click();
 
        # จัดการ Modal และ Alert พร้อม Retry หากไม่พบ Alert 
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "closeSmallModal-ok"))
        ).click()

        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.accept()

    def assert_book_deleted(self, book_title: str)-> bool:
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "delete-record-9781593277574"))
        )

    def logout(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.logout_button)).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains(self.expectedUrl))
        assert self.expectedUrl in self.driver.current_url
