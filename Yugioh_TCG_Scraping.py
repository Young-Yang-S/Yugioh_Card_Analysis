# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:04:09 2021

@author: daiya
"""


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import socket
from selenium.webdriver.support.ui import Select
import re
import os
import math


# chrome.exe --remote-debugging-port=9555 --user-data-dir="C:\selenum_1\AutomationProfile


socket.setdefaulttimeout(150)  # set the max loading time 30
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9555")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver11.exe"
chrome_options.add_argument("user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")    
driver = webdriver.Chrome(chrome_driver,  chrome_options=chrome_options)
agent = driver.execute_script("return navigator.userAgent")     



#### Part One : Get all the set names 

link = 'https://www.tcgplayer.com/search/yugioh/the-infinity-chasers?productLineName=yugioh&page=1&setName=%22duel-terminal---preview%22'
driver.get(link)


set_web = driver.find_elements_by_class_name('checkbox__option-value')

set_list = []

for i in set_web:
    set_list.append(i.text)

set_list = set_list[47:478]


set_link  = []

for i in set_list:
    try:
        tmp = i.replace("'",'')
    
    except:
        True
        
    try:
        tmp = tmp.replace(':','')
    except:
        True
    
    tmp = tmp.replace(' ','-')
    
    set_link.append(tmp)


final_set = set_link  


########### Part two : Get the information of all cards
def get_page_number():
    value = driver.find_element_by_class_name('results').text.split(' ')[-2]
    number = math.ceil(int(value)/24)
    
    return number
    
def single_pages():
    
    single = pd.DataFrame()
    
    set_name_web = driver.find_elements_by_class_name('search-result__subtitle')
    
    set_name = []
    
    for i in range(0,len(set_name_web)):
        set_name.append(set_name_web[i].text)
        
        
    rarity_id_web = driver.find_elements_by_class_name('search-result__rarity')
    
    rarity = []
    
    id_list = []

    sequence = []
    for i in range(0,len(rarity_id_web)):
        if rarity_id_web[i].text == '':
            sequence.append(i)
            id_name = ' Pack'
        else:
            rarity.append(rarity_id_web[i].text.split(' ')[0])

            try:
                id_name = rarity_id_web[i].text.split('·')[1].replace('#','')
        
            except:
                id_name = ' Pack'
                
        id_list.append(id_name)
        
    for k in range(0,len(sequence)):
        rarity = rarity[0:sequence[k]] + ['Pack'] + rarity[sequence[k]:]
    
    
    card_name_web = driver.find_elements_by_class_name('search-result__title')
    
    
    card_name = []
    
    for i in range(0,len(card_name_web)):
        card_name.append(card_name_web[i].text)
    
    
    price_web  = driver.find_elements_by_class_name("search-result__market-price") 
    
    price_list = []
    
    for i in price_web:
        if i.text == 'Market Price Unavailable':
            price_list.append('No Price')
        else:
            price_list.append(i.text.split(' ')[-1])
            
            
    single['Name'] = card_name
    single['Set'] = set_name 
    single['Rarity'] = rarity
    single['Id'] = id_list
    single['Market Price'] = price_list
    
    return single 
    

not_found = []
fail_scraped = []
count = 0
 
for j in range(285,len(final_set)):
    
    
    link = 'https://www.tcgplayer.com/search/yugioh/the-infinity-chasers?productLineName=yugioh&page=1&setName="{}"'.format(final_set[j])
    
  
    driver.get(link)
    
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-result__title"))) 
    
    except:
        not_found.append(link)
    
    number = get_page_number()
    
    time.sleep(8)
    single_page = pd.DataFrame()
    
    single_page = single_pages()
    
    for i in range(1,number):
        driver.find_element_by_id('nextButton').click()
        time.sleep(8)
        tmp = single_pages()
        try:
            single_page = single_page.append(tmp)
        
        except:
            fail_scraped.append(driver.current_url)
        
        print('   Finished ',i+1, 'out of ',number)
    
    
    name= final_set[j]      
    os.chdir(r'C:\Users\daiya\OneDrive\Desktop\Yugioh')  
    single_page.to_csv('{}.csv'.format(name),index=False)      
    
    
    print('Already Finished: ',count)
    count += 1
    
    

