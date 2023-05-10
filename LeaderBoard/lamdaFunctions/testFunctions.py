import requests


# data = requests.get(r"https://7zo46xcxefurhkuktmn7sjrvlm0flydm.lambda-url.us-east-2.on.aws/")
# print(data)

add = requests.post(r"https://7zo46xcxefurhkuktmn7sjrvlm0flydm.lambda-url.us-east-2.on.aws/", json={"username": "testNotin"})
print(add)