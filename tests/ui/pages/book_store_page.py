from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL

class BookStorePage:  
    search_field = (By.ID, "searchBox")
    logout_button = (By.ID, "submit")

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        self.driver.get(BASE_URL + "/books")
    
    def searchBook(self, book):
        search_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.search_field))
        search_input.clear()
        search_input.send_keys(book)
        
    def get_result_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#app > div > div > div > div.col-12.mt-4.col-md-6 > div.books-wrapper > div.ReactTable.-striped.-highlight > div.rt-table > div.rt-tbody > div:nth-child(1) > div > div:nth-child(3)")
            ) 
        ).text
        
    
    