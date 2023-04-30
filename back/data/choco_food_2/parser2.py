from bs4 import BeautifulSoup
import csv
import re


with open('rest2.html', 'r') as f:
    page = f.read()

soup = BeautifulSoup(page, 'html.parser')

restaurants = soup.find_all(class_="restaurant--container")

with open('restaurant2.csv', 'a') as f:
    id = 5
    cat_id = 59
    prod_id = 689
    prod_cat_id = 59
    restaurant_category = 1
    for rest in restaurants:
        title = rest.find('h1', class_ = "title").text.strip()
        desc = ""
        address = ""
        img = rest.find('img', alt = "restaurant preview")['src']
        delivery_time = int(re.search(r'(\d+)', rest.find(class_ = 'delivery-time').text).group())
        delivery_price = 600
        

        with open('prod_category2.csv', 'a') as d:
            
            prods = rest.find_all(class_ = 'foodtypes-list__item__caption')
            for i in prods:
                c_title = i.text
                icon = ""
                writer = csv.writer(d, delimiter=";")
                writer.writerow([cat_id, c_title, icon, id])
                cat_id += 1
            
        with open('product2.csv', 'a') as e:
            products = rest.find_all(class_='foodset__box')
            writer = csv.writer(e, delimiter=";")

            for j in products:
                items = j.find_all(class_ = 'food')

                for item in items:
                        
                    p_title = item.find(class_ = "food__title").text.strip()
                    p_desc = item.find(class_ = "food__description__value").text.strip()
                    price = int(re.search(r'(\d+)', item.find(class_ = "food__price__discount").text).group())
                    try:
                        pre_img = item.find(class_ = "food__image")
                        p_img = pre_img.find('img')['data-src']
                        if "https" not in p_img:
                            # img = 'https://chocofood.kz/_nuxt/img/nophoto-400x300.8339c8b.png'
                            continue
                    except:
                        # img = 'https://chocofood.kz/_nuxt/img/nophoto-400x300.8339c8b.png'
                        continue
                    writer.writerow([prod_id, p_title, p_desc, price, p_img, prod_cat_id, id])
                    prod_id += 1
                prod_cat_id += 1
                    
        
        writer = csv.writer(f, delimiter=";")
        writer.writerow([id, title, desc, address, img, delivery_time, delivery_price, restaurant_category])
        restaurant_category = 8
        id += 1


