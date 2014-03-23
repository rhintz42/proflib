from pyramid.view import view_config
from proflib.lib.decorators import persistent_locals2
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame

def fo():
    c = 30
    return c

@persistent_locals2
def foo():
    a = 10
    e = bar()
    c = fo()
    g = bar()
    h = tt()
    return a

@persistent_locals2
def ba():
    d = 20
    return d

#@persistent_locals
def tt():
    z = 20
    f = fo()
    return z

#@persistent_locals
def bar():
    b = 20
    d = ba()
    k = ba()
    return b

@view_config(route_name='home', renderer='json')
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar()
    b = bar()
    return {'project': 'proflib'}
