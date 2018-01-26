class Mixin1:
    def bar(self):
        print("this is my 'bar' message")


class Mixin2:
    def baz(self):
        print("this is my 'baz' message")


class Foo(Mixin2, Mixin1):
    pass  # allows us to instantiate an empty object from this class
    # you can use pass any where you have a block statement


if __name__ == "__main__":
    foo = Foo()
    foo.bar()  # this is my 'bar' message foo.baz() # this is my 'baz' message
