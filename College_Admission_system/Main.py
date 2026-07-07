#purpose :To Build a simple College_admission_&_marks_ Management System using Python and MySQL
#input:Name,Roll_no,Class,Marks
#output:To store and retrieve college admission and marks data
#Author:'dheerajkumarsahu827@gmail.com'
import random
import csv
from datetime import datetime
now = datetime.now()
import mysql.connector as c
from pathlib import Path
connection=c.connect(host="localhost",user="root",password="dheeraj@19",database="college_admission")

def view_registered_students():
    try:
        connection=c.connect(host="localhost",user="root",password="dheeraj@19",database="college_admission")
        cursor=connection.cursor()
        query="SELECT * FROM STUDENTS"
        cursor.execute(query)
        results=cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def new_admission_registration():
    try:
        available_courses()
        Course=input("Enter Course Name:")
        Name=input("Enter Student Name:")
        City=input("Enter City Name:")
        Gender=input("Enter Gender(M/F):")
        Mobile_no=input("Enter Mobile Number:")
        Email=input("Enter Email:")
        Marks_10=input("Enter Class 10th Marks:")
        streams()
        if streams()=="Mathamatics":
            Marks_12_Maths=float(input("Enter Class 12th Maths Marks:"))
            Marks_12_Physics=float(input("Enter Class 12th Physics Marks:"))
            Marks_12_Chemistry=float(input("Enter Class 12th Chemistry Marks:"))
            if Marks_12_Maths>=50 and Marks_12_Physics>=50 and Marks_12_Chemistry>=50:
                print("Eligible for Admission ")
            else:
                print("Not Eligible for Admission as the minimum Crieteria is not met. Please check the marks and try again.")
                menu()
        elif streams()=="Biology":
            Marks_12_Biology=float(input("Enter Class 12th Biology Marks:"))
            Marks_12_Physics=float(input("Enter Class 12th Physics Marks:"))
            Marks_12_Chemistry=float(input("Enter Class 12th Chemistry Marks:"))
            if Marks_12_Biology>=50 and Marks_12_Physics>=50 and Marks_12_Chemistry>=50:
                print("Eligible for Admission ")
            else:
                print("Not Eligible for Admission as the minimum Crieteria is not met. Please check the marks and try again.")
                menu()
        elif streams()=="Commerce":
            Marks_12_Accounts=float(input("Enter Class 12th Accounts Marks:"))
            Marks_12_Economics=float(input("Enter Class 12th Economics Marks:"))
            Marks_12_Business_Studies=float(input("Enter Class 12th Business Studies Marks:"))
            if Marks_12_Accounts>=50 and Marks_12_Economics>=50 and Marks_12_Business_Studies>=50:
                print("Eligible for Admission ")
            else:
                print("Not Eligible for Admission as the minimum Crieteria is not met. Please check the marks and try again.")
                menu()
        elif streams()=="Arts/Humanities":
            Marks_12_History=float(input("Enter Class 12th History Marks:"))
            Marks_12_Political_Science=float(input("Enter Class 12th Political Science Marks:"))
            Marks_12_Psychology=float(input("Enter Class 12th Psychology Marks:"))
            if Marks_12_History>=50 and Marks_12_Political_Science>=50 and Marks_12_Psychology>=50:
                print("Eligible for Admission ")
            else:
                print("Not Eligible for Admission as the minimum Crieteria is not met. Please check the marks and try again.")
                menu()
        file_path = Path("Registrations.csv")
        with open(file_path,mode="a",newline="") as file:
            headers=["Course","Name","City","Gender","Mobile_no","Email","Marks_10"]
            data=[Course.upper(),Name.capitalize(),City.capitalize(),Gender.upper(),Mobile_no,Email,Marks_10]
            writer = csv.writer(file)     
            writer.writerow(headers)
            writer.writerow(data)
    except Exception as e:
        print(f"Error occurred: {e}")

def available_courses():
    print("B.TECH")
    print("M.TECH")
    print(" BCA ")
    print(" MCA ")
    print(" BBA ")
    print(" MBA ")
    print(" B.COM")
    print(" M.COM")
    
def streams():
    print("Class 12th Streams\n:")
    print("Mathamatics:-1 ")
    print("Biology:-2")
    print("Commerce:-3")
    print("Arts/Humanities:-4")
    choice=int(input("Enter your choice:"))
    if choice==1:
        return "Mathamatics"
    elif choice==2:
        return "Biology"
    elif choice==3:
        return "Commerce"
    elif choice==4:
        return "Arts/Humanities"
    else:
        print("Invalid choice! Please try again.")

def check_admission_approval_status():
    Name=input("Enter Name:- ")    
    Course=input("Enter Course Name:- ")

def view_marks():
    pass

def view_notice():
    pass

def registered_feedback():
    pass

def menu():
    while True:
        print("Press '1' to View Registered Students")
        print("Press '2' for New Admission Registration")
        print("Press '3' to Check Admission Approval Status")
        print("Press '4' to view marks")
        print("Press '5' to View Notice")
        print("Press '6' to Registered Feedback")
        print("Press '7' to Exit")

        choice=int(input("Enter your choice:"))
        if choice==1:
            view_registered_students()
        elif choice==2:
            new_admission_registration()
        elif choice==3:
            check_admission_approval_status()
        elif choice==4:
            view_marks()
        elif choice==5:
            view_notice()
        elif choice==6:
            registered_feedback()
        elif choice==7:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please try again.")

menu()