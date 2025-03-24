import json
from urllib.request import urlretrieve
from dotenv import dotenv_values

config = dotenv_values(".env")

api_key = config["GOOGLE_API_KEY"]
search_engine_id = config["GOOGLE_SEARCH_ENGINE_ID"]

url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&start=11&q=filetype:pdf"

path, headers = urlretrieve(url)
file = open(path, encoding="utf-8")
search = json.load(file)

for item in search["items"]:
  title = "pdf/" + item["title"][:32]
  pdf_path, headers = urlretrieve(item["link"], f"{title}.pdf")
  print(pdf_path)