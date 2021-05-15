from bs4 import BeautifulSoup
import requests
import pandas as pd
# from icecream import ic
import random 
from tqdm import tqdm
from time import sleep
from datetime import datetime
import pickle as pkl
import re
import os
from selenium import webdriver
import time
from bs4 import BeautifulSoup

def readBacker(pkl_file):
    with open(pkl_file) as f:
        backer_list = pkl.load(f)
    return backer_list


def getBackerInfo(backer_url_list,backer_dicts,path):
    """
    backer_url_list [str]: The list containing the public backer profile url
    backer_dicts {name: {{feature}}}: the backer dicts contains all scrawled information from profile webstie
    path: the os path address contains chromedriver
    """
    driver=webdriver.Chrome(executable_path=path)  

    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        try:

            for url in tqdm(backer_url_list):
            

                execute_times(10)

                ### This is my previous code, you can write you own solution
                #############################
                # html=driver.page_source
                # soup = BeautifulSoup(html, 'html.parser') 
                # #get name
                # name = re.search(r'(?<=\n)(.*)(?=\n)',str(soup.find_all("h2", {"class": "mb2"}))).group()
                # #get backer num
                # backed_num = soup.find_all("span", {"class": "backed"})
                # num = int(re.search(r'\d+', str(backed_num)).group())
                # #get location
                # location = re.search(r'(?<=\d">)(.*)(?=<\/a>)',str(soup.find_all("span", {"class": "location"}))).group()
                # #get time w/t regex filter
                # time = soup.find_all("time")
                # #get backed projs
                # projs = soup.find_all("ul",{"class":"mobius"})
                # #assign value to dict
                # backer_dicts['name'] = name
                # backer_dicts['backed_num'] = num
                # backer_dicts['geolocation'] = location
                # backer_dicts['start_date'] = time
                # backer_dicts['url'] = url
                # backer_dicts['back_projs'] = projs


                # #get bio
                # html = requests.get(url+"/about").content
                # sleep(random.randint(1,5))

                #################################
        except Exception as e:
            print(e)
            return backer_dicts
    return backer_dicts