""" Script to parse through the UC Berkeley majors page,
    and compiles a list of classes required to declare each
    major. Serializes the resultant dictionary in the data 
    directory.
    """
import sys
from bs4 import BeautifulSoup as bs
import requests as req
import re
import _pickle as pickle


# TODO differentiate between majors/minors
# TODO add major info? - DEPARTMENT!
i = 1
URL = "http://guide.berkeley.edu/undergraduate/degree-programs/"
MAJORS_PATH = "data/Majors"
DEPTS_PATH = "data/Depts"
COURSES_PATH = "data/Courses"
# Maps department abbreviations to full names.
dept_dict = {}
# List of all unique Course objects.
Courses = []


def main():
    """Main entry point for script."""
    Majors = fill_major_links(URL)
    # fills Major objects with corresponding Courses.
    for major in Majors:
        major.get_major_classes()
    _file = open(MAJORS_PATH, 'wb')
    pickle.dump(Majors, _file)
    _file.close()
    _file = open(DEPTS_PATH, 'wb')
    pickle.dump(dept_dict, _file)
    _file.close()
    _file = open(COURSES_PATH, 'wb')
    pickle.dump(Courses, _file)
    _file.close()
    pass


class Major:
    def __init__(self, name, link):
        self.courses = []
        self.name = name
        self.link = link
    
    def __str__(self):
        return self.name

    def contains_course(self, course):
        # COURSE must be a proper course abbreviation.
        return course in self.courses

    def add_course(self, course):
        # COURSE must be a proper course abbreviation.
        assert course not in self.courses
        self.courses.append(course)

    def get_major_classes(self):
        """Adds all Course objects corresponding to this Major. Also builds
        global COURSES list with Course objects. """
        global Courses
        global i
        print(i)
        i += 1
        url = self.link
        soup = bs(req.get(url).text, "html.parser")
        courseblocks = soup.find_all('div', class_='courseblock')
        for course_tag in courseblocks:
            course_code = course_tag.find('span', class_='code').contents[0]
            # formatting the abbreviation uniformly
            course_code = course_code.replace(u'\xa0', u' ')
            course_code = course_code.replace(u'&amp;', u'&')
            full_name = str(course_tag.find('span', class_='title').contents[0])
            units = str(course_tag.find('span', class_='hours').contents[0])
            if not self.contains_course(course_code):
                # adds course code to this major
                self.add_course(course_code)
                course = Course(course_code, full_name, units)
                if course not in Courses:
                    # adds Course object to Courses
                    Courses.append(course)
                dept_abbrev = isolate_dept(course_code)
                if dept_abbrev not in dept_dict:
                    # adds dept abbreviation to the dictionary
                    add_dept(dept_abbrev, course_tag)
        return


class Course:
    def __init__(self, abbrev, full_name, units):
        self.abbrev = abbrev
        self.full_name = full_name
        self.units = units
        self.dept = isolate_dept(abbrev)
    
    def __str__(self):
        return "abbrev: " + self.abbrev + "\nfull name: " + self.full_name + "\nunits: " + self.units
    
    def __eq__(self, other):
        return self.abbrev == other.abbrev


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
    Majors = []
    for i in range(len(names)):
        link = url + urls[i] + "/"
        Majors.append(Major(names[i], link))
    return Majors


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
                return True
    return False


def isolate_dept(course_code):
    # Takes a course abbreviation (i.e. CS 61A) and returns the department 
    # abbreviation (i.e. CS)
    # FIXME
    p_dept_name = re.compile("(([A-Z\/,-]+) )+")
    dept_abbrev = p_dept_name.match(course_code).group().strip()
    return dept_abbrev




if __name__ == '__main__':
    main()
