import requests 
import http.client

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"2"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"39"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"528"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"45"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"48"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"61"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"143"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"140"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"135"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"78"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"3"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"1"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

querystring = {"id":"4"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=39&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=2&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=528&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=45&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=48&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=61&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=143&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests # type: ignore

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=140&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=135&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=78&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=1&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

# API endpoint and headers
url = 'https://api-football-v1.p.rapidapi.com/v3/teams?league=4&season=2024'
headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
}

# Making the HTTP GET request
response = requests.get(url, headers=headers)

# Handling the response
if response.status_code == 200:  # Check if the request was successful
    print(response.text)  # Print the API response (JSON string)
else:
    print(f"Failed to retrieve data: {response.status_code}")

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"39","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"2","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"528","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"61","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"143","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"140","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"135","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":"78","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"1","season":"2022"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"2","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"3","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"45","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"48","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

querystring = {"league":"4","season":"2024"}

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests

url = "https://api-football-v1.p.rapidapi.com/v3/timezone"

headers = {
	"x-rapidapi-key": "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())




def get_team_players(teamid):
    import http.client

conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

conn.request("GET", "/v3/players?team={teamid}&season={season}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


    
