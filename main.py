import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import os

# os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\Pamela.Buchwald\Desktop\cacert.pem'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.tripadvisor.com/Attraction_Review-g14134359-d14951238-Reviews-TeamLab_Planets_TOKYO-Toyosu_Koto_Tokyo_Tokyo_Prefecture_Kanto.html")
time.sleep(10)

PAGE_AMOUNT = 5 #w Pythonie jeśli jest jakaś STAŁA i chcemy zaznaczyć że ona się nie zmieni, ti piszumy wielkimi literami i Snake Case (tylko dla osooby która czyta ten kod)
#przyklad snake case slowo_slowo2
#camel case to slowoSlowo2
#Linter to program ktory dba o jakosc kody, tzn podkrelsa co MOZNA zrobic lepiej

#mamy pętle ktora przechodzi przez 5 stron

reviews = [] #tu będziemy trzymać wszystkie opinie
pages = [] # tu będziemy trzymać numer strony na której została odnalziona opinia

driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/button').click()

for i in range(PAGE_AMOUNT):
    reviews_on_single_page= []
    more_buttons = driver.find_elements(By.CLASS_NAME,'CECjK')
    print(len(more_buttons))
    for j in range(len(more_buttons)):
        if more_buttons[j].is_displayed():
            driver.execute_script('arguments[0].click();',more_buttons[j])
            time.sleep(1)
    page_source = driver.page_source # to co tu robimy to bierzemy to jak strona wygląda po przeklikaniu przez selenium i zapisujemy jako page_source
    soup = BeautifulSoup(page_source, 'html.parser') # do bs4 podajemy naszą rozwiniętą stronę jako obiekt do scrappowania
    reviews_selector = soup.find_all('div', class_='biGQs _P pZUbB KxBGd')
    for review_selector in reviews_selector:
        review_span = review_selector.find('span', class_='yCeTE')
        if review_span is None:
            continue #Jeśli nie znaleźliśmy spana z komentarzem to przejdzeimy do następnego elementu div
        review = review_span.get_text(strip=True)
        reviews_on_single_page.append(review)
    print(reviews_on_single_page)
    break
    

