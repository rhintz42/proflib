from functools import wraps
import sys
import os
import time
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
from outlib.lib.wout import output_to_logger, output_to_file
import coverage
import logging
import linecache
import venusian

logger = logging.getLogger(__name__)

# TODO
#   * Be able to generate coverage report
#       * See the lines I've hit
#   * Be able to Write output to specified file
#   * Take notes from:
#       * /opt/webapp/anweb/lib/python2.7/site-packages/pyramid/view.py:view_config
#       * /opt/webapp/anweb/lib/python2.7/site-packages/venusian/__init__.py:attach
#       * http://python-3-patterns-idioms-test.readthedocs.org/en/latest/PythonDecorators.html
#   * Debug the trace function using logging
#   * Create tests for the trace function

# Can learn about all of the variables the frame object has at this page:
#   http://docs.python.org/2/library/inspect.html#inspect-types

# This lock is here to prevent circular recursion with a function that has the
#   prof wrapper calling another function with the
#   prof wrapper
Lock = 0
Write_Called = 0
Depth = 0

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


def prof(depth=3, include_keys=None, include_variables=None, exclude_keys=None,
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
            global Depth
            if event == "call":
                Depth += 1
            if event == "return":
                if Depth > depth:
                    Depth -= 1
                    return
                lineno = frame.f_lineno
                name = frame.f_globals["__name__"]
                Depth -= 1
                func.frame_list.add_frame(frame, arg=arg)
            return tracer

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
            global Depth
            Depth += 1

            if Lock == 1:
                try:
                    # THIS *SHOULD BE* THE RETURN FROM THE FUNCTION JUST CALLED
                    res = func(*args, **kwargs)
                except:
                    res = None

                return res
            else:
                Lock = 1;

            # Start the Profiler
            sys.settrace(tracer)

            try:
                args2 = (args[1],)
                response = func(*args2, **kwargs)
                #response = func(*args, **kwargs)
            finally:
                # Stop the Profiler
                sys.settrace(None)

            # Build a hierarchy of all the frames calling one another
            func.frame_list.build_hierarchy()

            global Write_Called
            Write_Called += 1

            # Print output to Logger
            res = func.frame_list.to_json_output( \
                depth=depth,
                include_keys=include_keys,
                include_variables=include_variables,
                exclude_keys=exclude_keys,
                exclude_variables=exclude_variables)

            try:
                output_to_logger(res)
            except:
                # Something went wrong with the logger
                a = 10

            # Reset Things
            func.frame_list = FrameList()
            Depth = 0
            Lock = 0

            return response

        return wrapped
    return actual_decorator


class prof2(object):
    """ A function, class or method :term:`decorator` which allows a
    developer to create view registrations nearer to a :term:`view
    callable` definition than use :term:`imperative
    configuration` to do the same.

    For example, this code in a module ``views.py``::

      from resources import MyResource

      @view_config(name='my_view', context=MyResource, permission='read',
                   route_name='site1')
      def my_view(context, request):
          return 'OK'

    Might replace the following call to the
    :meth:`pyramid.config.Configurator.add_view` method::

       import views
       from resources import MyResource
       config.add_view(views.my_view, context=MyResource, name='my_view',
                       permission='read', route_name='site1')

    .. note: :class:`pyramid.view.view_config` is also importable, for
             backwards compatibility purposes, as the name
             :class:`pyramid.view.bfg_view`.

    :class:`pyramid.view.view_config` supports the following keyword
    arguments: ``context``, ``permission``, ``name``,
    ``request_type``, ``route_name``, ``request_method``, ``request_param``,
    ``containment``, ``xhr``, ``accept``, ``header``, ``path_info``,
    ``custom_predicates``, ``decorator``, ``mapper``, ``http_cache``,
    ``match_param``, ``csrf_token``, ``physical_path``, and ``predicates``.

    The meanings of these arguments are the same as the arguments passed to
    :meth:`pyramid.config.Configurator.add_view`.  If any argument is left
    out, its default will be the equivalent ``add_view`` default.

    An additional keyword argument named ``_depth`` is provided for people who
    wish to reuse this class from another decorator.  The default value is
    ``0`` and should be specified relative to the ``view_config`` invocation.
    It will be passed in to the :term:`venusian` ``attach`` function as the
    depth of the callstack when Venusian checks if the decorator is being used
    in a class or module context.  It's not often used, but it can be useful
    in this circumstance.  See the ``attach`` function in Venusian for more
    information.
    
    .. seealso::
    
        See also :ref:`mapping_views_using_a_decorator_section` for
        details about using :class:`pyramid.view.view_config`.

    .. warning::
    
        ``view_config`` will work ONLY on module top level members
        because of the limitation of ``venusian.Scanner.scan``.

    """
    venusian = venusian # for testing injection
    def __init__(self, *args, **settings):
        if 'for_' in settings:
            if settings.get('context') is None:
                settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped, *args):
        wrapped.frame_list = FrameList()
        include_keys=None
        include_variables=None
        exclude_keys=None,
        exclude_variables=None
        depth=4

        global Lock
        if Lock is None:
            Lock = 0

        def tracer(frame, event, arg):
            """
            Called by the sys.setprofile method on every event. The function
                checks to see if the event was a return, and if it is, save
                this frame.
            """
            global Depth
            if event == "call":
                Depth += 1
            if event == "return":
                if Depth > depth:
                    Depth -= 1
                    return
                lineno = frame.f_lineno
                name = frame.f_globals["__name__"]
                #logger.info("========================================")
                #logger.info(name)
                #logger.info("========================================")
                Depth -= 1
                wrapped.frame_list.add_frame(frame, arg=arg)
            return tracer

        def wrapped_f(*args,**kwargs):
            '''
            settings = self.__dict__.copy()
            depth = settings.pop('_depth', 0)

            def callback(context, name, ob):
                config = context.config.with_package(info.module)
                config.add_view(view=ob, **settings)

            info = self.venusian.attach(wrapped, callback, category='pyramid',
                                        depth=depth + 1)

            if info.scope == 'class':
                # if the decorator was attached to a method in a class, or
                # otherwise executed at class scope, we need to set an
                # 'attr' into the settings if one isn't already in there
                if settings.get('attr') is None:
                    settings['attr'] = wrapped.__name__

            settings['_info'] = info.codeinfo # fbo "action_method"
            import pdb;pdb.set_trace()
            '''
            global Depth
            Depth += 1

            global Lock
            if Lock == 1:
                try:
                    # THIS *SHOULD BE* THE RETURN FROM THE FUNCTION JUST CALLED
                    res = func(*args, **kwargs)
                except:
                    res = None

                return res
            else:
                Lock = 1;

            # Start the Profiler
            sys.settrace(tracer)

            try:
                args2 = (args[1],)
                response = wrapped(*args2, **kwargs)
                #response = wrapped(*args, **kwargs)
            finally:
                # Stop the Profiler
                sys.settrace(None)

            # Build a hierarchy of all the frames calling one another
            wrapped.frame_list.build_hierarchy()

            global Write_Called
            Write_Called += 1

            # Print output to Logger
            res = wrapped.frame_list.to_json_output( \
                depth=depth,
                include_keys=include_keys,
                include_variables=include_variables,
                exclude_keys=exclude_keys,
                exclude_variables=exclude_variables)

            try:
                output_to_logger(res)
            except:
                # Something went wrong with the logger
                a = 10

            # Reset Things
            wrapped.frame_list = FrameList()
            Depth = 0
            Lock = 0

            return response
            return wrapped(*args)
        return wrapped_f
