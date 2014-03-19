#import logging
from functools import wraps
import sys
import os

#logger = logging.getLogger(__name__)


_locals = {}

class persistent_locals(object):
    def __init__(self, func):
        self._locals = {}
        self._frame = {}
        self._function_name = ''
        self._filename = ''
        self._line_number = 0
        self.func = func
        self.test = 0

    def __call__(self, *args, **kwargs):
        def tracer(frame, event, arg):
            if event=='return':
                self._frame = frame
                self._function_name = frame.f_code.co_name
                self._filename = frame.f_code.co_filename
                self._line_number = frame.f_lineno
                self._locals = frame.f_locals.copy()
                self.test = self.test + 1

        # tracer is activated on next call, return or exception
        sys.setprofile(tracer)
        try:
            # trace the function call
            #res = self.func(*args, **kwargs)
            res = self.func(args)#*args, **kwargs)
        finally:
            # disable tracer and replace with old one
            sys.setprofile(None)

            path_split = os.path.dirname(os.path.abspath(__file__)).split('/')
            virtualenv_name = path_split[3]
            project_name = path_split[5]
            project_folder = '/opt/webapp/' + virtualenv_name + '/src/' + project_name + '/'
            profile_folder = project_folder + 'profile/'

            if not os.path.isdir(profile_folder): os.makedirs(profile_folder)

            # PRINT THE TIME OF WHEN THE CALL WAS MADE
            f = open(profile_folder + 'profiled_debug.txt', 'a')
            f.write("--------------------------------------------------------------------\n")
            f.write("%s:%s:%s:%s\n" % ( self.test, self._filename, self._function_name, self._line_number ))
            f.write("--------------------------------------------------------------------\n")
            for key in self._locals:
                f.write("%s= %s\n" % (key, self._locals[key]))
            f.write("\n")
            f.write("\n")
            f.write("\n")
            f.close()
        #import pdb;pdb.set_trace()
        return res

    def clear_locals(self):
        self._locals = {}

    @property
    def locals(self):
        return self._locals

'''
@persistent_locals
def debug_profile(func):
    """ 
    This decorator will check if my wrapper works.

    """
    @wraps(func)
    def wrapped(request):
        try:
            print("Hey")
            response = func(request)
            print("There")
        finally:
            path_split = os.path.dirname(os.path.abspath(__file__)).split('/')
            virtualenv_name = path_split[3]
            project_name = path_split[5]
            project_folder = '/opt/webapp/' + virtualenv_name + '/src/' + project_name + '/'
            profile_folder = project_folder + 'profile/'

            if not os.path.isdir(profile_folder): os.makedirs(profile_folder)

            f = open(profile_folder + 'profiled_debug.txt', 'a')
            f.write("Cool\n")
            f.write("Cool2\n")
            f.close()

        return response

    return wrapped
'''
