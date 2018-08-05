import web
import utils
from compilation import Major
from compilation import Course

#TODO: add, remove, filter (department), errors

urls = (
    '/', 'index',
    '/add', 'add'
    )

render = web.template.render('templates')
# list with all Major objects
Maj_list = utils.load_majors()

# list with all Course objects
Course_list = utils.load_courses()

# dict mapping department abbreviations to their full names
Dept_dict = utils.load_depts()

# run-time count of the number of courses from each major
# the user has taken.
major_tracker = dict.fromkeys(Maj_list, 0)

# run-time sorted list based on major_count.
sorted_majors = Maj_list.copy()

# run-time list of courses added by user.
courses_taken = []

def add_course(course, major_tracker, courses_taken):
    # make sure course is valid. update major_tracker.
    try:
        course_obj = utils.get_course_object(course, Course_list)
        assert (course_obj not in courses_taken), "You already added that course!"
        courses_taken.append(course_obj)
        for major in Maj_list:
            if major.contains_course(course):
                major_tracker[major] += 1
    except LookupError as err:
        print(err)

class index:
    def GET(self):
        # FIXME - sort Majors list
        sorted_majors = sorted(major_tracker, key=major_tracker.__getitem__, reverse=True)
        return render.index(sorted_majors, major_tracker)
        
class add:
    def POST(self):
        # FIXME - get user input, direct back to index
        i = web.input()
        add_course(i.major_name, major_tracker, courses_taken)
        raise web.seeother('/')


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()