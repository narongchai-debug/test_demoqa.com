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

    def open_page(self, retries=3):
        for i in range(retries):
            try:
                self.driver.get(BASE_URL + "/books")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.search_field)
                )
                self._remove_ads()
                return
            except Exception:
                if i == retries - 1: raise
                self.driver.refresh()
    
    def searchBook(self, book):
        search_input = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.search_field))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
        search_input.clear()
        search_input.send_keys(book)
        
    def get_result_title(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#app > div > div > div > div.col-12.mt-4.col-md-6 > div.books-wrapper > div.ReactTable.-striped.-highlight > div.rt-table > div.rt-tbody > div:nth-child(1) > div > div:nth-child(3)")
            ) 
        ).text
        
    
    