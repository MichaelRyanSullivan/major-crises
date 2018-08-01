"""Main script of this project. Reads the data compiled by
compilation.py, takes user input, and filters against major/
course list."""
import _pickle as pickle
import compilation
import cmd
from compilation import Major
from compilation import Course


def main():
    # FIXME
    prompt = CoursePrompt()
    prompt.cmdloop

    return


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

def get_major_object(name):
    # NAME is the full name
    global Majors
    for major in Majors:
        if major.name == name:
            return major
    raise LookupError('Not a valid major.')


def get_course_object(name):
    # assumes is a valid object
    global Courses
    for course in Courses:
        if course.abbrev == name:
            return course
    raise LookupError('Not a valid course.')


# def is_course(name):
#     """checks NAME (str) against the list of courses COURSES to check if
#     any course has the name NAME. """
#     global Courses
#     for course in Courses:
#         if course.abbrev == name:
#             return True
#     return False


Majors = load_majors()
Depts = load_depts()
Courses = load_courses()


class CoursePrompt(cmd.Cmd):
    """Prototype command processor.
    Commands: add (course), remove (course),
    filter (department), show_majors, show_courses, change_cap"""
    global Majors
    # run-time count of the number of courses from each major
    # the user has taken.
    major_count = dict.fromkeys(Majors, 0)
    # run-time sorted list based on major_count.
    sorted_majors = Majors.copy()
    # run-time list of Course objects taken by user.
    courses_taken = []
    # number of majors to display, default 10.
    DISPLAY_CAP = 10

    def update(self):
        """Rearranges sorted_majors to reflect changes to
        major_count."""
        self.sorted_majors = sorted(self.major_count, key=self.major_count.__getitem__, reverse=True)
        return

    def do_add(self, course):
        """add [course]
        Add the given course to list of courses taken."""
        # FIXME - make sure it is a valid course. update major_count.
        try:
            course_obj = get_course_object(course)
            assert (course_obj not in self.courses_taken), "You already added that course!"
            self.courses_taken.append(course_obj)
            for major in Majors:
                if major.contains_course(course):
                    self.major_count[major] += 1
        except LookupError as err:
            print(err)
        return

    def do_remove(self, course):
        """remove [course]
        Remove the given course from the list of courses
        taken. Course must be in the current list."""
        assert (course in self.courses_taken), "You haven't added that course!"
        self.courses_taken.remove(course)
        for major in Majors:
            if major.contains_course(course):
                self.major_count[major] -= 1
        return

    def do_show_majors(self, line):
        """majors
        Displays the current sorted list of majors. """
        self.update()
        for i in range(self.DISPLAY_CAP):
            print(self.sorted_majors[i])
        return

    def do_show_courses(self, line):
        """courses
        Displays the current list of courses tracked. """
        for course in self.courses_taken:
            print(course)
        return

    def do_filter(self, dept):
        """filter [department abbreviation]
        Filters the list of majors to only have those under
        the given department.  """
        # FIXME - first scrape for department of each major.
        return

    def do_change_cap(self, num):
        """change_cap [number]
        Changes the number of majors displayed by the command
        'majors' to NUMBER. Default is 10.
        """
        self.DISPLAY_CAP = num
        return


if __name__ == '__main__':
    CoursePrompt().cmdloop()
