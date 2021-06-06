from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pickle as pkl
import time
import random
import pprint as pprint
import re
import json
import sys
import ast

import requests
import html5lib

def retrieve_html(driver,BeautifulSoup):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#read filenames
def read_data_filenames():
    filenames = []
    print("Reading filenames...")
    with open('data/data_progress.txt','r') as f:
        content = f.readlines()
        f.close()
    for line in content:
        line = line.split(":")
        filename = line[0]
        filenames.append(filename)

    print("Filename reading completed.")
    return filenames

#Load all file json data
def load_json_files(filenames):
    json_files = []
    for filename in filenames:
        print("Loading", filename)
        try:
            with open('data/'+ 'data' + filename,'rb') as f:
                json_files.append(json.load(f))
        except FileNotFoundError:
            print("File not found.")
    print("Loading json files completed.")
    return json_files

#Store backers with its associated project urls
#e.g. [backer,[project1,project2...projectn]]
def backers_projects(json_files):
    backers_projects = []
    print("Retrieving backer and their backed projects...")

    for json_file in json_files:
        for backer in json_file:
            backer_name = backer[0]['name']
            projects = backer[1]
            project_urls = []

            #iterate thru each backer's projects
            for project in projects:
                project_url = ""
                project = json.loads(project)
                project_url = project['urls']['web']['project']
                project_urls.append(project_url)

            backers_projects.append((backer_name,project_urls))
    #pprint.pprint(backers_projects)
    print("Total number of backers with projects:",str(len(backers_projects)))
    return backers_projects

#initialise variables
filenames = []
json_files = []
backers_projects_urls = []

filenames = read_data_filenames()
json_files = load_json_files(filenames)
backers_projects_urls = backers_projects(json_files)

###Perform Web Scraping###
def create_driver(webdriver,Options):
    #Chrome configuration
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("window-size=1280,800")

    driver = webdriver.Chrome(executable_path="./chromedriver",options=chrome_options)
    return driver


try:
    #Loop thru all projects urls
    for backer_project in backers_projects_urls:
        project_urls = backer_project[1]

        for project_url in project_urls:
            driver = create_driver(webdriver,Options)
            #driver.get(project_url)
            driver.get('https://www.kickstarter.com/projects/fowers/paperback-adventures-a-novel-solo-word-game/description')
            soup = retrieve_html(driver,BeautifulSoup)
            time.sleep(2)

            ###Campaign Section###
            #retrieve story content
            try:
                story_tree = driver.find_elements_by_class_name('rte__content')
                story_content = ""

                for node in story_tree:
                    story_content += node.text

            except NoSuchElementException:
                print("story element not found")

            #risk and challenge content
            try:
                risk_challenge_content = ""
                risk_challenge_content = driver.find_element_by_id('risks-and-challenges').text

            except NoSuchElementException:
                print("risk_challenge element not found.")

            #Environmental commitments content
            try:
                env_commit_content = ""
                env_commit_content = driver.find_element_by_id('environmentalCommitments').text
                #print(env_commit_content)
            except NoSuchElementException:
                print("envrionmental_commitment element not found.")

            #Creator bio content
            try:
                project_creator_bio = ""
                project_creator_bio = driver.find_element_by_id('experimental-creator-bio').text
            except NoSuchElementException:
                print("project_creator_bio element not found.")

            #Support content
            try:
                pledge_amt_tree = driver.find_elements_by_class_name('pledge__amount')
                pledge_amt_list = []
                for pledge_amt in pledge_amt_tree:
                    pledge_amt_list.append(pledge_amt.text)
                #print(pledge_amt_list)
                #print("pledge_amt",len(pledge_amt_list))
            except NoSuchElementException:
                print("pledge_amt_tree element not found.")

            try:
                pledge_title_tree = driver.find_elements_by_class_name('pledge__title')
                pledge_title_list = []
                for pledge_title in pledge_title_tree:
                    pledge_title_list.append(pledge_title.text)
                #print(pledge_title_list)
                #print("pledge_title",len(pledge_title_list))
            except NoSuchElementException:
                print("pledge_title_tree element not found.")

            try:
                pledge_descp = driver.find_elements_by_class_name('pledge__reward-description')
                pledge_descp_list = []
                for descp in pledge_descp:
                    pledge_descp_list.append(descp.text)
                #print(pledge_descp_list)
                #print("descp",len(pledge_descp_list))
            except NoSuchElementException:
                print("pledge_descp element not found.")

            try:
                pledge_time_tree = driver.find_elements_by_class_name('pledge__extra-info ')
                time_list = []
                for pledge_time in pledge_time_tree:
                    tmp_list = []
                    tmp_list = pledge_time.text.split("\n")
                    #estimated delivery
                    if len(tmp_list) == 2:
                        time_list.append([{tmp_list[0]:tmp_list[1]}])

                    #shipping
                    elif len(tmp_list) == 4:
                        time_list.append([{tmp_list[0]:tmp_list[1]},{tmp_list[2]:tmp_list[3]}])

                #print(time_list)
                #print("time",len(time_list))
            except NoSuchElementException:
                print("pledge_time_tree element not found.")

            try:
                stats_tree = driver.find_elements_by_class_name('pledge__backer-stats')
                stat_list = []
                for stat in stats_tree:
                    stat_tmp_list = stat.text.split("\n")
                    stat_list.append(stat_tmp_list)
                #print(stat_list)
            except NoSuchElementException:
                print("backer_tree element not found.")

            support_list = []
            for amt,title,descp,date,stat in zip(pledge_amt_list,pledge_title_list,pledge_descp_list,time_list,stat_list):
                support_dict = {}
                support_dict['amt'] = amt
                support_dict['title'] = title
                support_dict['descp'] = descp
                support_dict['time'] = date
                support_dict['stat'] = stat
                support_list.append(support_dict)

            #pprint.pprint(support_list)
            campaign_data = {'story':story_content,'risks':risk_challenge_content,'env':env_commit_content,'creator_bio':project_creator_bio}
            #print(campaign_data)
            #print("==================")
            ###Updates Section###
            try:
                update_link = driver.find_element_by_partial_link_text('Updates')
                update_link.click()
                time.sleep(4)
            except NoSuchElementException:
                print("update link not found")

            #project status: launched/canceled
            try:
                project_status = driver.find_elements_by_css_selector('div.flex.flex-column.items-center.justify-center.h100p')
                status_list = []
                for status in project_status:
                    status = status.text.split('\n')
                    status_list.append({status[0]:status[1]})
                print(status_list)
            except NoSuchElementException:
                print("project status element not found.")

            #update no
            try:
                update_no_tree = driver.find_elements_by_css_selector('span.type-13.soft-black_50.text-uppercase')
                update_no_list = []
                for update in update_no_tree:
                    update_no_list.append(update.text)
                print(update_no_list)
            except NoSuchElementException:
                print("update_no element not found.")

            #title
            try:
                update_title_tree = driver.find_elements_by_css_selector('h2.mb3')
                update_title_list = []
                for update_title in update_title_tree:
                    update_title_list.append(update_title.text)
                print(update_title_list)
            except NoSuchElementException:
                print("update_title_tree element not found.")

            #user info
            try:
                #mb3 flex type-14 items-start border-bottom pb3
                #update_userinfo_tree = driver.find_element_by_css_selector('div.mb3.flex.type-14.items-start.border-bottom.pb3')
                update_userinfo_tree = driver.find_elements_by_css_selector('div.pl2')
                update_userinfo_list = []

                for userinfo in update_userinfo_tree:
                    if userinfo.text == "":
                        continue
                    temp_info_list = [item for item in userinfo.text.split('\n') if item != '']

                    name_status = temp_info_list[0]

                    update_date = temp_info_list [1]
                    name = ''
                    status = ''

                    print(temp_info_list)
                    if 'Creator' in name_status:
                        name_status = name_status.partition('Creator')
                        name = name_status[0]
                        status = name_status[1]
                    elif 'Collaborator' in name_status:

                        name_status = name_status.partition('Collaborator')
                        name = name_status[0]
                        status = name_status[1]

                    update_userinfo_list.append({'name':name,'status':status,'update_date':update_date})
                #pprint.pprint(update_userinfo_list)
            except NoSuchElementException:
                print("update_userinfo_tree element not found.")

            #update content
            try:
                content_tree = driver.find_elements_by_class_name('rte__content')
                update_content_list = []
                for content in content_tree:
                    update_content_list.append(content.text)
                print(update_content_list)
                print(len(update_content_list))
            except NoSuchElementException:
                print("content_tree element not found.")

            #To continue:add supdate formatted data into a list
            print("status:",len(status_list),'update_no:',len(update_no_list),'update_title:',len(update_title_list),'update_userinfo:',len(update_userinfo_list),'update_content:',len(update_content_list))
            update_list = []
            for update_no, update_title,update_userinfo,update_content in zip(update_no_list,update_userinfo_list,update_title_list,update_content_list):
                update_dict = {}
                update_dict['update_no'] = update_no
                update_dict['update_userinfo'] = update_userinfo
                update_dict['update_content'] = update_content
                update_list.append(update_dict)

            #include project status, i.e. project launched or project end
            update_list.append({'status':status_list})
            pprint.pprint(update_list)
            print(len(update_list))

            #to continue for comments..
            break
            #driver.quit()

        break


    #test_url = backer_project[0][1][0]
    #page = requests.get(test_url)

    '''
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html5lib')
        story = soup.find("section", class_="js-project-content js-project-description-content project-content")
        print(story.prettify())


    '''
    #driver = webdriver.Chrome(executable_path="./chromedriver",options=chrome_options)
    #driver.get(test_url)
    #soup = retrieve_html(driver,BeautifulSoup)
    #story = soup.find("div", class_="rte__content")
    #print(story)
    #driver.quit()

    #community_link = driver.find_element_by_link_text('Community')
    #community_link.click()
        #driver.get(test_url)

    #driver.quit()

    '''
    for url in backer_urls:
        driver.get(url)
        soup = retrieve_html(driver,BeautifulSoup)
        print(soup)
        break
    '''
except Exception as e:
    print(e)
