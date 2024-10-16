from gettext import textdomain

from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome driver with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless") # Run in headless mode for efficiency
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options= chrome_options)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://newswebsite.com"
           )


#Give time for dynamic content to load
time.sleep(3)

#Get the page source after dynamic content loads
html = driver.page_source

#parsing html with BeautifulSoup
soup = BeautifulSoup(html,'html.parser')
#Example of Extracting all article titles and their URLs
article = []
for item in soup.find_all('div', class_='article'):
    title = item.find('h2').text
    link = item.find('a')['href']
    article.append({
        'Title':title,
        'Link':link
    })
page_number = 1
while True:
    #Load the page
    driver.get(f"https:/newswebsite.com/page/{page_number}")

    #Wait for dynamic contect to load
    time.sleep(3)

    #parse the html
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    #Find the articles as before
    new_articles = soup.find_all('div', class_='article')
    if not new_articles:
        break    #Ext the loop if no more articles found

    #Extract Data
    for item in new_articles:
        title = item.find('h2').text
        link = item.find('a')['href']
        article.append({'Title': title,'Link':link})

    #Move to the next page
    page_number +=1

#Save to the CSV using pandas
df = pd.DataFrame(article)
df.to_csv('scraped_articles.csv', index=False)

