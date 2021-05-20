from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pickle as pkl
import time
import random
import pprint as pprint
import re
import json
import sys

def retrieve_html(driver,BeautifulSoup):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def rotate_proxy(webdriver,no_of_backers_urls):
    #Gather rotating proxy
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
    driver.quit()
    proxies = []

    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])

    #Expand proxies list
    return proxies * no_of_backers_urls


def rotate_proxy2(webdriver,no_of_backers_urls):
    from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
    req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
    proxies = req_proxy.get_proxy_list() #this will create proxy list
    return proxies * no_of_backers_urls

def rand_user_agent(random):
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    return random.choice(user_agent_list)

#store backers urls
with open('backer_list.pickle','rb') as f:
    backer_urls = pkl.load(f)


proxies = []
#proxies = rotate_proxy(webdriver,len(backer_urls))

#Trial Private proxies
proxies_list = [
    '45.95.96.132:8691',
    '45.95.96.187:8746',
    '45.95.96.237:8796',
    '45.136.228.154:6209',
    '45.94.47.66:8110'
]
proxies =  proxies_list * len(backer_urls)

test_url = ['https://www.kickstarter.com/profile/jamesvanosdol','https://www.kickstarter.com/profile/687298340']

backer_list = []

#Receive inputs to modify list and output file
start_idx = int(input("Start index for backers_urls: "))
end_idx = int(input("End index for backers_urls: "))
data_output = input("Batch_size and iteration_no, e.g 30_2: ")

backer_urls = backer_urls[start_idx:end_idx]
pprint.pprint(backer_urls)
total_project_crawled = 0
try:
    start_time = time.time()
    for url in backer_urls:
        #Use different proxy for each new url
        i = 0
        #improve chrome driver performance
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("window-size=1280,800")

        #chrome_options.add_argument('--proxy-server={}'.format(proxies[i]))
        i += 1

        #user different user-agent for each new url
        chrome_options.add_argument("user-agent="+rand_user_agent(random))

        driver = webdriver.Chrome(executable_path="./chromedriver",options=chrome_options)
        driver.maximize_window()
        backer_info = {}

        #access webpage url
        driver.get(url)

        time.sleep(random.randint(10,12))

        ##crawl about page##
        about_link = driver.find_element_by_link_text('About')
        #about_link = driver.find_element_by_xpath('/html/body/main/div/div[3]/div/div/div/ul/li[1]/a')
        about_link.click()
        time.sleep(random.randint(10,12))

        #retrieve about html
        soup = retrieve_html(driver,BeautifulSoup)

        try:
            #biography
            p_list = soup.find("div", class_="grid-row pt3").find_all("p")
            bio = ''

            for p in p_list:
                bio += ''.join(p.text).strip()

            #personal website
            links = soup.find("ul", class_="menu-submenu").find_all("a")
            websites = []

            for link in links:
                websites.append(link.text.strip())

            backer_info.update({'biography': bio})
            backer_info.update({'websites': websites})
            backer_info.update({'url_link':url})
        except AttributeError:
            pass

        ##crawl Backed webpage##
        backed_link = driver.find_element_by_partial_link_text('Backed')
        backed_link.click()
        time.sleep(random.randint(10,12))

        #pause every x seconds after scrolling to btm of webpage
        SCROLL_PAUSE_TIME = random.randint(5,8)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        #Loop infinte scrolling
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


        #Retrieve complete html page after infinite scroll
        soup = retrieve_html(driver,BeautifulSoup)

        #initialise variables
        name = ""
        backed = ""
        loc = ""
        join = ""

        #Backer's info
        try:
            name = soup.find("h2", class_="mb2").text.strip()
            backed = soup.find("span", class_="backed").text.strip()
            loc = soup.find("span", class_="location").text.strip()
            join = soup.find("span", class_="joined").text.strip()
        except AttributeError:
            pass

        backer_info.update({'name': name})
        backer_info.update({'no_of_backed_proj': backed})
        backer_info.update({'location': loc})
        backer_info.update({'joined_date': join})

        #Collect projects data from fully loaded page
        projects = soup.find_all('div', attrs={'class':'react-user-prof-card grid-col-12 grid-col-6-sm grid-col-4-lg'})

        project_list = []
        for project in projects:
            project_list.append(project["data-project"])

        total_project_crawled += len(project_list)

        backer_list.append((backer_info,project_list))

        time.sleep(random.randint(3,5))

        #Exit chrome driver
        driver.quit()

    #ouput file to json
    with open ('data/data'+ data_output +'.json','w') as outfile:
        json.dump(backer_list,outfile)

    #output crawled progress
    with open('data/data_progress.txt','a') as f:
        f.write(data_output+".json"+":"+str(start_idx) + "-" + str(end_idx)+ "\n")

finally:
    print("Crawling completed")
    print("Elapsed time: {0:.2f}".format(time.time() - start_time),"secs")
    print("Number of backers crawled:",len(backer_list))
    print("Number of Backer's project found:",total_project_crawled)
