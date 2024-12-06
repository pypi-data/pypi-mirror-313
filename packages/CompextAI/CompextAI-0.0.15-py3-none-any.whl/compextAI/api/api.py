import requests

class APIClient:
    """
    A class to make HTTP requests to the Compext AI API.
    """
    def __init__(self, base_url:str, api_key:str, timeout:int=10, retries:int=3):
        self.base_url = base_url + "/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.timeout = timeout
        self.retries = retries
    # set timeout for all the requests and retry if the request times out 
    def get(self, route:str, data:dict={},**kwargs):
        for _ in range(self.retries):
            try:
                response = requests.get(self.base_url + route, headers=self.headers, json=data, timeout=self.timeout, **kwargs)
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
            except requests.exceptions.Timeout:
                continue
        return {
            "status": 500,
            "data": {}
        }
    
    def post(self, route:str, data:dict={},**kwargs):
        for _ in range(self.retries):
            try:
                response = requests.post(self.base_url + route, headers=self.headers, json=data,timeout=self.timeout, **kwargs)
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
            except requests.exceptions.Timeout:
                continue
        return {
            "status": 500,
            "data": {}
        }
    
    def put(self, route:str, data:dict={},**kwargs):
        for _ in range(self.retries):
            try:
                response = requests.put(self.base_url + route, headers=self.headers, json=data,timeout=self.timeout, **kwargs)
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
            except requests.exceptions.Timeout:
                continue
        return {
            "status": 500,
            "data": {}
        }

    def delete(self, route:str, data:dict={},**kwargs):
        for _ in range(self.retries):
            try:
                response = requests.delete(self.base_url + route, headers=self.headers, json=data,timeout=self.timeout, **kwargs)
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
            except requests.exceptions.Timeout:
                continue
        return {
            "status": 500,
            "data": {}
        }

