class Bar:  # parent class
    def msg(self):
        print("this is my 'bar' message")


class Foo(Bar):  # inherits from Bar
    def __init__(self):
        self.msg()


if __name__ == "__main__":
    foo = Foo()  # this is my 'bar' message
