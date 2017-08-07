import requests
from bs4 import BeautifulSoup
import time
import json


def scrape_delicious_page(
        url: 'link to the Delicious page, including the username (eg. "https://del.icio.us/username?&page=1")') \
        -> "a list of bookmarks of the page organised in a dictionary":
    """Scrape bookmarks' data from a user's page on Delicious"""

    print('Send the request for ' + url)
    page = requests.get(url)
    print('Process')
    source = page.text
    soup = BeautifulSoup(source, "html.parser")
    outer_blocks = soup.find_all("div", class_="articleThumbBlockOuter")
    out = list()
    for block in outer_blocks:
        item_id = block.find("a")['href'].replace("/url/", "")
        title = block.find("a")['title']

        info = block.find("div", class_="articleInfoPan")
        link = info.find("a")['href']
        try:
            tag_names = block.find("ul", class_="tagName")("li")
            block_tags = list()
            for tag in tag_names:
                block_tags.append(tag.text)
        except:
            block_tags = list()
        d = {"id": item_id, "title": title, "link": link, "tags": block_tags}
        out.append(d)
    print('Finished with the page')
    return out





def scrape_delicious_user(username: 'Username as it appears in the url',
                          destination: 'Path and file name',
                          start_page: 'the number of the page to start scraping',
                          end_page: 'the number of the page to end the scraping') -> 'json with the title, link and tags of each entry of a delicious account':
    """This function scrapes the public bookmarks of a del.icio.us user. It returns the result as a json"""

    delay = 2
    obj = open(destination, "w+")
    obj.close()
    output_list = []
    num_pages = end_page - start_page
    for page in range(start_page, end_page+1):
        print("Add delay " + str(delay) + " s")
        time.sleep(delay)
        print("Scrape page " + str(page) + " (total pages:  " + str(num_pages +1) + ")")
        url_page = 'https://del.icio.us/' + username + '?&page=' + str(page)
        output_list.append(scrape_delicious_page(url_page))
    out = {"type": "Delicious bookmark collection",
           "username": username,
           "features": output_list,
           "collection_date": time.strftime("%d/%m/%Y %H:%M:%S")}
    print("Write the results in " + destination)
    with open(destination, "a+") as txt:
        txt.write(json.dumps(out))
    return out


