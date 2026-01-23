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
    logout_button = (By.ID, "submit")
    
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

    def open_page(self, retries=3):
        for i in range(retries):
            try:
                self.driver.get(BASE_URL + "/profile")
                self._remove_ads()
                # Wait for something that indicates the profile page is loaded
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.logout_button)
                )
                return
            except Exception:
                if i == retries - 1: raise
                self.driver.refresh()

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
        # หา Row ของหนังสือที่ต้องการลบ
        row = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'rt-tbody')]//div[contains(@class,'rt-tr-group')][.//a[normalize-space()='{book_title}']]"))
        )
        # รอให้ปุ่มลบแสดงผลและคลิกได้
        deleteBtn = WebDriverWait(row, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#delete-record-undefined"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", deleteBtn)
        self.driver.execute_script("arguments[0].click();", deleteBtn)

        # จัดการ Modal และ Alert พร้อม Retry หากไม่พบ Alert (มักเกิดใน CI)
        for i in range(3):
            try:
                ok_btn = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.ID, "closeSmallModal-ok"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ok_btn)
                self.driver.execute_script("arguments[0].click();", ok_btn)

                # รอ Alert
                alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
                alert.accept()
                break  # สำเร็จแล้วออกจาก Loop
            except TimeoutException:
                if i == 2:  # ครั้งสุดท้ายแล้วยังไม่ได้
                    raise TimeoutException(f"Failed to delete book '{book_title}' due to missing alert after clicking OK button in modal.")
                time.sleep(1)

        # รอให้ Modal หายไป
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, "closeSmallModal-ok"))
        )


    def assert_book_deleted(self, book_title: str)-> bool:

        xpath_row = f"//div[contains(@class,'rt-tbody')]//div[contains(@class,'rt-tr-group')][.//a[normalize-space()='{book_title}']]"
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, xpath_row))
        )

    def logout(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.logout_button)).click()
        WebDriverWait(self.driver, 10).until(EC.url_contains(self.expectedUrl))
        assert self.expectedUrl in self.driver.current_url