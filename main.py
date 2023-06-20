import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
from textblob import TextBlob

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.tripadvisor.com/Attraction_Review-g14134359-d14951238-Reviews-TeamLab_Planets_TOKYO-Toyosu_Koto_Tokyo_Tokyo_Prefecture_Kanto.html")
time.sleep(1)

PAGE_AMOUNT = 5 

reviews = []
pages = []

driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/button').click()

for i in range(PAGE_AMOUNT):
    reviews_on_single_page= []
    more_buttons = driver.find_elements(By.CLASS_NAME,'CECjK')
    for j in range(len(more_buttons)):
        if more_buttons[j].is_displayed():
            driver.execute_script('arguments[0].click();',more_buttons[j])
            time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    reviews_selector = soup.find_all('div', class_='biGQs _P pZUbB KxBGd')
    for review_selector in reviews_selector:
        review_span = review_selector.find('span', class_='yCeTE')
        if review_span is None:
            continue
        review = review_span.get_text(strip=True)
        reviews_on_single_page.append(review)
    reviews_amount = len(reviews_on_single_page)
    page_ids = [i+1]*reviews_amount 
    reviews.extend(reviews_on_single_page)
    pages.extend(page_ids)
    time.sleep(1)
    page_button = driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[11]/div[1]/div/div[1]/div[2]/div/a')
    actions = ActionChains(driver)
    actions.move_to_element(page_button)
    actions.perform()
    page_button.click()
    time.sleep(1)
driver.quit()

data = {'ID':pages,'Comments':reviews}

df = pd.DataFrame(data)
print(df.head(50))

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'Positive'
    elif sentiment < 0:
        return 'Negative'
    else:
        return 'Neutral'

df['Sentiment'] = df['Comments'].apply(analyze_text)

df.to_excel('wynik_pobierania.xlsx', index=False)

conn = sqlite3.connect('comments.sqlite')

df.to_sql('CommentsTable', conn, if_exists='append', index=False)

conn.close()
