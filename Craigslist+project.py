
# coding: utf-8

# # Imports

# In[1]:

import scrapy
from scrapy.selector import HtmlXPathSelector
import csv
import requests
import re
import numpy as np
import operator


# # Scraping Craigslist 

# In[2]:

class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    comp = scrapy.Field()


# In[3]:

class CraigsSpider(scrapy.Spider):
    name = "craigsBase"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/npo"]

    def parse(self, response):
        #crawls all the links
        for href in response.css("span.pl > a::attr('href')"):
            url = response.urljoin(href.extract())
            print(url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        item = CraigslistItem()
        item['title'] = response.xpath('//*[@id="titletextonly"]/text()').extract()
        item['comp'] = response.xpath('//*[@id="pagecontainer"]/section/section/div[1]/p/span[1]/b/text()').extract()
        yield item


# # Filtering out all the salaries

# In[4]:

salaries = []
clean_salaries = []
with open("craigfile.csv") as f: 
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if "$" in row[0]:   
            salarie = re.findall('\$\d*.\d{1,4}', row[0])
            for salary in salarie:
                if "-" in salary:
                    salary = salary.split("-")
                    salaryB = salary[:len(salary)/2]
                    salaryB = salaryB[0].strip("$")
                    salaryC = salary[len(salary)/2:]
                    salaries.append(salaryB)
                    salaries.append(salaryC[0])
                else:
                    salaries.append(salary)     
    for x in salaries:
        salaries = x.strip('$').replace(',','')
        clean_salaries.append(float(salaries))
print clean_salaries    


# # Dividing up the salaries based on amount

# In[7]:

annual = []
for i in clean_salaries:
        if i > 6000:
            annual.append(i)
print annual            


# In[8]:

month = []
for i in clean_salaries:
        if i > 500 and i < 6000:
            month.append(i)
print month 


# In[9]:

week = []
for i in clean_salaries:
        if i > 50 and i < 1000:
            week.append(i)
print week 


# In[10]:

hour = []
for i in clean_salaries:
        if i < 50:
            hour.append(i)
print hour 


# # Average annual salary

# In[11]:

print np.mean(annual)


# In[12]:

print clean_salaries


# # Average monthly salary

# In[13]:

print np.mean(month)


# # Average weekly salary

# In[14]:

print np.mean(week)


# # Average hourly salary

# In[15]:

print np.mean(hour)


# In[16]:

print clean_salaries


# # Alternative

# In[341]:

def divide_salaries(array):
    salaries = { annual == [], month == [], week == [], hour == [] }
    
    for i in array:
        if i > 5000:
            annual.append(i)
        elif i < 50:
            hour.append(i)
        elif i > 50 and i < 500:
            week.append(i)
        else: 
            month.append(i)
    return salaries

