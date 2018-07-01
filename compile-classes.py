""" Script to parse through the UC Berkeley majors page,
    and compiles a list of classes required to declare each
    major. Serializes the resultant dictionary in data/
    ...
    """
import sys
from bs4 import BeautifulSoup as bs
import requests as req
import re
import _pickle as pickle


# TODO differentiate between majors/minors
i = 1
URL = "http://guide.berkeley.edu/undergraduate/degree-programs/"
dept_dict = {}


class Major:
    # FIXME. Thinking: course objects (list), link to website,
    # some other info?
    def __init__(self, courses, link):
        self.courses = courses
        self.link = link


class Course:
    # FIXME. Thinking: abbrev, full_name, units
    def __init__(self, abbrev, full_name, units):
        self.abbrev = abbrev
        self.full_name = full_name 
        self.units = units

def main():
    """Main entry point for script."""
    major_links = fill_major_links(URL)
    # Maps majors to a list of classes that fulfill requirements.
    major_classes = dict()
    for major in major_links:
        url = major_links[major]
        major_classes[major] = get_major_classes(url)
    _file = open('data/major_classes', 'wb')
    pickle.dump(major_classes, _file)
    _file = open('data/dept_dict', 'wb')
    pickle.dump(dept_dict, _file)
    pass


def fill_major_links(url):
    """Returns a list of Major objects corresponding to each
    major with the links added to the major's website for each
    object. """
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
        d[names[i]] = url + urls[i] + "/"
    return d


def get_major_classes(url):
    """Takes a single major's web page and returns a list
        of the classes that count toward the major."""
    global i
    course_codes = []
    print(i)
    i += 1
    soup = bs(req.get(url).text, "html.parser")
    # FIXME do I need these re's?
    p_name = re.compile("(([A-Z\/,-]+) )+")
    courseblocks = soup.find_all('div', class_='courseblock')
    for course_tag in courseblocks:
        course_code = course_tag.find('span', class_='code').contents[0]
        course_code = course_code.replace(u'\xa0', u' ')
        course_code = course_code.replace(u'&amp;', u'&')
        if course_code not in course_codes:
            course_codes.append(course_code)
            dept_abbrev = p_name.match(course_code).group().strip()
        if dept_abbrev not in dept_dict:
            add_dept(dept_abbrev, course_tag)

        # TODO: MAKE A "COURSE" CLASS TO HOLD MORE INFO.
        # couse_name_full = course_tag.find('span', class_='title').contents[0]
        # course_units = course_tag.find('span', class_='hours').contents[0]
    return course_codes


def add_dept(dept_abbrev, course_tag):
    """Takes a <div class="courseblock"'> bs4 tag object and adds a
    mapping from the dept. abbreviation, DEPT_NAME, of the course to
    the full dept. name. Coursetag has the following children path:
        <div class="courseblock">
            <div class="coursebody">
                <div class="coursedetails">
                    <div class="course-section">
                        <p> ... </p>
    Returns True if successfully added, False otherwise.
    """
    p_dept = re.compile("'(.*)/Undergraduate'")
    for course_section in course_tag.find_all('div', class_="course-section"):
        for string in course_section.stripped_strings:
            string = repr(string)
            dept_match = p_dept.match(string)
            if dept_match:
                dept_full = dept_match.group(1)
                dept_dict[dept_abbrev] = dept_full
                print(dept_dict)
                return True
    return False


if __name__ == '__main__':
    sys.exit(main)
