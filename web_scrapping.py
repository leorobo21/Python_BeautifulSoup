from bs4 import BeautifulSoup
import requests
import csv


def crawl_pages(url):
    page = 0
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    api_table = soup.find("tbody")
    tab = api_table.find_all("tr")
    for tab in api_table:
        api_name = tab.find("a").text
        api_url = tab.find("a").get("href")
        api_category = tab.find("td", {"class": "views-field views-field-field-article-primary-category"}).text
        api_description = tab.find("td", {"class": "views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"}).text
        # print(api_name)
        # print("https://www.programmableweb.com"+api_url)
        # print(api_category)
        # print(api_description)
        csv_writer.writerow([api_name, "https://www.programmableweb.com"+api_url, api_category, api_description])  
    try:
        url_tag = soup.find("a", {"title": "Go to next page"})
        if url_tag.get('href'):
            url = "https://www.programmableweb.com"+url_tag.get("href")
            page +=1
            crawl_pages(url)
        else:
            print(page, "hreif")
            pass
    except Exception as e:
        print(page, e)
        pass    
url = "https://www.programmableweb.com/category/all/apis"
csv_file = open('udemy.csv', 'w', encoding="utf-8", newline='')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['API Name', 'API (absolute) URL', 'API Category', 'API Description'])

crawl_pages(url)
csv_file.close()
