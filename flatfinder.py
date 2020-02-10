from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

driver  = webdriver.Chrome("\webdrver\chromedriver.exe")

coins = []
prices = []
market_cap = []
driver.get("https://coinmarketcap.com/")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
myString = "&nbsp;"

for a in soup.find_all('tr', attrs = {'class':'cmc-table-row'}):
    name = a.find('div', attrs = {'class':'cmc-table__column-name sc-1kxikfi-0 eTVhdN'}).find('a', attrs = {'class':'cmc-link'})
    price = a.find('td', attrs = {'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).find('a', attrs = {'class':'cmc-link'})
    volume = a.find('td', attrs = {'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).find('div', attrs = {'class':''})
    prices.append(price.text)
    coins.append(name.text)
    vol = volume.text
    vol1 = vol.replace(r'\xa',' ')
    market_cap.append(vol1)
money = zip(prices, market_cap)
out_table = dict(zip(coins,money))
print(out_table)
