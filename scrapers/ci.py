
#https://courses.impodays.com

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from functools import lru_cache
import datetime as dt
import os

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

base_url ="https://courses.impodays.com/courses/"

#ci stands for freewebcart
ci_base_urls =[]
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
def scrape_ci():
    limit =20 #after page 10 the coupons dont work
    for i in range(1,limit+1):
        url_pt2 = f"page/{i}/"
        url=base_url
        if i>1:
            url = base_url+url_pt2
        soup = get_soup(url)

        #this gets only the link objects inside the square grid
        raw_links = soup.find_all("a",attrs={'class':'img-centered-flex rh-flex-center-align rh-flex-justify-center re_track_btn'})#[0]
        links = [link["href"] for link in raw_links]
        #print(links)

        for link in links:
            currentPageSoup = get_soup(link)
            timestamps.append(dt.datetime.now())

            #check if the page contains the coupon code
            IsUdemyCoupon = currentPageSoup.find(string="Get Course")
            if IsUdemyCoupon:
                #append to coupon_links list which contains all links containing the udemy url
                coupon_links.append(link)

                coupon_link = currentPageSoup.find_all('a',attrs={'class':'elementor-button elementor-button-link elementor-size-sm'})
                if coupon_link:
                    coupons.append(coupon_link[0].get('href'))
                else:
                    coupons.append(None)

                ci_base_urls.append(url)
                titles.append(currentPageSoup.title.string)
            else:
                coupon_links.append(None)
                coupons.append(None)

                ci_base_urls.append(url)
                titles.append(currentPageSoup.title.string)

    raw_data = {
        "idc_link" : pd.Series(ci_base_urls),
        "course_titles": pd.Series(titles),
        "coupon_links":pd.Series(coupon_links),
        "coupon_url":pd.Series(coupons),
        "timestamps":pd.Series(timestamps)

    }
    scraped_layer = pd.DataFrame(raw_data)
    if not os.path.exists("raw_layer"):
        os.mkdir("raw_layer")

    scraped_layer.to_csv("raw_layer/coursesimplodays.csv")