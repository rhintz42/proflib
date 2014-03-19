from pyramid.view import view_config
from proflib.lib.decorators import persistent_locals


def foo():
    return 10

def bar():
    return 20

@view_config(route_name='home', renderer='json')
@persistent_locals
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar()
    return {'project': 'proflib'}
