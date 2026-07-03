#Purpose:-To create a school management system using JSON in Python
#Author:-Dheeraj Kumar Sahu
#Contact:-dheerajkumarsahu827@gmail.com
import json
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime as now
try:
    Database="C:\\Users\\User\\OneDrive\\Desktop\\Programming\\B_tech_CS_journey\\_management_project\\School_data.json"
    data={"Students" : [] ,"Teachers" : []}
    if Path(Database).exists():
        with open(Database,"r") as file:
            content= file.read()
            if content:
                data=json.loads(content)

    def save():
        with open(Database,"w") as file:
            json.dump(data,file,indent=4)

    class Persons(ABC):

        @abstractmethod
        def get_roles(self):
            pass

        @abstractmethod
        def register(self):
            pass

        @abstractmethod
        def show_details(self):
            pass

        @staticmethod
        def validate_email(email):
            if "@" in email and "." in email:
                return True
            else:
                return False

    class Students(Persons):
        def get_roles(self):
            return "Student"
        
        def register(self):
            name=input("Enter Student Name  :-")
            age=int(input("Enter Student Age:-"))
            email=input("Enter Student Email:-")
            roll_no=int(input("Enter Roll.no:-"))
            if not Persons.validate_email(email):
                print("Invalid Email")
                return
            for i in data['Students']:
                if  i['roll_no']==roll_no:
                    print("Roll.no already exists")
                    return

            data['Students'].append({"name":name,"age":age,"email":email,"roll_no":roll_no,"grades":{}})
            save()
            print(f"Student Named :-  {name} Data Saved")

        def Add_grades(self):
            roll_no=int(input("Enter Roll.no:-"))
            subject=input("Enter Subject:- ")
            marks=float(input("Enter marks :- "))
            for i in data['Students']:
                if i['roll_no']==roll_no:
                    i['grades'][subject]=marks
                    save()
                    print(f"Grades added for Student with Roll.no:- {roll_no}")
                    return
            print("Student not found")
        
        def show_details(self):
            roll_no=int(input("Enter Roll Number:-  "))
            for s in data["Students"]:
                if s["roll_no"]==roll_no:
                    print(f"Name:- {s['name']}")
                    print(f"Age:- {s['age']}")
                    print(f"Email:- {s['email']}")
                    print(f"Roll.no:- {s['roll_no']}")
                    print(f"Grades:- {s.get('grades',{})}")
                    return

    class Teachers(Persons):
        def get_roles(self):
            return "Teacher"
        
        def register(self):
            name=input("Enter Teacher Name  :-")
            age=int(input("Enter Teacher Age:-"))
            email=input("Enter Teacher Email:-")
            subject=input("Enter Subject:-")
            emp_id=input("Enter Employee ID:-")
            if not Persons.validate_email(email):
                print("Invalid Email")
                return
            for i in data['Teachers']:
                if  i['email']==email:
                    print("Email already exists")
                    return

            data['Teachers'].append({"name":name,"age":age,"email":email,"subject":subject,"emp_id":emp_id})
            save()
            print(f"Teacher Named :-  {name} Data Saved")
        
        def show_details(self):
            emp_id=input("Enter Emp_id:-  ")
            for s in data["Teachers"]:
                if s["emp_id"]==emp_id:
                    print(f"Name:- {s['name']}")
                    print(f"Age:- {s['age']}")
                    print(f"Email:- {s['email']}")
                    print(f"Subject:- {s['subject']}")
                    print(f"Employee ID:- {s['emp_id']}")
                    return

    #ASSIGNING OBJECTS TO CLASSES
    Stu=Students()
    Tea=Teachers()
    print("Press 1 to register a Student")
    print("Press 2 to resister a Teacher")
    print("Press 3 to add Grades")
    print("Press 4 to show a Student Deatils")
    print("Press 5 to show a Teacher Details")

    choice = int(input("Enter your choice:-"))

    if choice==1:
        Stu.register()
    elif choice ==2:
        Tea.register()
    elif choice ==3:
        Stu.Add_grades()
    elif choice ==4:
        Stu.show_details()
    elif choice ==5:
        Tea.show_details()
except Exception as E:
    print(E)