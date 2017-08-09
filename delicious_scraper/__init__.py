import requests
from bs4 import BeautifulSoup
import time
import calendar
import re
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
        s = str(info.find_all("p"))
        date = re.findall(r'luposky<\/a> on ([^;]*[0-9])<\/p>', s)
        date = time.strptime(date[0], '%B %d, %Y')
        date_from_1970 = calendar.timegm(date)
        try:
            tag_names = block.find("ul", class_="tagName")("li")
            block_tags = list()
            for tag in tag_names:
                block_tags.append(tag.text)
        except:
            block_tags = list()
        d = {"id": item_id, "title": title, "link": link, "tags": block_tags, "date":date_from_1970}
        out.append(d)
    print('Finished with the page')
    return out


def scrape_delicious_user(username: 'Username as it appears in the url',
                          destination: 'Path and file name',
                          start_page: 'the number of the page to start scraping',
                          end_page: 'the number of the page to end the scraping',
                          file_format: 'json or netscape bookmark file') -> 'json with the title, link and tags of each entry of a delicious account':
    """This function scrapes the public bookmarks of a del.icio.us user. It returns the result as a json"""
    delay = 2
    obj = open(destination, "w+")
    obj.close()
    output_list = []
    num_pages = end_page - start_page
    for page in range(start_page, end_page+1):
        print("Add delay " + str(delay) + " s")
        time.sleep(delay)
        print("Scrape page " + str(page) + " (total pages:  " + str(num_pages + 1) + ")")
        url_page = 'https://del.icio.us/' + username + '?&page=' + str(page)
        output_list.append(scrape_delicious_page(url_page))
    out = {"type": "Delicious bookmark collection",
           "username": username,
           "features": output_list,
           "collection_date": time.strftime("%d/%m/%Y %H:%M:%S")}
    print("Write the results in " + destination)
    if file_format == "json":
        with open(destination, "a+") as txt:
            txt.write(json.dumps(out))
    if file_format == "html":
        html = open(destination, "a+")
        html.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
        html.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
        html.write('<!-- This is an automatically generated file. It will be read and overwritten. Do Not Edit! -->')
        html.write('<TITLE>Bookmarks</TITLE>')
        html.write('<H1>Bookmarks</H1>')
        html.write('<DL><p>')
        count = 1
        for page in out['features']:
            try:
                for bookmark in page:
                    title = bookmark['title']
                    link = bookmark['link']
                    tags = bookmark['tags']
                    date = bookmark['date']
                    line = '<dt><a href="' + link + '" add_date=' + str(date) + ' private="0" tags="' + ",".join(
                        tags) + '">' + title + '</a>'
                    html.write(line)
                    print(count)
                    print(line)
                    count += 1
            except IndexError:
                continue

        html.write('</DL><p>')
        html.close()
    else:
        print("Not valid file format")
    return out


