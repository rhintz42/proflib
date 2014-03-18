#import logging
from functools import wraps

#logger = logging.getLogger(__name__)



def twrapper(func):
    """ 
    This decorator will check if my wrapper works.

    """
    @wraps(func)
    def wrapped(request):
        try:
            print("Hey")
            response = func(request)
            print("There")
        finally:

            # this *must* happen after the view is called
            # once we've cleaned up the filters and everything, we want to call
            # highfiver so it'll clear the SOSS cache
            print("cool")

        return response

    return wrapped
