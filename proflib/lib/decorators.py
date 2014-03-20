from functools import wraps
import sys
import os
import time


# Can learn about all of the variables the frame object has at this page:
#   http://docs.python.org/2/library/inspect.html#inspect-types

Lock = 0

class persistent_locals(object):

    def __init__(self, func):
        self.locals_map = {}
        self.func = func
        self.num_functions_called = 0
        global Lock
        if Lock is None:
            Lock = 0

    def __call__(self, *args, **kwargs):
        global Lock
        if Lock == 1:
            try:
                res = self.func(*args, **kwargs)
            except:
                res = None
            return res
        else:
            Lock = 1;

        def tracer(frame, event, arg):
            timeStarted = time.time()
            if event=='return':
                function_name = frame.f_code.co_name
                self.num_functions_called = self.num_functions_called + 1
                self.locals_map[function_name+str(self.num_functions_called)] = {
                    'frame': frame,
                    'filename': frame.f_code.co_filename,
                    'line_number': frame.f_lineno,
                    'locals': frame.f_locals.copy(),
                    'function_name': function_name,
                    'time': timeStarted,
                    'called_by': frame.f_back.f_code.co_name,
                    'pos': self.num_functions_called,
                }

        sys.setprofile(tracer)
        try:
            res = self.func(*args, **kwargs)
        except:
            res = self.func(args)
        finally:
            sys.setprofile(None)

            path_split = os.path.dirname(os.path.abspath(__file__)).split('/')
            virtualenv_name = path_split[3]
            project_name = path_split[5]
            project_folder = '/opt/webapp/' + virtualenv_name + '/src/' + project_name + '/'
            profile_folder = project_folder + 'profile/'

            if not os.path.isdir(profile_folder): os.makedirs(profile_folder)

            f = open(profile_folder + 'profiled_debug.txt', 'a')
            banned_functions = ['__call__']

            f.write("####################################################################\n")
            #import pdb;pdb.set_trace()
            for key in self.locals_map:
                frame = self.locals_map[key]
                if frame['function_name'] in banned_functions:
                    continue
                f.write("====================================================================\n")
                f.write("--------------------------------------------------------------------\n")
                f.write("%s:%s:%s\n" % ( frame['filename'], frame['function_name'], frame['line_number'] ))
                f.write("--------------------------------------------------------------------\n")
                f.write("Called By: %s\n" % (frame['called_by']))
                f.write("--------------------------------------------------------------------\n")
                f.write("Num Function Called: %s\n" % (frame['pos']))
                f.write("--------------------------------------------------------------------\n")
                for var_name in frame['locals']:
                    f.write("%s= %s\n" % (var_name, frame['locals'][var_name]))
                f.write("====================================================================\n")
                f.write("\n")
                f.write("\n")
                f.write("\n")
            f.write("####################################################################\n")
            f.close()
        Lock = 0
        self.locals_map = {}
        self.num_functions_called = 0
        return res

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
