from django.test import TestCase
from colock import utils

# Create your tests here.
@utils.hook()
def testmsg(world):
    print "hello! %s" % world
