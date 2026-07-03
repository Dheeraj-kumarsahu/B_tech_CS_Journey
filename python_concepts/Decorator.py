def timer(func):
    def wrapper():
        print("Starting")
        func()
        print("Done")
    return wrapper

@timer
def greet():
    print("Hello World")

greet()