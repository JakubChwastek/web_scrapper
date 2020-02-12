from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

engine = db.create_engine('postgresql://flats_db.sql')
engine.connect()


driver  = webdriver.Chrome("\webdrver\chromedriver.exe")

flats = []
prices = []
market_cap = []
driver.get("https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/gdansk/?search%5Bdistrict_id%5D=99")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

for a in soup.find('table', attrs={'id':'offers_table'}).find_all('td', attrs = {'class':'offer'}):
    name = a.find('a', href=True,  attrs = {'class':'marginright5 link linkWithHash detailsLink'})
    price = a.find('p', attrs = {'class':'price'})
    if name is not None:
        unified_name =  name.text.replace('\n', '')
        flats.append(unified_name)
    if price is not None:
        unified_price = price.text.replace('\n', '')
        prices.append(unified_price)

out_table = dict(zip(flats,prices))
print(out_table)
