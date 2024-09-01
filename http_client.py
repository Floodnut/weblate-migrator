from typing import List, Optional
import requests

class HttpClient:
    def __init__(self, base_url: str, key: str):
        self.base_url = base_url
        self.key = key
        self.headers = {
            'Authorization': f'Token {self.key}',
            'Content-Type': 'application/json',
        }
        
    def get(self, url: str):
        return requests.get(url = f'{self.base_url}/{url}', headers=self.headers)

    def post(self, url: str, data: Optional[dict] = None, file_path: Optional[str] = None):
        if file_path is None:
            return requests.post(url = f'{self.base_url}/{url}', headers=self.headers, json = data)
        
        return requests.post(url = f'{self.base_url}/{url}', headers=self.headers, json = data, files = {'file': open(file_path, 'rb')})
    
    def put(self, url: str, data: dict):   
        return requests.put(url = f'{self.base_url}/{url}', headers=self.headers, json = data)
    
    def patch(self, url: str, data: dict):
        return requests.patch(url = f'{self.base_url}/{url}', headers=self.headers, json = data)
    
    def delete(self, url: str):
        return requests.delete(url = f'{self.base_url}/{url}', headers=self.headers)
