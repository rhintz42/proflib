#import logging
from functools import wraps
#import threading
import sys
import os

#logger = logging.getLogger(__name__)

Thing = 0

class persistent_locals(object):

    def __init__(self, func):
        self.locals_map = {}
        self._locals = {}
        self._frame = {}
        self._function_name = ''
        self._filename = ''
        self._line_number = 0
        self.func = func
        self.test = 0
        global Thing
        if Thing is None:
            Thing = 0

    def __call__(self, *args, **kwargs):
        global Thing
        if Thing == 1:
            try:
                res = self.func(*args, **kwargs)
            except:
                res = None
            return res
        else:
            Thing = 1;

        def tracer(frame, event, arg):
            if event=='return':
                self.locals_map[frame.f_code.co_name] = {
                    'frame': frame,
                    'filename': frame.f_code.co_filename,
                    'line_number': frame.f_lineno,
                    'locals': frame.f_locals.copy(),
                }
                self.test = self.test + 1

        # tracer is activated on next call, return or exception
        #import pdb;pdb.set_trace()
        #threading.setprofile(tracer)
        sys.setprofile(tracer)
        try:
            # trace the function call
            res = self.func(*args, **kwargs)
        except:
            res = self.func(args)#*args, **kwargs)
        finally:
            # disable tracer and replace with old one
            #threading.setprofile(None)
            sys.setprofile(None)

            #import pdb;pdb.set_trace()
            path_split = os.path.dirname(os.path.abspath(__file__)).split('/')
            virtualenv_name = path_split[3]
            project_name = path_split[5]
            project_folder = '/opt/webapp/' + virtualenv_name + '/src/' + project_name + '/'
            profile_folder = project_folder + 'profile/'

            if not os.path.isdir(profile_folder): os.makedirs(profile_folder)

            # PRINT THE TIME OF WHEN THE CALL WAS MADE
            f = open(profile_folder + 'profiled_debug.txt', 'a')
            for function_name in self.locals_map:
                frame = self.locals_map[function_name]
                f.write("--------------------------------------------------------------------\n")
                f.write("%s:%s:%s\n" % ( frame['filename'], function_name, frame['line_number'] ))
                f.write("--------------------------------------------------------------------\n")
                for key in frame['locals']:
                    f.write("%s= %s\n" % (key, frame['locals'][key]))
                f.write("\n")
                f.write("\n")
                f.write("\n")
            f.close()
        #import pdb;pdb.set_trace()
        Thing = 0
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
