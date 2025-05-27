
#https://idownloadcoupon.com


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

base_url ="https://idownloadcoupon.com/"

#idc:idownloadcoupon
idc_base_urls =[]
titles=[]
coupon_links =[]
coupons =[]
timestamps =[]
#returns a soup object
def get_soup(url:str):
    raw = requests.get(url,headers=HEADERS,allow_redirects=True)
    raw_soup = bs(raw.content,features="lxml")
    return raw_soup

def scrape_idc():
    limit =20 # working coupons are rare after page 10
    for i in range(1,limit+1):
        url=base_url
        url_pt2 = f"page/{i}/"
        if i>1:
            url = base_url+url_pt2
        soup = get_soup(url)

        #get only the links in the ul/li grid
        raw_links = soup.find_all("a",attrs={'class':'button product_type_external'})
        raw_titles = soup.find_all('h2',attrs={'class':'woocommerce-loop-product__title'})
        #curr_link = soup.find_all('a',attrs={'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
        links = [l['href'] for l in raw_links]
        #print(links)
        curr_title=0
        curr_titles=[title.string for title in raw_titles]

        for link in links:
            rd = requests.get(link,allow_redirects=True)
            timestamps.append(dt.datetime.now())

            #print(rd.history)
            #print(rd.url)
            coupon_links.append(link)
            coupons.append(rd.url)
            #print(bs.prettify(rd))
            idc_base_urls.append(url)
            titles.append(curr_titles[curr_title])
            curr_title+=1


    """
    [<Response [302]>, <Response [302]>, <Response [301]>]
    https://www.udemy.com/course/running-open-llms-locally-practical-guide/?LSNPUBID=nN98ER4vNAU&couponCode=D_0525&ranEAID=nN98ER4vNAU&ranMID=47907&ranSiteID=nN98ER4vNAU-0UqF20FA0vMPqa7qorxwhw&utm_medium=udemyads&utm_source=aff-campaign
    """

    raw_data = {
        "idc_link" : pd.Series(idc_base_urls),
        "course_titles": pd.Series(titles),
        "coupon_links":pd.Series(coupon_links),
        "coupon_url":pd.Series(coupons),
        "timestamps":pd.Series(timestamps)

    }
    scraped_layer = pd.DataFrame(raw_data)
    if not os.path.exists("raw_layer"):
        os.mkdir("raw_layer")

    scraped_layer.to_csv("raw_layer/idownloadcoupon.csv")