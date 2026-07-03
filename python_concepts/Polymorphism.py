class Dog:
    def speak(self):
        print("Woof")

class Cat:
    def speak(self):
        print("Meow")

class Duck:
    def speak(self):
        print("Quack")

for animal in [Dog(),Cat(),Duck()]:
    animal.speak()