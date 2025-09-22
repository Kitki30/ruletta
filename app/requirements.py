import modules.cache as cache 

def check():
    if not cache.get("rand_extra_func"):
        return False
    return True