'''
This script is used to web scrape news articles from Google regarding any keyword.
'''

import requests, lxml
from bs4 import BeautifulSoup
import urllib.request,sys,time
import pandas as pd
import csv

root = 'https://www.google.com/'
url = 'INSERT URL HERE'
r = requests.get(url)
soup = BeautifulSoup(r.content)

results = []

def scrape_news(url):
      r = requests.get(url)
      soup = BeautifulSoup(r.content)
      for item in soup.find_all('div', attrs = {'class': 'ZINbbc xpd O9g5cc uUPGi'}):

          # Retrieving link
          raw_link = item.find('a', href = True)['href']
          link = raw_link.split("/url?q=")[1].split("&sa=U")[0]

          #Retrieving article content
          article = requests.get(link)
          parsed_article = BeautifulSoup(article.text,'lxml')
          paragraphs = parsed_article.find_all('p')
          article_text = ""
          for p in paragraphs:
              article_text += p.text
          
          # Retrieving Title
          title = item.find('div', class_ ='BNeawe vvjwJb AP7Wnd').get_text()

          #Retrieving Description and Time
          description_time = item.find('div', attrs = {'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
          time = description_time.split(' · ')[0]
          description = description_time.split(' · ')[1]

          results.append([title, link, description, time, article_text])

      # Finding next page url
      next = soup.find('a', attrs = {'aria-label': 'Next page'})['href']
      url = root + next
      
      scrape_news(url)

scrape_news(url)

# export data to csv file
headers = ['title', 'link', 'description', 'time', 'article_text']
df = pd.DataFrame(results, columns = headers)
df.to_csv("news_articles.csv")

len(results)

