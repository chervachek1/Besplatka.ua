import openpyxl
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import lxml

headers = {
    'accept': '*/*',
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

def get_numbers():
    try:
        ser = Service('C:/Users/kusmi/Desktop/Data Science/besplatka/chromedriver.exe')
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(service=ser, options=op)
        #get_all_url = []
        #for i in range(1, 20):
            #url = f'https://besplatka.ua/electronika-i-bitovaya-tehnika/smartfone-telefone/page/{i}'
            #r = requests.get(url=url, headers=headers)
            #src = r.text
            #soup = BeautifulSoup(src, 'lxml')
            #get_url = soup.find_all(class_='fl-100 d-title')
            #for url in get_url:
                #a_url = url.find('a').get('href')
                #all_url = f'https://besplatka.ua{a_url}'
                #get_all_url.append(all_url)
        #with open('all_url.json', 'w') as file:
            #json.dump(get_all_url, file, indent=4, ensure_ascii=False)

        with open('all_url.json') as file:
            all_get_url = json.load(file)

        x = 2
        excel_file = openpyxl.load_workbook('besplatka_numbers.xlsx')
        work_sheet = excel_file['Лист1']

        for url in all_get_url:
            driver.get(url)
            time.sleep(5)
            driver.set_window_size(1552, 840)
            try:
                driver.find_element(By.CSS_SELECTOR, ".enc-phone").click()
            except: pass
            time.sleep(1)
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            try:
                number = soup.find(class_='title-phones').text
                work_sheet['B' + str(x)] = number
                city = str(soup.find(class_='a-7f7').text).replace('Оголошення ', '')
                work_sheet['A' + str(x)] = city
            except:
                pass
            x += 1
        excel_file.save(filename='besplatka_numbers.xlsx')
    except Exception as ex:
        excel_file.save(filename='besplatka_numbers.xlsx')
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    get_numbers()

if __name__ == '__main__':
    main()