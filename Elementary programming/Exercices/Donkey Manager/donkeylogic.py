"""
Defines the donkeygotchi's internal logic
"""
import donkeydefs as defs

def init():
    """
    Initializes donkey data by creating a new dictionary with initial values for
    all keys, and returns it.
    """
    donkeydata = {
        "SATIATION": defs.INITIAL,
        "HAPPINESS": defs.INITIAL,
        "ENERGY": defs.INITIAL,
        "AGE": 0,
        "MONEY": 0,
        "RETIRED": False,
    }
    return donkeydata

def _age(donkeydata):
    """
    Ages the donkey and - if needed - puts it in retirement. Meant only for 
    internal use in this module.
    """
    donkeydata["AGE"] += 1
    
    if donkeydata["AGE"] == defs.RETIREMENT_AGE:
        donkeydata["RETIRED"] = True

def _update_states(donkeydata):
    """
    Changes the donkey's state as time passes, and puts the donkey in retirement
    if needed. Meant only for internal use in this module.
    """
    if donkeydata["AGE"] % 2 == 0:
        if donkeydata["SATIATION"] > 6 and donkeydata["ENERGY"] < defs.MAX_STATE:
            donkeydata["ENERGY"] += 1
        donkeydata["SATIATION"] -= 1
    if donkeydata["AGE"] % 3 == 0:
        donkeydata["HAPPINESS"] -= 1
    
    if donkeydata["SATIATION"] <= 0 or donkeydata["HAPPINESS"] <= 0 or donkeydata["ENERGY"] <= 0:
        donkeydata["RETIRED"] = True

def feed(donkeydata):
    """
    Feeds the donkey, i.e. raises its satiation, if it isn't at the maximum yet.
    """
    _age(donkeydata)
    _update_states(donkeydata)
    if donkeydata["SATIATION"] < defs.MAX_STATE:
        donkeydata["SATIATION"] += 1
    
def tickle(donkeydata):
    """
    Tickles the donkey, i.e. raises its happiness, it it isn't at the maximum yet.
    """
    _age(donkeydata)
    _update_states(donkeydata)
    if donkeydata["HAPPINESS"] < defs.MAX_STATE:
        donkeydata["HAPPINESS"] += 1

def work(donkeydata):
    """
    Makes the donkey work by spending its energy in return for money.
    """
    _age(donkeydata)
    donkeydata["ENERGY"] -= 1
    donkeydata["MONEY"] += 1
    _update_states(donkeydata)