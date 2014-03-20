from pyramid.view import view_config
from proflib.lib.decorators import persistent_locals
from proflib.models.tmodel import cool

def fo():
    c = 30
    return c

#@persistent_locals
def foo():
    a = 10
    e = bar()
    c = fo()
    return a

#@persistent_locals
def ba():
    d = 20
    return d

#@persistent_locals
def bar():
    b = 20
    d = ba()
    return b

@view_config(route_name='home', renderer='json')
@persistent_locals
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar()
    b = bar()
    c = cool()
    return {'project': 'proflib'}
