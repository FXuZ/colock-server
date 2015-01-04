#!/bin/env python2
# -*- encoding:utf-8 -*-

from functools import wraps

hooks = {}

def hook(*names):
    def decorator(func):
        commands = names
        if func.__name__ not in names:
            commands = names + (func.__name__,)

        for i in range(len(commands)):
            if isinstance( commands[i], basestring ):
                if commands[i] not in hooks:
                    hooks[commands[i]] = {"module": func.__module__, "func": func}

        @wraps(func)
        def wrapper(*args):
            return func(*args)

        return wrapper

    return decorator

def call_hook(name, *args):
    return hooks[name]["func"](*args)

@hook("test")
def testdeco(world):
    print "hello! %s" % world

if __name__ == "__main__":
    print hooks
    call_hook("test", "world")
