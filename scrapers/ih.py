#Inventhigh.net

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from functools import lru_cache
import datetime as dt
import os
import notify

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

base_url ="https://inventhigh.net/freecoupon"

#fwc stands for freewebcart
fwc_base_urls =[]
titles=[]
coupon_links =[]
coupons =[]
timestamps =[]
#returns a soup object
#@lru_cache
def get_soup(url:str):
    raw = requests.get(url,headers=HEADERS)
    raw_soup = bs(raw.content,features="lxml")
    return raw_soup

"""
#for debugging
re = requests.get(base_url,headers=HEADERS)
with open("freewebcart.txt","wb") as f:
    f.write(re.content)
"""

def scrape_ih():

    soup = get_soup(base_url)

    #this gets only the link objects inside the square grid
    #raw_links = soup.find_all("div",attrs={'class':'row content'})#[0]
    raw_links = soup.find_all('a',attrs={'class':'btn btnmain'})#,"target":"_blank"})


    #links = [link.get("href") for link in raw_links]
    #to get the actual links
    links = [link["href"] for link in raw_links]#.find_all('a',href=True)]
    #print('\n'.join(links))

    for link in links:
        currentPageSoup = get_soup(link)
        timestamps.append(dt.datetime.now())

        

        #check if the page contains the coupon code
        udemy_coupon = currentPageSoup.find_all('a',attrs={'class':'btn btnmain',"target":"_blank"})
        #get the linksynergy url after redirects
            
        rd = requests.get(link,allow_redirects=True)
        
        if udemy_coupon:
           
            #append to coupon_links list which contains all links containing the udemy url
            coupon_links.append(link)

            coupon_link = currentPageSoup.find_all('a',attrs={'rel':'nofollow noopener'})
            coupons.append(rd.url)
            #coupons.append(coupon_link.get('href'))

            fwc_base_urls.append(url)
            titles.append(currentPageSoup.title.string)
        else:
            coupon_links.append(None)
            coupons.append(None)

            fwc_base_urls.append(url)
            titles.append(currentPageSoup.title.string)

    #print(coupon_links)

    #creating the dataframe
    raw_data = {
        "fwc_link" : pd.Series(fwc_base_urls),
        "course_titles": pd.Series(titles),
        "coupon_links":pd.Series(coupon_links),
        "coupon_url":pd.Series(coupons),
        "timestamps":pd.Series(timestamps)

    }
    
    scraped_layer = pd.DataFrame(raw_data)
    
    os.makedirs("raw_layer",exist_ok=True)

    scraped_layer.to_csv("raw_layer/freewebcart.csv",mode="a")







if __name__ == "__main__":
    scrape_ih()
