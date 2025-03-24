import json
from urllib.request import urlretrieve
from dotenv import dotenv_values
from unicodedata import normalize
from re import sub

config = dotenv_values(".env")

api_key = config["GOOGLE_API_KEY"]
search_engine_id = config["GOOGLE_SEARCH_ENGINE_ID"]
start_index = 100

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = normalize('NFKC', value)
    else:
        value = normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = sub(r'[^\w\s-]', '', value.lower())
    return sub(r'[-\s]+', '-', value).strip('-_')

def get_search_results(start):
  url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&start={start}&q=filetype:pdf"
  path, headers = urlretrieve(url)
  file = open(path, encoding="utf-8")
  return json.load(file)

def has_next_page(search):
  return "nextPage" in search["queries"]

def total_results(search):
   return int(search["searchInformation"]["totalResults"])

if __name__=="__main__":
  search = get_search_results(start_index)
  print(search["searchInformation"])

  for i in range(start_index + 10, total_results(search), 10):
    for item in search["items"]:
      title = "pdf/" + slugify(item["title"])
      pdf_path, headers = urlretrieve(item["link"], f"{title}.pdf")
      print(pdf_path)

    search = get_search_results(i)
    if not has_next_page(search):
      break
    else:
       print(search["searchInformation"])