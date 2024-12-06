# import os
#
# import requests
# from dotenv import load_dotenv
#
# CODI_BASE_URL = "https://getcody.ai/api/v1"
#
# class Codi_Rest_API:
#
#     def __init__(self):
#         pass
#
#     def api_key(self):
#         load_dotenv()
#         return os.environ.get('CODI_API_KEY')
#
#     def auth_headers(self):
#         return f"Bearer {self.api_key()}"
#
#     def request(self, method, path, data=None):
#         headers = {'Authorization': self.auth_headers()}
#         url     = f"{CODI_BASE_URL}{path}"
#         return requests.request(method, url, headers=headers, json=data).json()
#
#     def request_get(self, path):
#         return self.request('GET', path)
#
#     # todo: add pagination support
#     def bots(self):
#         return self.request_get('/bots').get('data')
#
#     def conversations(self):
#         return self.request_get('/conversations').get('data')
#
#     def conversation(self, conversation_id):
#         return self.request_get(f'/conversations/{conversation_id}').get('data')
#
#     def documents(self):
#         return self.request_get('/documents').get('data')
