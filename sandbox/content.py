import requests
import justext

url = input("Enter any url: ")
response = requests.get(url)

paragraphs = justext.justext(response.content, justext.get_stoplist("English"))

for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
        print(paragraph.text)
