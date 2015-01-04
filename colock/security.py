__author__ = 'Chengyu'


def injection_filter(s):
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]
    for stuff in dirty_stuff:
        s = s.replace(stuff, "")
    return s
# prevent injection