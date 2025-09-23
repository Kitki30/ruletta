import modules.cache as cache
import modules.popup as popup 

def check():
    # Check extra fucttions
    if not cache.get("rand_extra_func"):
        popup.show("Your micropython port doesn't support MICROPY_PY_RANDOM_EXTRA_FUNCS!")
        return False
    
    # Check version
    ver = [cache.get("ver_major"), cache.get("ver_minor"), cache.get("ver_patch")]
    ver_req = [2, 2, 0]
    if ver < ver_req:
        popup.show("Ruletta requires Stick firmware version 2.2.0 or higher!")
        return False
    
    return True