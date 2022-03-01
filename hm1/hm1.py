import requests
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


# вытаскивает все ссылки из html по url
def website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    scheme = urlparse(url).scheme
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for s in soup.select('header'):
        s.extract()
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin('https://habr.com/', href)
        if (not href.startswith('https://habr.com/ru/post/')) and (not href.startswith('https://habr.com/ru/company/')):
            continue
        href = href.split("?", maxsplit=1)[0]
        urls.add(href)
    return urls


# возвращает все ссылки html файла переходя по дургим ссылкам (пока не наюерется 100)
def all_website_links(url):
    urls = set()
    url_queue = []

    while len(urls) < 100:
        print(len(urls))
        locale_urls = website_links(url)
        dif_set = locale_urls.difference(urls)
        urls = urls.union(dif_set)
        url_queue.extend(dif_set)
        url = url_queue.pop(0)
    print(len(urls))
    print(urls)
    return urls


# скачивает html файлы
def upload_html(urls):
    dir = "html"
    os.mkdir(dir)

    i = 0
    for url in urls:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        name = dir + "/" + str(i) + ".html"
        with open(name, "w") as file:
            file.write(str(soup))
        with open('index.txt', 'a') as file:
            file.write(name + " : " + url + '\n')
        i += 1


u = all_website_links('https://habr.com/ru/all/')
upload_html(u)
