# Basic formatting
print(
    "My name is {} and I'm from {}".format("Mark", "England")
)

# Positional access to arguments
print(
    "{2}, {0}, {1}".format("foo", "bar", "baz")
)

# Splatting arguments
args = ["foo", "bar", "baz"]
print(
    "{}, {}, {}".format(*args)
)

# Repeatable indexes
print(
    "{0}, {1}, {0}, {2}".format("foo", "bar", "baz")
)

# Named arguments
print(
    "{foo}, {bar}, {baz}".format(foo="FOO", bar="BAR", baz="BAZ")
)

# Keyword arguments
args = {"foo": "FOO", "bar": "BAR", "baz": "BAZ"}
print(
    "{foo}, {bar}, {baz}".format(**args)
)

# Complex object access
args = ("foo", "bar", "baz")
print(
    "{0[0]}, {0[1]}, {0[2]}".format(args)
)

# Alignment and Padding
print("{:†<10}".format("foo"))
print("{:†>10}".format("foo"))
print("{:†^10}".format("foo"))

# Separators
print("{:,}".format(1234567890))

# Percentages
print("{:.0%}".format(1))
