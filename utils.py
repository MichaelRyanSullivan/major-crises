import _pickle as pickle
import compilation
import cmd
from compilation import Major
from compilation import Course

def load_majors():
    # Loads and returns the list of Major objects from
    # compilation.MAJORS_PATH
    _file = open(compilation.MAJORS_PATH, "rb")
    Majors = pickle.load(_file)
    _file.close()
    return Majors


def load_depts():
    # Loads and returns the dictionary of department abbrevs.
    # from compilation.DEPTS_PATH.
    _file = open(compilation.DEPTS_PATH, 'rb')
    Depts = pickle.load(_file)
    _file.close()
    return Depts


def load_courses():
    # Loads and returns the list of Course objects
    # from compilation.COURSES_PATH
    _file = open(compilation.COURSES_PATH, 'rb')
    Courses = pickle.load(_file)
    _file.close()
    return Courses


def filter_course(majors, major_count, course):
    # Iterates through each Major object in MAJORS and adds one to the
    # corresponding major_count dict value if COURSE (a string) is a course
    # in the Major object.
    # FIXME
    return

def get_major_object(name, Majors):
    # NAME is the full name
    for major in Majors:
        if major.name == name:
            return major
    raise LookupError('Not a valid major.')


def get_course_object(name, Courses):
    # assumes is a valid object
    for course in Courses:
        if course.abbrev == name:
            return course
    raise LookupError('Not a valid course.')

