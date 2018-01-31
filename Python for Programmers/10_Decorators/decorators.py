import time


def upit(func):
    def helper(msg):
        response = func(msg)
        modified_response = response.upper()
        print("""
        upit decorates
        value: {}
        into: {}
        for message: {}""".format(response, modified_response, msg))
        return modified_response

    return helper


def hyphenit(func):
    def helper(msg):
        response = func(msg)
        modified_response = response.replace(" ", "-")
        print("""
        hyphenit decorates
        value: {}
        into: {}
        for message: {}""".format(response, modified_response, msg))
        return modified_response

    return helper


@upit
@hyphenit
def message(msg):
    return "%s (%s)" % (msg, str(time.time()))


print(message("hello world"))


def memoize(func):
    cache = {}

    def helper(key, client, ttl=30):
        if key not in cache:
            set_key(func, key, client)
        else:
            if check_expiration(cache, key, ttl):
                set_key(func, key, client)

        return cache[key]["value"]

    def set_key(func, key, client):
        cache[key] = {"timestamp": time.time(), "value": func(key, client)}

    def check_expiration(cache, key, ttl):
        elapsed = time.time() - cache[key]["timestamp"]
        if elapsed > ttl:
            del cache[key]
            return True

    return helper
