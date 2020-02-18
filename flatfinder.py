from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Integer, Date

base = declarative_base()

engine = db.create_engine('postgresql+psycopg2://postgres:password@localhost:5433/flats')
#engine.connect()


driver  = webdriver.Chrome("\webdrver\chromedriver.exe")

flats = []
prices = []
market_cap = []
driver.get("https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/gdansk/?search%5Bdistrict_id%5D=99")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

def find_flat():
    for a in soup.find('table', attrs={'id':'offers_table'}).find_all('td', attrs = {'class':'offer'}):
        name = a.find('a', href=True,  attrs = {'class':'marginright5 link linkWithHash detailsLink'})
        price = a.find('p', attrs = {'class':'price'})
        if name is not None and price is not None:
            unified_name =  name.text.replace('\n', '')
            flats.append(unified_name)
            unified_price = price.text.replace('\n', '')
            prices.append(unified_price)
            new_flat(unified_name, unified_price)

    out_table = dict(zip(flats,prices))
    print(out_table)

Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

class User(base):

    __tablename__ = 'flat'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)

    def __init__(self , name, price):
        self.name = name
        self.price = price

def new_flat(name, price):
    user = User(f"{name}", f"{price}")
    session.add(user)
    session.commit()
#db.sql.expression.insert(flat, flats)
find_flat()