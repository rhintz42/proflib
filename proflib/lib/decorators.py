from functools import wraps
import sys
import os
import time
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
from outlib.lib.wout import output_to_logger

# Can learn about all of the variables the frame object has at this page:
#   http://docs.python.org/2/library/inspect.html#inspect-types

# This lock is here to prevent circular recursion with a function that has the
#   prof wrapper calling another function with the
#   prof wrapper
Lock = 0


def prof(depth=2):
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
            if event=='return':
                func.frame_list.add_frame(frame)

        @wraps(func)
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
                    res = func(*args, **kwargs)
                except:
                    res = None
                return res
            else:
                Lock = 1;

            # Start the Profiler
            sys.setprofile(tracer)
            try:
                response = func(*args, **kwargs)
            finally:
                # Stop the Profiler
                sys.setprofile(None)

            # Build a hierarchy of all the frames calling one another
            func.frame_list.build_hierarchy()

            # Print output to Logger
            output_to_logger(func.frame_list.to_json_output(depth=depth))

            # Reset Things
            func.frame_list = FrameList()
            Lock = 0

            return response

        return wrapped
    return actual_decorator
