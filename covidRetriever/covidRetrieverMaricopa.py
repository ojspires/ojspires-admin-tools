# PCHD COVID-19 Progress Report: https://webcms.pima.gov/cms/One.aspx?portalId=169&pageId=568644
# MCHD COVID-19 Progress Report: https://www.maricopa.gov/5786/COVID-19-Data#level
import requests, shutil, selenium, httpie, os
from bs4 import BeautifulSoup as bs
from datetime import date

# Set up Selenium:
# Gotta use selenium; BeautifulSoup or wget are redirected by the website to an html file, which reads as corrupt if saved as a png
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
service = Service(executable_path=r'C:\Users\ojspires\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Set up the source and output file
os.chdir(r"J:\Shared drives\Arizona - Congregation\Graphics\temp\\")
dateString = str(date.today())
outFile = ".".join([r"mariCOVID",dateString,"png"])
statusMaricopa = r'https://www.maricopa.gov/5786/COVID-19-Data#level'
pageMaricopa = requests.get(statusMaricopa)

## Set up the webhook: the final non-commented line in the discord_webhook file should contain the full http://... webhook link
try:
    for line in open("./discord_webhook.txt"):
        li=line.strip()
        if not li.startswith("#"):
            webhook = line.rstrip()
except:
    print(webhook)
    
#Locate the Community Transmission Level in a span class:
def my_tag_selector(tag):
    # We only accept "a" tags with a titlelink class
    return tag.has_attr("class") and "commTransLvltxt" in tag.get("class")

# Locate the Covid Risk level statement:
soup = bs(pageMaricopa.content, "html.parser")
results = soup.find_all(my_tag_selector)[0].parent.text
print(results)	# Print the url of the image

