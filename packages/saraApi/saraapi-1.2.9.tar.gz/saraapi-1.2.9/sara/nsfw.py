
from .reqNh import get_random_doujin, get_cover_image_url, get_doujin_info
from .req import get

__version__ = '1.1.8'
class LimitExceeded(Exception):
    pass


def ass():
    return get('ass')

def boobs():
    return get('boobs')

def blowjob():
    return get('blowjob')

def ahegao():
    return get('ahegao')

def bdsm():
    return get('bdsm')

def cum():
    return get('cum')

def hentai():
    return get('hentai')

def femdom():
    return get('femdom')

def doujin():
    doujin_id = get_random_doujin()

    if doujin_id:
        doujin_info = get_doujin_info(doujin_id)
    if doujin_info:
        cover_url = get_cover_image_url(doujin_info)
        return cover_url

    return None

def maid():
    return get('maid')

def orgy():
    return get('orgy')

def panties():
    return get('panties')

def netorare():
    return get('netorare')

def gifs():
    return get('gifs')

def feet():
    return get('feet')

def pussy():
    return get('pussy')

def uglyBastard():
    return get('uglyBastard')

def uniform():
    return get('uniform')

def foxgirl():
    return get('foxgirl')

def cumslut():
    return get('cumslut')

def glasses():
    return get('glasses')

def thighs():
    return get('thighs')

def tentacles():
    return get('tentacles')

def masturbation():
    return get('masturbation')

def school():
    return get('school')

def yuri():
    return get('yuri')

def succubus():
    return get("succubus")
