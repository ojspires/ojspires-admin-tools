#!C:\Users\ojspires\AppData\Local\Programs\Python\Python310\python.exe

#########################################################################
#    covidRetriever.py                                                  #
#                                                                       #
# This script pulls the current covid status for the following          #
# counties, and posts them to the discord channel indicated in the      #
# webhook section of this document.                                     #
# C:\Users\ojspires\workspace\Gray Hat Python\src\covidRetriever.py     #
# * Pima County Health Dept COVID-19 Progress Report:                   #
#   https://webcms.pima.gov/cms/One.aspx?portalId=169&pageId=568644     #
# * Maricopa County Health Dept VID-19 Progress Report:                 #
#   https://www.maricopa.gov/5786/COVID-19-Data#level                   #
# 0.1    12-31-22    Initial Rev.                        O Spires       #
# 0.2    01-08-23    Add testRun and webhook file input  O Spires       #
# TODO:  convert text to embed                                          #
# https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html #
# https://discord.com/developers/docs/resources/channel                 #
#########################################################################

## Imports
# Also needed: install Selenium and HTTPie binaries on system
import requests, os
from bs4 import BeautifulSoup as bs
from datetime import date

## Set up Selenium:
# Gotta use selenium; BeautifulSoup or wget are redirected by the website to an html file, which reads as corrupt if saved as a png
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
service = Service(executable_path=r'C:\Users\ojspires\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver.exe')
driver = webdriver.Chrome(service=service)

## Run Modes:
testRun = True

## Set up the source and output file
os.chdir(r"J:\Shared drives\Arizona - Congregation\Graphics\temp\\")
dateString = str(date.today())
outFile = ".".join([r"pimaCOVID",dateString,"png"])
statusPima = r'https://webcms.pima.gov/cms/One.aspx?portalId=169&pageId=568644'
pagePima = requests.get(statusPima)
statusMaricopa = r'https://www.maricopa.gov/5786/COVID-19-Data#level'
pageMaricopa = requests.get(statusMaricopa)


## Set up the webhook: 
#
# the final non-commented line in the discord_webhook file 
# should contain the full http://... webhook link
try:
    for line in open("./discord_webhook.txt"):
        li=line.strip()
        if not li.startswith("#"):
            webhook = line.rstrip()
except:
    print(webhook)


# Locate the Pima Covid Risk Image:
soupPima = bs(pagePima.content, "html.parser")
resultsPima = soupPima.find("img", title="CV-19 Indicator")
# print(results['src'])
imagePima = ''.join(["/".join(statusPima.split('/')[0:3]),resultsPima['src']])	# Build the URL
print(imagePima)	# Print the url of the image
print(outFile)	# This is where the file should save

driver.get(imagePima)	# Use Selenium to open the image
title = driver.title
print('Title:',title)
image = driver.find_element(by=By.TAG_NAME, value="img")	# Pull out the image from the html
# print(image)
with open(outFile, 'wb') as file:
    file.write(image.screenshot_as_png)
    
#Locate the Maricopa Community Transmission Level in a span class:
def my_tag_selector(tag):
    # We only accept "a" tags with a titlelink class
    return tag.has_attr("class") and "commTransLvltxt" in tag.get("class")

# Locate the Maricopa Covid Risk level statement:
soupMaricopa = bs(pageMaricopa.content, "html.parser")
resultsMaricopa = soupMaricopa.find_all(my_tag_selector)[0].parent.text
print(resultsMaricopa)    # Print the url of the image

## Output 
#  as one liner:
#httpieString = 'C:\\Users\\ojspires\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\http.exe --ignore-stdin -f %s username=COVot content="%s. The current COVID-19 Community Level in Pima County is below." file1@%s' % (webhook, resultsMaricopa, outFile)
#print(httpieString)
#os.system(httpieString)


# Output as two lines:
httpieString1 = 'C:\\Users\\ojspires\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\http.exe --ignore-stdin %s username=COVot content="%s."' % (webhook, resultsMaricopa)
httpieString2 = 'C:\\Users\\ojspires\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\http.exe --ignore-stdin -f %s username=COVot content="The current COVID-19 Community Level in Pima County is:" file1@%s' % (webhook, outFile)
print(httpieString1+'\n'+httpieString2)
if testRun:
    print('== END Test Run ==')
else:
    os.system(httpieString1)
    os.system(httpieString2)

# Working commandString = ''.join([' payload_json=\'{\\"username\\": \\"COVIDbot\\", \\"content\\": \\"hello\\"}\' file1@',outFile])
# Working combined commandString = ''.join([' payload_json=\'{\\"username\\": \\"COVIDbot\\", \\"content\\": \\"',resultsMaricopa,'. The current COVID-19 Community Level in Pima County is below.\\"}\' file1@',outFile])
