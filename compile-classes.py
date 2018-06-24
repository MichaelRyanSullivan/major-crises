""" Script to parse through the UC Berkeley majors page,
    and compiles a list of classes required to declare each
    major. Writes a file to the repository of the format:
    MAJOR1 CLASS1 CLASS2...
    MAJOR2 CLASS1 ....
    ...
    """
import sys
from bs4 import BeautifulSoup as bs
import requests as req
import re
try:
    import _pickle as pickle
except:
    import pickle



URL = "http://guide.berkeley.edu/undergraduate/degree-programs/"
# def main():
#     """Main entry point for script."""
#     major_links = get_major_links(URL)
#     print(major_links)
    #Maps majors to a list of classes that fulfill requirements.
    # major_classes = dict()
    # for major in major_links:
    #     url = major_links[major]
    #     major_classes[major] = get_major_classes(url)
    # write_to_file(major_classes)


def get_major_links(url):
    """Returns a dictionary mapping major names to
    the URL to their courses page."""
    soup = bs(req.get(url).text, "html.parser")
    scripts = soup.find_all('script')
    strScript = ''
    for script in scripts:
        string = str(script)
        if (len(string) > len(strScript)):
            strScript = string
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
    classes = []
    soup = bs(req.get(url).text, "html.parser")
    bubble_classes = soup.find_all("a", class_="bubblelink code")
    # p_class = re.compile("showCourse\(this, '([A-Z ]+ *[A-Z]*[0-9]+[A-Z]*)'\)")
    # p_class = re.compile("showCourse\(this, '(.*)'")
    p_class = re.compile('href=".*">(.*)</a>')
    p_num = re.compile(" *([A-Z]*[0-9]+[A-Z]*)")
    p_name = re.compile("(([A-Z\/]+) )+")
    prev = ""
    for bubble in bubble_classes:
        m = p_class.search(str(bubble))
        _class = m.group(1)
        print(repr(_class))
        _class = _class.replace(u'\xa0', u' ')
        _class = _class.replace(u'&amp;', u'&')
        num_match = p_num.match(_class)
        if num_match:
            print(prev)
            num = num_match.group().strip()
            prev_name_match = p_name.match(prev)
            prev_name = prev_name_match.group().strip()
            _class = prev_name + " " + num
        if _class not in classes:
            classes.append(_class)
            prev = _class
    return classes

def write_to_file(major_classes):
    """Takes a dictionary of majors to a list of classes that fulfill
       requirements, MAJOR_CLASSES, and writes those requirements to
       a file in the repository."""
    with open('major_requirements.txt', 'wt+') as _file:
        for major in major_classes:
            _file.write(major + ";")
            reqs = major_classes[major]
            for req in reqs:
                _file.write(" " + req)
            _file.write("\n")

def read_from_file():
    """Reads requirements from major_requirements.txt and returns a dictionary
    """

major_links = get_major_links(URL)

# main()
# if __name__ == '__main__':
#     sys.exit(main)
