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
