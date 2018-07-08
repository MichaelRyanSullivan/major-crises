"""Main script of this project. Reads the data compiled by
compilation.py, takes user input, and filters against major/
course list."""
import _pickle as pickle
import compilation
import cmd


def main():
    # FIXME
    prompt = CoursePrompt()
    prompt.cmdloop

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
    # Loads and returns the list of Course objects
    # from compilation.COURSES_PATH
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
    pass


class CoursePrompt(cmd.Cmd):
    """Prototype command processor.
    Commands: add (course), remove (course),
    filter (department), display """
    Majors = load_majors()
    Depts = load_depts()
    Courses = load_courses()
    # run-time count of the number of courses from each major
    # the user has taken.
    course_count = dict.fromkeys(Majors, 0)
    # run-time list of Course objects taken by user.
    courses_taken = []
    # number of majors to display, default 10.
    DISPLAY_CAP = 10

    def do_add(self, course):
        """add [course]
        Add the given course to list of courses taken."""
        # FIXME
        if course in self.courses_taken:
            # raise some error about it being there
            return
        else:
            self.course_obj = get_course_object(course)
            self.courses_taken.append(course)
            self.do_display()
        pass

    def do_remove(self, course):
        """remove [course]
        Remove the given course from the list of courses
        taken. Course must be in the current list."""
        # FIXME
        pass

    def do_display(self):
        """display
        Displays the current sorted list of majors. """
        # FIXME
        pass

    def do_filter(self, dept):
        """filter [department abbreviation]
        Filters the list of majors to only have those under
        the given department.  """
        # FIXME - first scrape for department of each major.
        pass


if __name__ == '__main__':
    CoursePrompt().cmdloop()
    