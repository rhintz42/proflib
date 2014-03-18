from pyramid.view import view_config
from proflib.lib.decorators import twrapper


@view_config(route_name='home', renderer='json')
@twrapper
def my_view(request):
    print("!Nice!")
    return {'project': 'proflib'}
