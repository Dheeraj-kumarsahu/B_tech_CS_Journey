def total(*args):
    print(f"SUM OF ALL THE VALUES IS : - {sum(args)}")

total(1,2,3,4,5,6,7,8,9,10)

def profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}:{value}")
profile(name="akarsh",age=22)