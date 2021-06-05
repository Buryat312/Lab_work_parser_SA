import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd 


class Writer:
    def __init__(self, products):
        self.prodDF = pd.DataFrame(
            {'product_name': products.product_names, 
            'product_link': products.product_links,
            'category': products.categories}
        )
    def write_to_xlsx(self):
        writer = pd.ExcelWriter('products.xlsx', engine='xlsxwriter')
        self.prodDF.to_excel(writer, sheet_name='Product', index=False)
        writer.save()

    def write_to_csv(self):
        csvFileContents = self.prodDF.to_csv(index=False)
        with open("products.csv", "w", encoding='utf-8') as f:
            f.write(csvFileContents)

class Products:
    def __init__(self, products):
        self.products = products

        self.product_names = []
        self.product_links = []
        self.categories = []


        for prod in products:
            self.product_names.append(prod.product_name)
            self.product_links.append(prod.product_link)
            self.categories.append(prod.category)

def writer(data):
    with open('lab_kivano.csv', 'a') as file:
        write = csv.writer(file)
        return write.writerow((
            data
        ))

class Kivano:
    def __init__(self, product_name, product_link, category):
        self.product_name = product_name
        self.product_link = product_link
        self.category = category

# data = []

def get_data(url):
    response = requests.get(url)
    html =response.text
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='list-view').find_all_next('div', class_='item')
    url = 'https://www.kivano.kg'
    for ad in ads:
        try:
            product_name = ad.find('div', class_='listbox_title').text
        except:
            product_name = 'Нет имени'
        try:
            product_link = ad.find('div', class_='listbox_title').find('a').get('href')
        except:
            product_link = 'Нет линка'
        try:
            category = soup.find('div', class_='product-index').find('div', class_='portlet-title').find('ul', class_='breadcrumb2').find('li', itemprop="itemListElement")[2].find('a').get('href')
            category = category.strip()
        except:
            category = 'Другое'
        
        # data.append(product_name)
        # data.append(product_link)
        # data.append(category)
        data = [
            product_name,
            url + product_link,
            category,
        ]
        print(data)
        writer(data)

# exmpl = []
def main():

    url1 = f'https://www.kivano.kg/bytovaya-tekhnika'
    url2 = f'https://www.kivano.kg/sport-i-otdykh'
    url3 = 'https://www.kivano.kg/kompyutery'
    url4 = 'https://www.kivano.kg/periferiya'
    all_url = []
    all_url.append(url1)
    all_url.append(url2)
    all_url.append(url3)
    all_url.append(url4)
    page_part = '?page='
    for url in all_url:
        for i in range(1, 4):
            url_gen = url + page_part + str(i)
            # print(url_gen)   #ВЫТАСКИВАЕТ 3 СТР С КАЖДОГО САЙТА
            # print(get_data(url_gen))
            get_data(url_gen)
            # exmpl.append(Kivano(data[0]), data[1], data[2])
            # print(exmpl)


if __name__ == '__main__':
    main()