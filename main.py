import time
from datetime import datetime as dt
import requests
import selectorlib
import sqlite3

URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db")

def scrape(URL):
    response = requests.get(URL, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract_temp.yaml")
    value = extractor.extract(source)["home"]
    return value

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperature VALUES(?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split()
    row = [item.strip() for item in row]
    date, temperature = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM temperature WHERE date=? AND temperature=?", (date, temperature))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    scraped = scrape(URL)
    time.sleep(3)
    extracted = extract(scraped)
    row = dt.now().strftime("%Y_%m_%d-%H_%M_%S")+ "," + extracted
    store(row)