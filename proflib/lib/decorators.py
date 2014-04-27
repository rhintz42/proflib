from functools import wraps
import sys
import os
import time
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
from outlib.lib.wout import output_to_logger, output_to_file
import coverage
import logging

# Can learn about all of the variables the frame object has at this page:
#   http://docs.python.org/2/library/inspect.html#inspect-types

# This lock is here to prevent circular recursion with a function that has the
#   prof wrapper calling another function with the
#   prof wrapper
Lock = 0
Write_Called = 0

# Used for parsing xml output from std.out to a variable
import contextlib
@contextlib.contextmanager
def capture():
    import sys
    from cStringIO import StringIO
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()
        #import pdb;pdb.set_trace()


def prof(depth=2, include_keys=None, include_variables=None, exclude_keys=None,
            exclude_variables=None):
    def actual_decorator(func):
        """ 
        This decorator will check if my wrapper works.

        """
        func.frame_list = FrameList()

        global Lock
        if Lock is None:
            Lock = 0

        def tracer(frame, event, arg):
            """
            Called by the sys.setprofile method on every event. The function
                checks to see if the event was a return, and if it is, save
                this frame.
            """
            # THE ARG ARGUMENT SHOULD BE THE RETURN VALUE FROM THE FUNCTION
            if event=='return':
                func.frame_list.add_frame(frame, arg=arg)

        @wraps(func)    # TRACE WRAPPER
        def wrapped(*args, **kwargs):
            """
            This function does all the heavy-lifting of the function, setting
                the sys.setprofile to start for the function being called.
            Will check that the wrapper hasn't been called by a function that
                has called the current function
            Clear the data saved in func after done
            """
            global Lock
            if Lock == 1:
                try:
                    # THIS *SHOULD BE* THE RETURN FROM THE FUNCTION JUST CALLED
                    res = func(*args, **kwargs)
                    #output_to_logger(res)
                except:
                    res = None
                return res
            else:
                Lock = 1;

            # Start the Profiler
            #cov = coverage.coverage()
            #cov.start()
            sys.setprofile(tracer)

            try:
                response = func(*args, **kwargs)
            finally:
                # Stop the Profiler
                sys.setprofile(None)

            # Build a hierarchy of all the frames calling one another
            func.frame_list.build_hierarchy()
            #cov.stop()
            #cov.save()

            global Write_Called
            Write_Called += 1

            # Print output to Logger
            output_to_logger(func.frame_list.to_json_output( \
                depth=depth,
                include_keys=include_keys,
                include_variables=include_variables,
                exclude_keys=exclude_keys,
                exclude_variables=exclude_variables))

            # Print output to File
            """
            output_to_file('/opt/webapp/proflib_visualizer/src/proflib_visualizer/proflib_visualizer/static/json/proflib_json_files/test_%s.json' %(Write_Called),
                            func.frame_list.to_json_output( \
                                depth=depth,
                                include_keys=include_keys,
                                include_variables=include_variables,
                                exclude_keys=exclude_keys,
                                exclude_variables=exclude_variables),
                            append=False)
            """
            
            #import subprocess
            #proc = subprocess.Popen(["python", "-c", "cov.xml_report(outfile='-')"], stdout=subprocess.PIPE)
            #out = proc.communicate()[0]
            #import pdb;pdb.set_trace()
            #with capture() as out:
            #    cov.xml_report(outfile='-')

            # Reset Things
            func.frame_list = FrameList()
            Lock = 0

            return response

        return wrapped
    return actual_decorator
