from pages.book_store_page import BookStorePage
import allure

@allure.feature("UI")
@allure.story("UI Search book")
@allure.title("ui search book")
def test_search_book(driver):
    search_book = "Learning JavaScript Design Patterns"
    bookStorePage = BookStorePage(driver)
    
    #Go to Books page
    bookStorePage.open_page()
    bookStorePage.searchBook(search_book)

    result_title = bookStorePage.assert_search_book()
    assert search_book in result_title