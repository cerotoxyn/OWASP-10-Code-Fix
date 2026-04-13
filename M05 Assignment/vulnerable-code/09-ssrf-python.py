url = input("Enter URL: ")
response = requests.get(url)
print(response.text)