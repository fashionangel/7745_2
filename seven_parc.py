import time
import os
import logging
import getpass
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

logging.basicConfig(                           
    filename='7745_stat.log',
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True,
    encoding='utf-8'
)

class Parser:

    def __init__(self, link):
        self.link = link
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)
        self.username = getpass.getuser()
        self.script_name = os.path.basename(sys.argv[0])
        self.info_list = []
        self.links_list = []
        self.clear_ads = []
        self.date_dict = {}

    def switchOptions(self):
            proxies = [
                'http://13.80.134.180:80',
                'http://37.120.189.106:80',
                'http://51.38.231.41:80',
                'http://104.248.207.60:80',
            ]
            proxy = random.choice(proxies)
            logging.info(f"Использую прокси: {proxy}")
    
            options = Options()
            options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT {random.uniform(1.0, 5.0)}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36')
            options.add_argument(f'--proxy-server={proxy}')
    
            self.driver = webdriver.Chrome(options=options)

    def accept_cookie(self):
        logging.info(f"Начало | Пользователь: {self.username} | Скрипт: {self.script_name}")
        try:
            clickable_element = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.ID, "dldkdAccept"))
            )
            clickable_element.click()
            logging.info("cookie-баннер закрыт")
        except Exception:
            logging.exception("Не удалось закрыть cookie-баннер")

    def electro_choice(self):
        logging.info("Кликаю фильтр 'Электро'")
        try:
            clickable_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[5]/div/div/main/div[2]/div[2]/aside/div[1]/form/div[5]/div[2]/div[2]/label"))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            logging.info("Фильтр 'Электро' применён")
        except Exception:
            logging.exception("Ошибка при выборе фильтра 'Электро'")

    def power(self):
        logging.info("Кликаю фильтр мощности (1)")
        try:
            clickable_element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[7]/div[2]/div[1]/label/span[1]/span"))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            logging.info("Фильтр мощности (1) применён")
        except Exception:
            logging.exception("Ошибка при выборе фильтра мощности (1)")

    def power_second(self):
        logging.info("Кликаю фильтр мощности (2)")
        try:
            clickable_element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[7]/div[2]/div[2]/label/span[1]/span"))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            logging.info("Фильтр мощности (2) применён")
        except Exception:
            logging.exception("Ошибка при выборе фильтра мощности (2)")

    def mange(self):
        logging.info("Кликаю фильтр 'Mange'")
        try:
            clickable_element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[12]/div[2]/div[9]/label/span[1]/span"))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            logging.info("Фильтр 'Mange' применён")
        except Exception:
            logging.exception("Ошибка при выборе фильтра 'Mange'")

    def show_product(self):
        logging.info("Нажимаю кнопку 'Показать товары'")
        try:
            clickable_element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[22]/button[1]"))
            )
            clickable_element.click()
            logging.info("Кнопка 'Показать товары' нажата")
        except Exception:
            logging.exception("Ошибка при нажатии кнопки 'Показать товары'")

    def get_all_links_on_page(self):
        logging.info("Собираю ссылки со страницы")
        try:
            elements = self.driver.find_elements(By.CLASS_NAME, value='block')
        except Exception:
            logging.exception("Не удалось получить элементы со страницы")
            return []

        self.links_list = []
        for element in elements:
            href = element.get_attribute('href')
            if href is not None:
                self.links_list.append(href)

        self.clear_ads = [item for item in self.links_list
                          if item is not None and '/product/' in item]


        self.clear_ads = self.clear_ads[1:]

        logging.info(f"Всего ссылок найдено: {len(self.links_list)} | "
                     f"товаров после фильтрации: {len(self.clear_ads)}")
        return self.clear_ads

    def get_info(self):
        words = ['Основные характеристики', 'Особенности', 'Функции',
                 'Защита', 'Габариты и вес', 'Габариты упаковки']

        total = len(self.clear_ads)
        logging.info(f"Начинаю парсинг объявлений: {total} шт.")

        for link in self.clear_ads:
            self.info_list = []
            logging.info(f"Обрабатываю: {link}")

            try:
                self.driver.get(link)
                time.sleep(3)

                tabble_list = self.driver.find_elements(By.TAG_NAME, 'td')
                for table in tabble_list:
                    try:
                        tabblee_list = table.find_element(By.TAG_NAME, 'span')
                        if tabblee_list.text:
                            self.info_list.append(tabblee_list.text)
                    except Exception:
                        if table.text:
                            self.info_list.append(table.text)

                self.info_list = [i for i in self.info_list if i not in words]

                self.date_dict[link] = {}
                for i in range(0, len(self.info_list)):
                    if i % 2 == 0 and i + 1 < len(self.info_list):
                        self.date_dict[link][self.info_list[i]] = self.info_list[i + 1]

                print(self.date_dict[link])

            except Exception:
                logging.exception(f"Ошибка при обработке {link}")
                continue

            time.sleep(3)

        logging.info(f"Парсинг завершён. Успешно обработано: {len(self.date_dict)} из {total}")

    def creating_csv_file(self):
        logging.info("Формирую CSV-файл")
        try:
            df_1 = pd.DataFrame(self.date_dict).T
            df_1.index.name = "link"
            df_1.to_csv("var.csv", index=True, encoding='utf-8-sig')
            logging.info(f"CSV сохранён: var.csv | строк: {len(df_1)} | колонок: {len(df_1.columns)}")
        except Exception:
            logging.exception("Не удалось сохранить CSV")



