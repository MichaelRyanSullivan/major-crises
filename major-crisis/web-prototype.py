import web
import utils
from compilation import Major
from compilation import Course

urls = (
    '/', 'index'
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


class index:
    def GET(self):
        # FIXME - sort Majors list
        sorted_majors = sorted(major_tracker, key=major_tracker.__getitem__, reverse=True)
        return render.index(sorted_majors, major_tracker)
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()