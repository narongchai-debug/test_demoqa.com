import requests
from config.settings import API_BASE_URL

class AccountClient:
    ACCOUNT_BASE_PATH = f"{API_BASE_URL}/Account/v1"

    def create_user(self, username: str | None = None, password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return requests.post(self.ACCOUNT_BASE_PATH + "/User", json=payload)
    
    def generate_token(self, username: str | None = None , password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return requests.post(self.ACCOUNT_BASE_PATH + "/GenerateToken", json=payload)

    def user_authorization(self, username: str | None = None, password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return requests.post(self.ACCOUNT_BASE_PATH + "/Authorized", json=payload)
    
    def get_user_by_uid(self, uid: str | None = None, token: str | None = None):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return requests.get(self.ACCOUNT_BASE_PATH + f"/User/{uid}", headers=headers)

    def delete_user_by_uid(self, uid:str | None = None, token: str | None = None):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return requests.delete(self.ACCOUNT_BASE_PATH + f"/User/{uid}", headers=headers)