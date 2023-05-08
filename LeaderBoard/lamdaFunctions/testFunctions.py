import requests


data = requests.get(r"https://jpi6gndryx6spdpjad3fl2blgm0hpunb.lambda-url.us-east-2.on.aws/")
print(data)

add = requests.get(r"https://7zo46xcxefurhkuktmn7sjrvlm0flydm.lambda-url.us-east-2.on.aws/", data={"username": "Test"})
print(add)