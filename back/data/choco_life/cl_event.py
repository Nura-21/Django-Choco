from bs4 import BeautifulSoup
import csv
import requests
import re
import datetime


# id title image discount alert_info expiration_date use_until_date total_bought_amount category_id company_id

def get_date(s):
    x = re.search(r'(\d.*\d)', s)
    t = x.group(1)
    dic = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12
    }
    l = t.split(" ")
    date = datetime.date(int(l[2]), dic[l[1]], int(l[0]))
    return date


category_id = 0
company_id = 0
certificate_id = 0
event_id = 0

pages = {
    0: [
        "https://chocolife.me/56940-ledoviy-kompleks-almaty-arena/",
        "https://chocolife.me/56927-alem-kids/",
        "https://chocolife.me/55088-park-nasledniki-v-trts-sputnik/",
        "https://chocolife.me/55085-park-nasledniki-v-trk-maxima/"
    ],
    1: [
        "https://chocolife.me/56937-organic-space/",
        "https://chocolife.me/39184-podarochnie-karty-chocolifeme/",
        "https://chocolife.me/56842-animatory-adali-project/",
        "https://chocolife.me/56927-alem-kids/",
    ],
    2: [
        "https://chocolife.me/56493-stomatologiya-saradan/",
        "https://chocolife.me/56494-stomatologiya-saradan/",
        "https://chocolife.me/56127-stomatologicheskaya-klinika-almaty-dent/",
        "https://chocolife.me/56931-reabilitatsionniy-meditsinskiy-tsentr-daua/"
    ],
    3: [
        "https://chocolife.me/55033-platinum-spa/",
        "https://chocolife.me/56338-master-olga/",
        "https://chocolife.me/56942-studiya-sacave/",
        "https://chocolife.me/56934-studiya-yesya-sugar/"
    ],
    4: [
        "https://chocolife.me/54639-sport-complex-qazaqstan/",
        "https://chocolife.me/54441-s-fitness-na-seyfullina/",
        "https://chocolife.me/56720-set-magazinov-prokata-skadi/",
        "https://chocolife.me/56727-set-sportivnykh-magazinov-extremal/"
    ]
}

for key, value in pages.items():
    category_id = key
    for j in range(0, len(value)):
        try:
            page = requests.get(value[j])
            soup = BeautifulSoup(page.content, 'html.parser')
            i = soup.select('cl-deals-detail')[0]

            title = i.find(class_="d-detail__heading").text

            image = i.find("img")['src']

            discount = int(re.search(r'\d+', i.find(class_="dd-tag--favourite").text).group())
            alert_info = i.find(class_="cl-info__terms").text
            dates = i.find_all(class_="dd-tag--circle")
            expiration = get_date(dates[0].text)
            until = get_date(dates[1].text)
            total_bought = int(re.search(r'\d+', i.find(class_="d-detail__stat").select("em")[0].text).group())

            company_title = i.find(class_="d-detail__desc").text
            company_desc = i.find(class_="cl_info__article").text
            sale_points = i.find(class_="cl-info__contacts").text

            certificates = i.find_all(class_="ddi-choose")

            if len(certificates) > 3:
                for k in range(0, 3):
                    c_title = certificates[k].find(class_="ddi-choose__title").text
                    c_txt = certificates[k].find_all(class_="ddi-choose__text")
                    c_discount = int(re.search(r'\d+', c_txt[0].text).group())
                    c_bought = int(re.search(r'\d+', c_txt[1].text).group())

                    c_prices = certificates[k].find_all(class_="ddi-choose__price")
                    c_initial = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[0].text).group().split()))
                    try:
                        c_final = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[1].text).group().split()))
                    except:
                        c_final = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[0].text).group().split()))

                    with open("certificate.csv", "a") as d:
                        writer = csv.writer(d, delimiter=';')
                        writer.writerow([certificate_id, c_title, c_discount, c_bought, c_final, event_id])
                        certificate_id += 1
            else:
                for k in range(0, len(certificates)):
                    c_title = certificates[k].find(class_="ddi-choose__title").text
                    c_txt = certificates[k].find_all(class_="ddi-choose__text")
                    c_discount = int(re.search(r'\d+', c_txt[0].text).group())
                    c_bought = int(re.search(r'\d+', c_txt[1].text).group())

                    c_prices = certificates[k].find_all(class_="ddi-choose__price")
                    c_initial = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[0].text).group().split()))
                    try:
                        c_final = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[1].text).group().split()))
                    except:
                        c_final = int(''.join(re.search(r'\d+ \d+|\d+', c_prices[0].text).group().split()))

                    with open("certificate.csv", "a") as d:
                        writer = csv.writer(d, delimiter=';')
                        writer.writerow([certificate_id, c_title, c_discount, c_bought, c_final, event_id])
                        certificate_id += 1

            # with open('company.csv', 'a') as c:
            #     writer = csv.writer(c, delimiter=';')
            #     writer.writerow([company_id, company_title, company_desc, sale_points])

            with open('event.csv', 'a') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    [event_id, title, image, discount, alert_info, expiration, until, total_bought, category_id,
                     company_id])
                event_id += 1
                company_id += 1
        except:
            print(value[j])
