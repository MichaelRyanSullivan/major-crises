""" Script to parse through the UC Berkeley majors page,
    and compiles a list of classes required to declare each
    major. """
import sys
from bs4 import BeautifulSoup as bs
import requests as req
import re

URL = "http://guide.berkeley.edu/undergraduate/degree-programs/"

def main():
    """Main entry point for script."""
    major_links = get_major_links(URL)
    print(major_links)
    # major_classes = dict()
    # for major in major_links:
    #     url = major_links[major]
    #     major_classes[major] = get_major_classes(url)
    pass

def get_major_links(url):
    """Returns a dictionary mapping major names to
    the URL to their courses page."""
    soup = bs(req.get(url).text, "html.parser")
    scripts = soup.find_all('script')
    strScript = ''
    print(scripts)
    for script in scripts:
        string = str(script)
        if (len(string) > len(strScript)):
            strScript = string
    print(strScript)
    p_name = re.compile('name:"(.*)"')
    p_url = re.compile('url:"(.*)"')
    names = p_name.findall(strScript)
    urls = p_url.findall(strScript)
    assert(len(names) == len(urls))
    d = {}
    for i in range(len(names)):
        d[names[i]] = URL + urls[i] + "/"
    return d

def get_major_classes(url):
    """Takes a single major's web page and returns a list
    of the classes that count toward the major."""

    pass

if __name__ == '__main__':
    sys.exit(main)
