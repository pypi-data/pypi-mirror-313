'''
The Soundlib module is developed and maintained by the 401.

All rights to the code and its functionalities are reserved.

Unauthorized distribution of this module is strictly prohibited.

'''

from _soundlib import *
from _soundlib import __doc__

__all__ = dir(__import__('_soundlib'))
