import time
from datetime import datetime as dt
import requests
import selectorlib

URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(URL):
    response = requests.get(URL, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract_temp.yaml")
    value = extractor.extract(source)["home"] # "tours" is the key of dict
    return value

def store(extracted):
    #now = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    with open("data.txt", "a") as file:
        #line = f"{now},{extracted}\n"
        file.write(extracted + "\n")

if __name__ == "__main__":
    scraped = scrape(URL)
    #print(scraped)
    extracted = extract(scraped)
    #print(dt.now().strftime("%Y_%m_%d-%H_%M_%S")+ "," + extracted)
    store(dt.now().strftime("%Y_%m_%d-%H_%M_%S")+ "," + extracted)
    time.sleep(2)


