# import requests
# import json
#
# while True:
#     response = requests.post("http://127.0.0.1:8000/webmoni/api/domain_all/")
#     for i in json.loads(response.text)['data']:
#         if i['cert_valid_days'] == None  and i['cert_valid_date'] == None and i['status_id'] != 100:
#
#     # print(json.loads(response.text))
#
#     exit()