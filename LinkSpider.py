import os

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import csv
import time
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import GetDataFunc

from fileFunc import *


def main():
    username = input("Linkedin Username: ")
    password = input("Linkedin Password: ")
    path = 'input.xls'
    fileName = 'output.xls'
    if os.path.isfile(fileName):
        print('start')
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('chromedriver', options=chrome_options)

    driver.get('https://www.linkedin.com/')
    driver.set_page_load_timeout(100)
    driver.find_element_by_name("session_key").send_keys(username)
    driver.find_element_by_name("session_password").send_keys(password)
    driver.find_element_by_class_name("sign-in-form__submit-btn").click()

    search_List = open_file(path)
    index = 0
    for search_pro in search_List:
        index += 1
        print("进行到第"+str(index)+"位")
        search_name = search_pro[0]
        print("search_name: " + search_name)
        keyWord = search_name.replace(" ", "%20")
        '''
        searchURL = 'https://www.linkedin.com/search/results/people/?' \
                    'facetGeoRegion=%5B%22us%3A0%22%5D&facetIndustry=%5B%22106%22%2C%2243%' \
                    '22%2C%2241%22%2C%2242%22%2C%2246%22%2C%2245%22%2C%22129%22%5D' '&keywords=' \
                    + keyWord + '&origin=FACETED_SEARCH' + '&page=1'
        '''
        searchURL = 'https://www.linkedin.com/search/results/people/?keywords='+ keyWord +'&origin=GLOBAL_SEARCH_HEADER'
        print("searchURL: "+searchURL)

        have_result = 1
        driver.get(searchURL)
        if driver.find_elements_by_css_selector(".search-no-results"):
            print("no results")
            have_result = 0;
            edit_file(fileName, [search_name, "no results",searchURL])

        if have_result == 1:
            print("here")
            driver.implicitly_wait(10)

            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.search-result__info'))
            WebDriverWait(driver, 30).until(element_present)

            results = driver.find_elements_by_css_selector(".search-result__info")
            temp_link = results[0].find_element_by_css_selector('a').get_attribute('href')
            if '/in/' in temp_link:
                personal_link = temp_link
                print("personal_link: " + personal_link)
                GetDataFunc.getPersonalData(driver, personal_link, search_name, fileName)
            else:
                print("no access")
                edit_file(fileName,[search_name, searchURL, "no access"])


if __name__ == '__main__':
    main()

