import requests, time
from config.settings import API_BASE_URL
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class AccountClient:
    ACCOUNT_BASE_PATH = f"{API_BASE_URL}/Account/v1"

    def __init__(self):
        self.session = requests.Session()
        # ตั้งค่า Retry: ลองใหม่ 3 ครั้ง ถ้าเจอ Status 500, 502, 503, 504
        # โดยการรอจะค่อยๆ เพิ่มขึ้น (backoff_factor)
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,  # รอ 2s, 4s, 8s ระหว่างการรอแต่ละครั้ง
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def create_user(self, username: str | None = None, password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return self.session.post(self.ACCOUNT_BASE_PATH + "/User", json=payload)
    
    def generate_token(self, username: str | None = None , password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return self.session.post(self.ACCOUNT_BASE_PATH + "/GenerateToken", json=payload)

    def user_authorization(self, username: str | None = None, password: str | None = None):
        payload = {
            "userName": username,
            "password": password
        }
        return self.session.post(self.ACCOUNT_BASE_PATH + "/Authorized", json=payload)
    
    def get_user_by_uid(self, uid: str | None = None, token: str | None = None):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return self.session.get(self.ACCOUNT_BASE_PATH + f"/User/{uid}", headers=headers)

    def delete_user_by_uid(self, uid:str | None = None, token: str | None = None):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return self.session.delete(self.ACCOUNT_BASE_PATH + f"/User/{uid}", headers=headers)