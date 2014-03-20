from pyramid.view import view_config
from proflib.lib.decorators import persistent_locals
from proflib.models.tmodel import cool


@persistent_locals
def foo():
    a = 10
    return a

@persistent_locals
def bar():
    b = 20
    return b

@view_config(route_name='home', renderer='json')
@persistent_locals
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar()
    c = cool()
    return {'project': 'proflib'}
