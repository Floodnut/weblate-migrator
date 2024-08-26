import requests

class HttpClient:
    def __init__(self, base_url: str, key: str):
        self.base_url = base_url
        self.key = key
        self.headers = {
            'Authorization': f'Token {self.key}',
            'Content-Type': 'application/json',
        }
        
    def get(self):
        return requests.get(url = self.base_url,headers=self.headers)

    def post(self, data: dict):
        return requests.post(url = self.base_url, headers=self.headers, json = data)
    
    def put(self, data: dict):   
        return requests.put(url = self.base_url, headers=self.headers, json = data)
    
    def patch(self, data: dict):
        return requests.patch(url = self.base_url, headers=self.headers, json = data)
    
    def delete(self):
        return requests.delete(url = self.base_url, headers=self.headers)