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

base_url ="https://freewebcart.com/category/provider/udemy-coupon/"

#fwc stands for freewebcart
fwc_base_urls =[]
titles=[]
coupon_links =[]
coupons =[]
#returns a soup object
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

limit =10
for i in range(1,limit+1):
    url_pt2 = f"page/{i}/"
    url=base_url
    if i>1:
        url = base_url+url_pt2
    soup = get_soup(url)
        
    #this gets only the link objects inside the square grid
    raw_links = soup.find_all("div",attrs={'class':'wp-block-group is-layout-flow wp-block-group-is-layout-flow'})[0]


    #links = [link.get("href") for link in raw_links]
    #to get the actual links
    links = [link["href"] for link in raw_links.find_all('a',href=True)]
    #print('\n'.join(links))

    for link in links:
        currentPageSoup = get_soup(link)

        #check if the page contains the coupon code
        IsUdemyCoupon = currentPageSoup.find(string="Get On Udemy")
        if IsUdemyCoupon:
            #append to coupon_links list which contains all links containing the udemy url
            coupon_links.append(link)

            coupon_link = currentPageSoup.find_all('a',attrs={'class':'eb-button-anchor'})
            coupons.append(coupon_link[0].get('href'))
            
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
    "coupon_url":pd.Series(coupons)

}
scraped_layer = pd.DataFrame(raw_data)

scraped_layer.to_csv("freewebcart.csv")