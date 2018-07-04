"""Main script of this project. Reads the data compiled by
compilation.py, takes user input, and filters against major/
course list."""
import _pickle as pickle
import compilation


def main():
    # FIXME
    Majors = load_majors()
    Depts = load_depts()
    Courses = load_courses()
    # run-time count of the number of courses from each major
    # the user has taken.
    course_count = dict.fromkeys(Majors, 0)
    # run-time list of Course objects taken by user.
    courses_taken = []
    # FIXME - get user input. this will be some kind of "while" loop.
    course_code = "CS 61A"
    # FIXME - add to courses_taken, update 

    pass


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
    # Loads and returns the list of Course objects from compilation.COURSES_PATH
    _file = open(compilation.COURSES_PATH, 'rb')
    Courses = pickle.load(_file)
    _file.close()
    return Courses


def filter_course(majors, course_count, course):
    # Iterates through each Major object in MAJORS and adds one to the
    # corresponding COURSE_COUNT dict value if COURSE (a string) is a course 
    # in the Major object.
    
    # FIXME
    pass

def get_course_object(name):
    # FIXME - make this throw error "not a valid abbrevation".