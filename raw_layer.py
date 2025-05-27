from scrapers import scrapers

for site,scraper in scrapers:
    print(f"running {site}")
    try:
        scraper()
    except Exception as e:
        print(e)
