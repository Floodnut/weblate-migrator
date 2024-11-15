from typing import Optional
import requests

class HttpClient:
    def __init__(self, base_url: str, key: str):
        self.base_url = base_url
        self.key = key
        self.json_headers = {
            'Authorization': f'Token {self.key}',
            'Content-Type': 'application/json',
        }
        
        self.form_headers = {
            'Authorization': f'Token {self.key}',
        }
    
        
    def get(self, url: str):
        return requests.get(url = f'{self.base_url}/{url}', headers=self.json_headers)

    def post(self, url: str, data: Optional[dict] = None):
        return requests.post(url = f'{self.base_url}/{url}', headers=self.json_headers, json = data)
    
    def form_post(self, url: str, data: Optional[dict] = None, file_path: Optional[str] = None):
        if file_path:
            with open(file_path, 'rb') as _file:
                file = {'file': _file}
                return requests.post(url = f'{self.base_url}/{url}', headers=self.form_headers, files=file)
        
        return requests.post(url = f'{self.base_url}/{url}', headers=self.form_headers, data=data)
        
    def put(self, url: str, data: dict):   
        return requests.put(url = f'{self.base_url}/{url}', headers=self.json_headers, json = data)
    
    def patch(self, url: str, data: dict):
        return requests.patch(url = f'{self.base_url}/{url}', headers=self.json_headers, json = data)
    
    def delete(self, url: str):
        return requests.delete(url = f'{self.base_url}/{url}', headers=self.json_headers)
