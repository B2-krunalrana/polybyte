import requests
login_url = "https://kite.zerodha.com/api/login"


# Payload for login request 
payload = {
    "user_id": "ranakrunal2704",
    "password": ""
}

# POST request to login
response = requests.post(login_url, json=payload)

# response status
if response.status_code == 200:
    print("Login successful!")
else:
    print("Login failed. Status code:", response.status_code)
    print("Response content:", response.text)
