from .req import get

__version__ = '1.1.8'
class LimitExceeded(Exception):
    pass

def baka():
    return get('baka')
def kiss():
    return get('kiss')
def kill():
    return get('kill')
def spank():
    return get('sfwspank')
def punch():
    return get('punch')
def poke():
    return get('poke')