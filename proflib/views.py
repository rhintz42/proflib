from pyramid.view import view_config
from proflib.lib.decorators import prof
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
#from .views2 import hello
from proflib.views2 import hello


def fo():
    """ fo here """
    c = 30
    return c


#@prof(1)
def ba(var):
    d = var
    return d


#@prof()
def tt():
    z = 20
    f = fo()
    return z


#@test()
#@prof()
def bar(tr):
    b = 20
    if tr:
        d = ba(3)
        k = ba('j')
    else:
        d = ba(4)
        k = ba('z')
        
    return b


@view_config(route_name='home', renderer='json')
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar(True)
    b = bar(False)
    return {'project': 'proflib'}


@prof(3, include_keys=['local_variables', 'function_name','return_value', 'children', 'code'],
        exclude_keys=['local_variables', 'function_name','return_value', 'children', 'code'],
        include_variables=['x'], exclude_variables=["x"])
def foo():
    """ foo here (A bit bigger than the others) """
    a = 10
    e = bar(True)
    c = fo()
    g = bar(False)
    h = tt()
    x = longer_docstring()
    return a

#@otherprof
#@prof(2)
def longer_docstring():
    """
    This is the docstring for the function longer_docstring
    It is called by foo
    '''Pretty cool'''
    """
    x = 84
    return x

def add_headers(self, request, **kwargs):
    """Add any headers needed by the connection. As of v2.0 this does
    nothing by default, but is left for overriding by users that subclass
    the :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

    This should not be called from user code, and is only exposed for use
    when subclassing the
    :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

    :param request: The :class:`PreparedRequest <PreparedRequest>` to add headers to.
    :param kwargs: The keyword arguments from the call to send().
    """
    pass

def get(self, block=True, timeout=None):
    """Return the stored value or raise the exception.

    If this instance already holds a value / an exception, return / raise it immediatelly.
    Otherwise, block until another greenlet calls :meth:`set` or :meth:`set_exception` or
    until the optional timeout occurs.

    When the *timeout* argument is present and not ``None``, it should be a
    floating point number specifying a timeout for the operation in seconds
    (or fractions thereof).
    """
    if self._exception is not _NONE:
        if self._exception is None:
            return self.value
        raise self._exception
    elif block:
        switch = getcurrent().switch
        self.rawlink(switch)
        try:
            timer = Timeout.start_new(timeout)
            try:
                result = self.hub.switch()
                assert result is self, 'Invalid switch into AsyncResult.get(): %r' % (result, )
            finally:
                timer.cancel()
        except:
            self.unlink(switch)
            raise
        if self._exception is None:
            return self.value
        raise self._exception
    else:
        raise Timeout
