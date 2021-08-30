from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
from random import randint 

links = ["https://www.eldorado.ru/c/smartfony/", "https://www.eldorado.ru/c/noutbuki/", "https://www.eldorado.ru/c/kholodilniki/"]
opts = Options()
opts.set_headless()
driver = webdriver.Firefox(options=opts)
driver.maximize_window()
k = 0
data = []

def create_files(data):
    for i in range(9):
        item_reviews = data[i*10:(i+1)*10]
        with open(f'{randint(0,60000)}.json', 'w') as f:
            json.dump(item_reviews, f)

def check_stars(html):
    html = html.findAll('div', {'class':'star starFull'})
    return(len(html))

def find_review_button(buttons):
    button = 0
    buttons = driver.find_elements_by_xpath('//button[@class="By Gy"]')
    for i in range(len(buttons)):
        if "По отзывам" in str(buttons[i].text):
            button = buttons[i]
    
    return button

def get_reviews_data():
    global data
    html = driver.page_source
    html = BeautifulSoup(html,features="lxml")
    reviews = html.findAll('div', {'class':'usersReviewsListItem'})
    for k in range(len(reviews)):
        data.append({
                "url":str(driver.current_url), 
                "author":BeautifulSoup(str(reviews[k].find('span', {'class':'userName'})), "lxml").get_text(),
                "date":BeautifulSoup(str(reviews[k].find('div', {'class':'userReviewDate'})), "lxml").get_text(),
                "stars":check_stars(reviews[k]),
                "content":BeautifulSoup(str(reviews[k].find('div', {'class':'middleBlockItem'})), "lxml").get_text(),
        })

for i in range(3):
    driver.get(links[i])

    element_to_click = find_review_button(html)
    actions = ActionChains(driver)
    actions.click(element_to_click)
    actions.perform()

    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "LD")))

    html = driver.page_source
    html = BeautifulSoup(html,features="lxml")

    items = html.findAll('a', {'class':'LD'})
    for j in range(3):
        item = BeautifulSoup(str(items[j]), features="lxml").find('a')['href']
        link = "https://www.eldorado.ru"+str(item)+"?show=response#customTabAnchor"
        print(link)
        driver.get(link)
        driver.execute_script("window.scrollTo(0, 1000);")
        get_reviews_data()
create_files(data)