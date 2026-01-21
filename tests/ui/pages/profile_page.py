from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config.settings import BASE_URL
import requests, time

class ProfilePage:
    expectedUrl = "/login"
    logout_button = (By.ID, "submit")
    
    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        self.driver.get(BASE_URL + "/profile")

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

    def delete_book(self, book_title: str,timeout: int = 15):
        #หาRow ของหนังสือที่ต้องการลบ
        row = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'rt-tbody')]//div[contains(@class,'rt-tr-group')][.//a[normalize-space()='{book_title}']]"))
        )
        # รอให้ปุ่มลบแสดงผลและคลิกได้
        deleteBtn = WebDriverWait(row, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#delete-record-undefined"))
        )
        deleteBtn.click()

        ok_btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "closeSmallModal-ok"))
        )
        ok_btn.click()

        # จัดการ Alert ทันทีหลังจากกด OK ใน Modal
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.accept()

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