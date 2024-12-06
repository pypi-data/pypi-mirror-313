import random

utter_ughs = ["Ugh","Argh","Sigh","Pfft","Tsk","Doh","Gah","Bah","Meh","Eugh","Hmph","Oof","Yeesh","Cripes","Blah","Darn","Rats","Sheesh","Oops","Yikes","Phooey","Groan","Whoops","Dang","Aw, man","Blast","Drat","Hoo boy","For crying out loud","Oh, come on!"]

def get_random(array):
    return array[random.randint(0, len(array) - 1)]

def ughs():
    """
    Ughs
    
    Spit out a random utter ugh for you.
    
    Parameters
    ----------

    Returns
    -------
    str
        Return a string of ugh.
    
    Examples
    --------
    >>> print(ugh()).
    """
    return get_random(utter_ughs)