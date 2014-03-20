from proflib.lib.decorators import persistent_locals
import sys
import os

@persistent_locals
def cool():
    rollup = {
        'data': [
            1,
            2,
        ],
        'status': 200
    }

    return rollup
