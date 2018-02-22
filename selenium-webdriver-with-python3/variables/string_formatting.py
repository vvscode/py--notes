city = "Minsk"
event = "show"

# "Welcome to <city> and enjoy the <event>"
print("1 Welcome to " + city + " and enjoy the " + event)
print("2 Welcome to {} and enjoy the {}".format(city, event))
print("3 Welcome to %s and enjoy the %s" % (city, event))
print("4 Welcome to {1} and enjoy the {0}".format(event, city))
print("5 Welcome to {a} and enjoy the {b}".format(a=city, b=event))
print("5 Welcome to %(a)s and enjoy the %(b)s" % {'a': city, 'b': event}) # old and ugly style %(b)s - s - string
