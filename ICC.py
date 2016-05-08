"""
Indeed Resume Crawler.

Use requests, beautiful soup and regex to get all the resumes from indeed.com.
"""

import requests
from bs4 import BeautifulSoup
import re
import time


def indeed_crawler(query, location, start):
    """Indeed Resume Crawler Function."""
    payload = dict()
    payload['q'] = query
    if location != 'None':
        payload['l'] = location
    if start > 0:
        payload['start'] = start * 50
    for k, v in payload.items():
        print(k, v)
    r = requests.get('http://www.indeed.com/resumes', params=payload)
    data = r.text
    print(r.status_code)
    print(r.url)

    soup = BeautifulSoup(data, 'html.parser')
    for a in soup.find('ol').find_all('a', href=re.compile('/r/.+/.+')):
        link = re.sub('\?.+', '', a['href'])
        file_name = re.search('/r/(.+)/.+', a['href']).group(1) + '.pdf'
        url = "http://www.indeed.com" + link + '/pdf'
        print(url)
        print('Downloading {}'.format(file_name))
        resume = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in resume.iter_content(512):
                f.write(chunk)


def resume_downloader(query, location, pages):
    """Download resumes in batch."""
    for i in range(0, pages, 1):
        print(i)
        indeed_crawler(query, location, i)
        time.sleep(5)


if __name__ == '__main__':
    resume_downloader('C++', 'None', 3)
