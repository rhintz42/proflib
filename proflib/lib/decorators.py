from functools import wraps
import sys
import os
import time
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
from outlib.lib.wout import output_to_logger

# Can learn about all of the variables the frame object has at this page:
#   http://docs.python.org/2/library/inspect.html#inspect-types

# TODO
#   * Create a Frame Model
#       * Will store all of the functions and such
#       * Will have a parent and children
#       * Need to make sure every time a function is called, it's accounted
#           for
#       * Should be organized something like this:
#           func_name: {
#               func_called
#   * Create an organize function that will organize things better so that
#       functions called by parent functions will be "Inside" their parents


# This lock is here to prevent circular recursion with a function that has the
#   persistent_locals wrapper calling another function with the
#   persistent_locals wrapper
Lock = 0

# Should reset the frame list if this value is anything other than 0
TIMES_CALLED = 0

# ADD PARAMETER FOR THE DEPTH WANT TO GO
def persistent_locals(depth=2):
    def actual_decorator(func):
        """ 
        This decorator will check if my wrapper works.

        """
        func.frame_list = FrameList()
        global Lock
        if Lock is None:
            Lock = 0

        def tracer(frame, event, arg):
            if event=='return':
                func.frame_list.add_frame(frame)

        @wraps(func)
        def wrapped(*args, **kwargs):
            global Lock
            if Lock == 1:
                try:
                    res = func(*args, **kwargs)
                except:
                    res = None
                return res
            else:
                Lock = 1;

            sys.setprofile(tracer)
            try:
                response = func(*args, **kwargs)
            finally:
                sys.setprofile(None)

            func.frame_list.build_hierarchy()

            output_to_logger(func.frame_list.to_json_output(depth=depth))

            #CLEAR FRAME_LIST. IT SEEMS TO BE CACHED IF NOT
            func.frame_list = FrameList()
            Lock = 0
            return response

        return wrapped
    return actual_decorator


'''
class persistent_locals(object):

    def __init__(self, func):
        self.locals_map = {}
        self.func = func
        self.functions_in_order = []
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
                pos = len(self.functions_in_order)
                function_name = frame.f_code.co_name
                key = function_name+str(pos)
                self.functions_in_order.append(key)
                self.locals_map[key] = {
                #self.locals_map[function_name] = {
                    'frame': frame,
                    'filename': frame.f_code.co_filename,
                    'line_number': frame.f_lineno,
                    'locals': frame.f_locals.copy(),
                    'function_name': function_name,
                    'time': timeStarted,
                    'called_by': frame.f_back.f_code.co_name,
                    'pos': pos,
                }

        sys.setprofile(tracer)
        try:
            res = self.func(object, *args, **kwargs)
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
            #for key in self.locals_map:
            for key in self.functions_in_order:
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
        self.functions_in_order = []
        return res
'''
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
