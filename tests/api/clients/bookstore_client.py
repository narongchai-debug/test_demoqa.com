import requests
from config.settings import API_BASE_URL

class BookStoreClient:
    ACCOUNT_BASE_PATH = API_BASE_URL + "/BookStore/v1"

    def get_all_books(self):
        return requests.get(self.ACCOUNT_BASE_PATH + "/Books")
    
    def get_book_by_isbn(self, isbn: str, ):
        params = {
            "ISBN": isbn
        }
        return requests.get(self.ACCOUNT_BASE_PATH + "/Book", params= params)

    def add_book(self, uid: str, isbn: str, token: str):
        payload = {
            "userId": uid,
            "collectionOfIsbns": [{ "isbn": isbn }]
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.post(self.ACCOUNT_BASE_PATH + "/Books", headers=headers ,json=payload)
    
    def delete_book(self, isbn: str, uid: str, token: str):
        payload = {
            "isbn": isbn,
            "userId": uid
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.delete(self.ACCOUNT_BASE_PATH + "/Book", headers=headers ,json=payload)
    
    def delete_all_books(self, uid: str, token: str):
        params = {
            "UserId": uid
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.delete(self.ACCOUNT_BASE_PATH + "/Books", params=params, headers=headers)
    
    def edit_book(self, isbn_old: str, uid: str, isbn_new, token: str):
        payload= {
            "userId": uid,
            "isbn": isbn_new
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }
        return requests.put(self.ACCOUNT_BASE_PATH + f"/Books/{isbn_old}", headers=headers,json=payload)