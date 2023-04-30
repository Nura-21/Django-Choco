from bs4 import BeautifulSoup
import requests
import re

page = requests.get('https://chocolife.me/56107-karaoke-lyubimoe-plus/')
soup = BeautifulSoup(page.content, 'html.parser')

certificates = soup.find_all(class_ = 'ddi-choose')

for i in range(0, 3):
    c_title = certificates[i].find(class_= "ddi-choose__title").text
    c_txt = certificates[i].find_all(class_ = "ddi-choose__text")
    c_discount = int(re.search(r'\d+', c_txt[0].text).group())
    c_bought = int(re.search(r'\d+', c_txt[1].text).group())

    c_prices = certificates[i].find_all(class_ = "ddi-choose__price")
    c_initial = int(''.join(re.search(r'\d+ \d+', c_prices[0].text).group().split()))
    c_final = int(''.join(re.search(r'\d+ \d+', c_prices[1].text).group().split()))
    print(c_title, c_discount, c_bought, c_initial, c_final)
    
