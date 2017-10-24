""" Script to parse through the UC Berkeley majors page,
    and compiles a list of classes required to declare each
    major. """
import sys

URL = http://guide.berkeley.edu/undergraduate/degree-programs/

def main():
    """Main entry point for script."""
    major_links = get_major_links(URL)
    major_prereqs = dict()
    for major in major_links:
        url = major_links[major]
        prereqs = get_major_prereqs(url)
        major_prereqs[major] = prereqs
    pass

def get_major_links(url):
    """Returns a dictionary mapping major names to
    the URL to their courses page."""
    pass

def get_major_prereqs(url):
    """Takes a single major's web page and returns a list
    of the classes needed to declare the major."""
    pass

if __name__ == '__main__':
    sys.exit(main)
