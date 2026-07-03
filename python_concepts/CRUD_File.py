#CRUD Operations in Python
from pathlib import Path
print("Welcome to the CRUD Operations Program")

def Create():
    try:
        X=input("Enter the name of the file to be created:")
        path = Path(X)
        if path.exists():
            print("File already exists")
        else:
            File=open(X,'w')
            print("File Created Successfully")
            File.close()
    except Exception as e:
        print(f'Error occurred while creating file:{e}')

def Read():
    try:
        X=input("Enter the name of the file to be read:")
        path = Path(X)
        if not path.exists():
            print("File does not exist")
            return
        else:
            File=open(X,'r')
            content=File.read()
            print(content)
            File.close()
    except Exception as e:
        print(f'Error occurred while reading file:{e}')

def Update():
    try:
        X=input("Enter the name of the file to be updated:")
        path = Path(X)
        if not path.exists():
            print("File does not exist")
            return
        else:
            def append():
                File=open(X,'a')
                content=input("Enter the content to be added:")
                File.write(content)
                File.close()
                print("Content Updated Successfully")
            
            def overwrite():
                File=open(X,'w')
                content=input("Enter the content to be Overwrite:")
                File.write(content)
                File.close()
                print("Content Updated Successfully")
            
            def rename ():
                import os
                Y=input("Enter the current name of the file:")
                X=input("Enter the new name for the file:")
                os.rename(Y,X)
                print("File Renamed Successfully")


        def menu():
            while True:
                print("Please select an operation:")
                print("1. Append")
                print("2. Overwrite")
                print("3. Rename")
                print('4. EXIT')
                choice = input("Enter your choice (1-4): ")
                if choice == "1":
                    append()
                elif choice == "2":
                    overwrite()
                elif choice == "3":
                    rename()
                elif choice == "4":
                    print("EXITING ....")
                    break
                else:
                    print("Invalid Choice")
        menu()
    except Exception as e:
        print(f'Error occurred while updating file:{e}')

def Delete():
    try:
        password=input("Enter the password to delete the file:")
        if password == "!@#$%":
            import os
            X=input("Enter the name of the file to be deleted:")
            if not Path(X).exists():
                print("File does not exist")
                return
            os.remove(X)
            print("File Deleted Successfully")
        else:
            print("INCORRECT PASSWORD FILE IS NOT DELETED")
    except Exception as e:
        print(f'Error occurred while deleting file:{e}')

def Menu(): 
    while True:  
        print("Please select an operation:")
        print("1. Create")
        print("2. Read")
        print("3. Update")
        print("4. Delete")
        print("5. EXIT ")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            Create()
        elif choice == "2":
            Read()
        elif choice == "3":
            Update()
        elif choice == "4":
            Delete()
        elif choice == "5":
            print("EXITING ....")
            break
        else:
            print("Invalid Choice")
Menu()