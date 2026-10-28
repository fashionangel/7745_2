import time
import os
import logging
import getpass
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

logging.basicConfig(                            #настройка логера
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

    def accept_cookie(self):
        clickable_element = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.ID, "dldkdAccept"))
        )
        clickable_element.click()

    def electro_choice(self):
        clickable_element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[5]/div/div/main/div[2]/div[2]/aside/div[1]/form/div[5]/div[2]/div[2]/label"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    def power(self):
        clickable_element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[7]/div[2]/div[1]/label/span[1]/span"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    def power_second(self):
        clickable_element = WebDriverWait(self.driver, 3).until(
           EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[7]/div[2]/div[2]/label/span[1]/span"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    def mange(self):
        clickable_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[12]/div[2]/div[9]/label/span[1]/span"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    def show_product(self):
        clickable_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='catalog-filter-form']/div[22]/button[1]"))
        )
        clickable_element.click()

    def get_all_links_on_page(self):
        elements = self.driver.find_elements(By.CLASS_NAME, value='block')

        self.links_list = []
        for element in elements:
            href = element.get_attribute('href')
            if href is not None:
                self.links_list.append(href)

        # clear_ads: оставляем только ссылки на товары
        self.clear_ads = []
        for item in self.links_list:
            if item is not None and r'/product/' in item:
                self.clear_ads.append(item)

        # первая ссылка не нужна
        self.clear_ads = self.clear_ads[1:]

        return self.clear_ads

    def get_info(self):
        words = ['Основные характеристики', 'Особенности', 'Функции',
                'Защита', 'Габариты и вес', 'Габариты упаковки']

        for link in self.clear_ads:
            self.info_list = []
            self.driver.get(link)
            time.sleep(3)

            tabble_list = self.driver.find_elements(By.TAG_NAME, 'td')
            for table in tabble_list:
                try:
                    tabblee_list = table.find_element(By.TAG_NAME, 'span')
                    if tabblee_list.text == '':
                        pass
                    else:
                        self.info_list.append(tabblee_list.text)
                except Exception:
                    if table.text == '':
                        pass
                    else:
                        self.info_list.append(table.text)

            self.info_list = [i for i in self.info_list if i not in words]

            self.date_dict[link] = {}
            for i in range(0, len(self.info_list)):
                if i % 2 == 0 and i + 1 < len(self.info_list):
                    self.date_dict[link][self.info_list[i]] = self.info_list[i + 1]

            time.sleep(3)
            print(self.date_dict[link])

    def creating_csv_file(self):
        df_1 = pd.DataFrame(self.date_dict).T
        df_1.index.name = "link"
        df_1.to_csv("var.csv", index=True, encoding='utf-8-sig')