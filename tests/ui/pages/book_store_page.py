from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL

class BookStorePage:  
    search_field = (By.ID, "searchBox")
    logout_button = (By.ID, "submit")

    def __init__(self, driver):
        self.driver = driver

    def _remove_ads(self):
        script = """
        var ads = document.querySelectorAll('#fixedban, footer, [id^="google_ads"]');
        for (var i = 0; i < ads.length; i++) {
            ads[i].style.display = 'none';
        }
        """
        self.driver.execute_script(script)

    def open_page(self):
        self.driver.get(BASE_URL + "/books")
        self._remove_ads()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.search_field)
        )
    
    def searchBook(self, book_title: str):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.search_field)).send_keys(book_title)

    def assert_search_book(self)-> bool:
        return self.driver.find_element(By.ID, "see-book-Learning JavaScript Design Patterns").text

    
    