from pyramid.view import view_config
from proflib.lib.decorators import persistent_locals
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame

def fo():
    c = 30
    return c

@persistent_locals
def foo():
    a = 10
    e = bar(True)
    c = fo()
    g = bar(False)
    h = tt()
    return a

@persistent_locals
def ba(var):
    d = var
    return d

#@persistent_locals
def tt():
    z = 20
    f = fo()
    return z

#@persistent_locals
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
