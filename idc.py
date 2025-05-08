#https://freewebcart.com
#https://idownloadcoupon.com
#https://www.coursecouponz.com
#https://easylearn.ing
#https://courses.impodays.com

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

url ="https://idownloadcoupon.com/"

#idc:idownloadcoupon
idc_base_urls =[]
titles=[]
coupon_links =[]
coupons =[]

#returns a soup object
def get_soup(url:str):
    raw = requests.get(url,headers=HEADERS,allow_redirects=True)
    raw_soup = bs(raw.content,features="lxml")
    return raw_soup


#fwc stands for freewebcart
fwc_base_urls =[]
titles=[]
coupon_links =[]
coupons =[]


count =0
limit =10
for i in range(limit+1):
    url_pt2 = f"page/{i}/"
    if i>0:
        url = url+url_pt2
    soup = get_soup(url)
    
    raw_links = soup.find_all("li",attrs={'class':'products columns-4'})
    print(raw_links)