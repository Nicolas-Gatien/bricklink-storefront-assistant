import requests
from requests_oauthlib import OAuth1

class BrickLink():
    def __init__(self, consumer_key, consumer_secret, token_value, token_secret) -> None:
        self.auth = OAuth1(consumer_key, consumer_secret, token_value, token_secret)
        self.url = 'https://api.bricklink.com/api/store/v1'
    
    def get_inventories(self) -> list:
        endpoint = f'{self.url}/inventories'
        response = requests.get(endpoint, auth=self.auth)
        data = response.json()['data']
        return data
    
    def get_catory_list(self) -> list:
        endpoint = f'{self.url}/categories'
        response = requests.get(endpoint, auth=self.auth)
        data = response.json()['data']
        return data
        