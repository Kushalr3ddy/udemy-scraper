from .cc import scrape_cc
from .ci import scrape_ci
from .fwc import scrape_fwc
from .idc import scrape_idc

scrapers =[
("coursecouponz",  scrape_cc),
("courses.impodays", scrape_ci),
("freewebcart", scrape_fwc),
("idownloadcoupon", scrape_idc)
]