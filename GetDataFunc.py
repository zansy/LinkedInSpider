# coding=utf-8
import csv
import json
import re
from time import sleep

from bs4 import BeautifulSoup

from fileFunc import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def getPersonalData(driver, personal_link, search_name, file_path):
    driver.get(personal_link)
    driver.set_page_load_timeout(30)
    html = driver.page_source
    #driver.implicitly_wait(3)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)*3/5);")
    try:
        scroll_element2 = driver.find_element_by_css_selector(".education-section")
        scroll_element2.location_once_scrolled_into_view
    except:
        pass

    soup = BeautifulSoup(html, "html.parser")
    json_alldata = soup.find_all("code")
    type(json_alldata)
    for x in json_alldata:
        try:
            json_data = json.loads(x.text)
        except ValueError:
            pass
        if "data" in json_data:
            if "$type" in json_data["data"]:
                if json_data["data"]["$type"] == "com.linkedin.voyager.identity.profile.ProfileView":
                    break

    name = headline = industry = location = summary = vanity_url = website = email = phone = "None"
    first_name = last_name = pro_title = pro_company = location = pro_school = follow_num = ''
    for x in json_data["included"]:
        if x["$type"] == "com.linkedin.voyager.identity.profile.Profile":
            try:
                name = x["firstName"] + " " + x["lastName"]
                print("name: " + name)
            except:
                pass

            try:
                headline = x["headline"]
                print("headline: " + headline)
                temp = headline.split(" at ")
                pro_title = temp[0]
                pro_company = temp[1]
            except:
                pass

            try:
                industry = x["industryName"]
                print("industry: " + industry)
            except:
                pass

            try:
                location = x["locationName"]
                print("location: " + location)
            except:
                pass

    new_html = driver.page_source
    soup = BeautifulSoup(new_html, "html.parser")

    # More experience Button
    try:
        expButtonDivList = driver.find_elements_by_css_selector(".pv-profile-section__actions-inline")
    except:
        pass

    for expButtonDiv in expButtonDivList:
        try:
            expButton = expButtonDiv.find_element_by_xpath(".//button")
            while expButton.get_attribute('aria-expanded') != 'true':
                expButton.send_keys(u'\ue007');
                expButton = expButtonDiv.find_element_by_xpath(".//button")
        except:
            pass



    try:
        summary_List = [search_name, personal_link, name, pro_title, pro_company, industry, location];
        edit_file(file_path, summary_List)
    except:
        print("summary_List write error")
        pass

    exp_sector = soup.find("section", "experience-section")
    if exp_sector:
        edit_file(file_path, [" ","EXP"])
        for each_exp in exp_sector.select(".pv-entity__position-group-pager"):
            print("****")
            print(each_exp.text.replace("\n\n", ""))
            same_company_group = each_exp.find("div", "pv-entity__company-details")

            if same_company_group:
                company_name = same_company_group.h3.findAll("span")[1].text
                for different_position_exp in each_exp.select(".pv-entity__summary-info-v2"):
                    row = [" ",company_name]
                    htag = different_position_exp.findAll(re.compile(r'h\d+'))
                    for h in htag:
                        current_information = h.findAll("span")[1].text
                        row.append(current_information)
                    edit_file(file_path, row)

            else:
                title = companyName = employdDates = start_date = end_date = duration = location = "null"
                each_exp = each_exp.find("div", "pv-entity__summary-info").text.replace("\n", "")

                title = each_exp.split("Company Name")[0]
                if len(each_exp.split("Company Name")) > 1:
                    theRest = each_exp.split("Company Name")[1]

                companyName = theRest.split("Dates Employed")[0]
                if len(theRest.split("Dates Employed")) > 1:
                    theRest = theRest.split("Dates Employed")[1]

                employdDates = theRest.split("Employment Duration")[0]
                list = employdDates.split("–")
                start_date = list[0]
                if len(list) > 1:
                    end_date = list[1]
                else:
                    end_date = start_date
                if len(theRest.split("Employment Duration")) > 1:
                    theRest = theRest.split("Employment Duration")[1]

                duration = theRest.split("Location")[0]
                if len(theRest.split("Location")) > 1:
                    location = theRest.split("Location")[1]
                row = [" ",title, companyName, start_date, "-", end_date, duration, location]
                edit_file(file_path, row)
    else:
        print("no exp_sector")

    # 开始导入教育信息
    edu_content = soup.find("section", "education-section")
    if edu_content:
        edit_file(file_path, [" ","EDU"])
        for each_edu in edu_content.select("li"):
            each_edu = each_edu.find("div", "pv-entity__summary-info")
            uni_name = degree_name = field = dates = "null"
            try:
                uni_name = each_edu.div.h3.text
            except:
                pass

            try:
                degree_name = each_edu.find("p", "pv-entity__degree-name").findAll("span")[1].text
            except:
                pass

            try:
                field = each_edu.find("p", "pv-entity__fos").findAll("span")[1].text
            except:
                pass

            try:
                dates = each_edu.find("p", "pv-entity__dates").findAll("span")[1].text
            except:
                pass

            row = [" ",uni_name, degree_name, field, dates]
            print("---here is insert row---")
            for temp in row:
                print(temp,end=' | ')
            edit_file(file_path, row)
    else:
        print("no edu_sector")


    return