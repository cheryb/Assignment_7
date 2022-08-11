import sqlite3
database = sqlite3.connect("assignment7.db")
cursor = database.cursor()
import time


############## STUDENT ################
# Add/remove course from semester schedule (based on course ID number).
######## Done by Nitin and Chirag ################
def add_remove_course_from_schedule():
    print("You have selected option 1. Add/remove course from semester schedule (based on course ID number).")
    choice2 = input("Do you want to add (1) or remove(2) this course from your schedule: ")
    while choice2 == 1 or 2:
       
        choice2 = int(choice2)
        if choice2 == 1:
            courseID = input("Type the ID that you want to add: ")
            courseID = int(courseID)
            cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % (courseID))
            response = cursor.fetchall()
            course_list = response[0][0].split(", ")
            course_list.append(courseID)
            course_list = (', ').join(course_list)
            cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list))

        elif choice2 == 2:
            courseID = input("Type the ID that you want to remove: ")
            courseID = int(courseID)
            cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % (courseID))
            response = cursor.fetchall()
            course_list = response[0][0].split(", ")
            course_list.remove(courseID)
            course_list = (', ').join(course_list)
            cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list))
 
######## Check for schedule conflict ###############
def check_conflict():
    cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % self.id)
    response = cursor.fetchall()
    crn_list = response[0][0].split(", ")
    schedule = []
    for crn in crn_list:
        cursor.execute("""SELECT TITLE, TIME, DAY FROM COURSE WHERE CRN='%s';""" % crn)
        course_info = cursor.fetchall()
        title, time, day = course_info[0]

    for prev_title, prev_time, prev_day in schedule:
        if prev_time == time and prev_day == day:
            print(f"Time conflict between {prev_title} and {title} on {day} at {time}")
            print("You cannot take both classes at the same time. \n")
            break

            schedule.append([title, time, day])
 
########### Print Schedule ###############
def print_schedule():
    cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % self.id)
    response = cursor.fetchall()
    crn_list = response[0][0].split(", ")
    schedule = []
    for crn in crn_list:
        cursor.execute("""SELECT TITLE, TIME, DAY FROM COURSE WHERE CRN='%s';""" % crn)
        course_info = cursor.fetchall()
        title, time, day = course_info[0]
        schedule.append([title, time, day])     
    for s in schedule:
        print(s)

 #################### Student #######################           


 ################# Instructor #######################
# Assemble and print course roster (instructor).
######## Done by Brianna ############
def print_course():
    print("You have selected option 2. Assemble and print course roster (instructor).")
    instructor = input("Enter the name of the instructor: \n")
    cursor.execute("""SELECT * FROM COURSE WHERE INSTRUCTOR = '%s';""" % (instructor)) 
    course_list = cursor.fetchall()
    for c in course_list:
        print(c)
 
 ######### Search and Print class roster ################
def printroster():
    cursor.execute("""SELECT CRN, TITLE FROM COURSE WHERE INSTRUCTOR='%s';""" % fullname)
    courses_prof = cursor.fetchall()
    cursor.execute("""SELECT NAME, SURNAME, `COURSE LIST` FROM STUDENT;""")
    students = cursor.fetchall()
    roster = []
    for c in courses_prof:
        curr_roster = []
        for student in students:
            student_name = student[0] + " " + student[1]
            if student[2] is None:
                continue
            course_list = student[2].split(", ")
            for course_student in course_list:
                if c[0] == int(course_student):
                    curr_roster.append(student_name) 
        for i in range(len(courses_prof)):
            print(courses_prof[i])
            print(roster[i])

################# Instructor #####################

############### Admin ###########################
# Add/remove courses from the system (admin).
 ##### DONE by Brianna #########

def add_remove_course_from_system():
    print("You have selected option 3. Add/remove courses from the system (admin).")
    choice = input("Select: Add Course (1) or Remove Course(2) ")
    choice = int(choice)
    if choice == 1:
        crn = input("CRN: ")
        title = input("TITLE: ")
        department = input("DEPARTMENT: ")
        time = input("TIME: ")
        day = input("DAY: ")
        semester = input("SEMESTER: ")
        year = input("YEAR: ")
        credits = input("CREDITS: ")
        cursor.execute("""INSERT INTO COURSE (CRN, TITLE, DEPARTMENT, TIME, DAY, SEMESTER, YEAR, CREDITS) VALUES (?,?,?,?,?,?,?,?)""" , (crn, title, department, time, day, semester, year, credits) )
    elif choice == 2:
        course = input("Enter CRN of course you want to delete: ")
        course = int(course)
        cursor.execute("""DELETE FROM COURSE WHERE CRN = '%d' ;""" % (course))
        print("The course has been deleted")

# Add/Remove student/teacher from system
######### Done by Brianna #############
def add_remove_student_teacher_from_schedule():
    print("You have selected option 3. Add/remove student/teacher from the system (admin).")
    choice = input("Select: Student (1) or Teacher (2) ")
    choice = int(choice)
    if choice == 1:
        student = input("Enter student's first name: ")
        student_last = input("Enter student's last name: ")
        print(student, student_last)
        choice2 = input("Do you want to add or remove this student: ")
        choice2 = int(choice2)
        if choice2 == 1:
            id = input("ID: ")
            gradyear = input("GRADYEAR: ")
            major = input("MAJOR: ")
            email = input("EMAIL: ")
            cursor.execute("""INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL ) VALUES (?,?,?,?,?, ?)""" , (id, student, student_last, gradyear, major, email) )
        elif choice2 == 2:
            cursor.execute("""DELETE FROM STUDENT WHERE NAME = '%s' ;""" % (student))
            print("The student has been deleted")
    elif choice == 2:
        teacher = input("Enter teacher's first name: ")
        teacher_last = input("Enter student's last name: ")
        print(teacher, teacher_last)
        choice2 = input("Do you want to add or remove this teacher: ")
        choice2 = int(choice2)
        if choice2 == 1:
            id = input("ID: ")
            title = input("TITLE: ")
            hireyear = input("HIREYEAR: ")
            dept = input("DEPARTMENT: ")
            email = input("EMAIL: ")
            cursor.execute("""INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR,DEPT, EMAIL ) VALUES (?,?,?,?,?, ?)""" , (id, teacher, teacher_last, hireyear, dept, email) )
        elif choice2 == 2:
            cursor.execute("""DELETE FROM INSTRUCTOR WHERE NAME = '%s' ;""" % (teacher))
            print("The instructor has been deleted")

###### Link/unlink student/teacher to course ############
######### Done by Nitin and Chirag ###########
def link_unlink_student_teacher_to_course():
    choice = input("Do you want to link/unlink a student or teacher: ")
    if choice == 1:
        choice2 = input("Do you want to link or unlink the student: ")
        choice2 = int(choice2)
        if choice2 == 1:
            studentID = input("Enter student's ID: ")
            studentID = int(studentID)
            cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % studentID)
            response = cursor.fetchall()
            course_list = response[0][0].split(", ")
            course_list.append(str(CRN))
            course_list = (', ').join(course_list)
        elif choice2 == 2:
            studentID = input("Enter student's ID: ")
            studentID = int(studentID)
            cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % studentID)
            response = cursor.fetchall()
            course_list = response[0][0].split(", ")
            course_list.remove(str(CRN))
            course_list = (', ').join(course_list)
            cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list, studentID))
    elif choice == 2:
        choice2 = input("Do you want to link or unlink the student: ")
        choice2 = int(choice2)
        if choice2 == 1:
            instructorname = input("Enter instructor name: ")
            CRN = input("Enter CRN: ")
            cursor.execute("""UPDATE COURSE SET INSTRUCTOR='%s' WHERE CRN='%d';""" % (instructorName, CRN))
        elif choice2 == 2:
            instructorname = input("Enter instructor name: ")
            CRN = input("Enter CRN: ")
            cursor.execute("""UPDATE COURSE SET INSTRUCTOR='%s' WHERE INSTRUCTOR='%s' AND CRN='%d';""" % ('---', instructorName, CRN))


################ Admin ################


############## All users ###################
# Search all courses (all users) 
########### Done by Nitin and Chirag ############
def search_all_courses():
    print("You have selected option 5. Search all courses (all users).")

    cursor.execute("""SELECT title FROM COURSE""")
    course_list = cursor.fetchall()
    for c in course_list:
        print(c)

# Search courses based on parameters (all users). ######## DONE #########
######### Done by Nitin and Chirag ##############
def search_specific_courses():
    print("You have selected option 6. Search courses based on parameters (all users).")

    parameters = ['CRN', 'TITLE', 'DEPARTMENT', 'TIME', 'DAY', 'SEMESTER']
    inputs = [''] * 6
    for i in range(6):
        parameter = parameters[i]
        inputs[i] = input(f'Enter a {parameter}: ')

    crn, title, department, time, day, semester = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5]
    cursor.execute("""SELECT * FROM COURSE WHERE CRN = '%s' OR TITLE = '%s' OR DEPARTMENT = '%s' OR TIME = '%s' OR DAY = '%s' OR SEMESTER = '%s';""" % (crn, title, department, time, day, semester)) 

    course_list = cursor.fetchall()
    for c in course_list:
        print(c)



# Log-in, log-out (all users).
######## Done by Brianna ###############
def log_in_log_out():
    choice = input("Are you a student (1), instructor(2) or admin(3)? ")
    choice = int(choice) 
    name = input("Enter email: ")
    if choice == 1:
        cursor.execute("""SELECT email FROM STUDENT WHERE email=?""", [name])
        for row in iter(cursor.fetchone, None):
            print(row)
            print("You are now logged in")
        user_input = input("Please select an option \n 1. Add/remove course from semester schedule (based on course ID number). \n 2. Search all courses (all users). \n 3. Search courses based on parameters (all users): \n")
        user_input = int(user_input)
        if user_input == 1:
            add_remove_course_from_schedule() ####### Good Enough #######
        elif user_input == 2:
            search_all_courses() ## Works 
        elif user_input == 3: ## Works
            search_specific_courses() 
        elif user_input == 4:
            check_conflict()
        elif user_input == 5:
            print_schedule()


    elif choice == 2:
        cursor.execute("""SELECT email FROM INSTRUCTOR WHERE email=?""", [name])
        for row in iter(cursor.fetchone, None):
            print(row)
            print("You are now logged in")
            user_input = input("Please select an option \n 1. Assemble and print course roster (instructor). \n 2. Search courses based on parameters (all users): \n 3. Search/Print teaching schedule \n")
            user_input = int(user_input)
            if user_input == 1:
                print_roster() 
            elif user_input == 2:
                search_specific_courses() 
            elif user_input == 3:
                print_course()
                
    elif choice == 3:
        cursor.execute("""SELECT email FROM ADMIN WHERE email=?""", [name])
        for row in iter(cursor.fetchone, None):
            print(row)
            print("You are now logged in")
            user_input = input("Please select an option \n 1. Add/remove courses from the system (admin). \n 2. Search all courses (all users). \n 3. Search courses based on parameters (all users): \n 4. Add/remove instructors/students from system \n")
            user_input = int(user_input)
            if user_input == 1:
                add_remove_course_from_system() ## Works
            elif user_input == 2:
                search_all_courses() 
            elif user_input == 3:
                search_specific_courses() 
            elif user_input == 4:
                add_remove_student_teacher_from_schedule()
            elif user_input == 5:
                link_unlink_student_teacher_to_course()



log_in = input("WELCOME to CURSE, please log-in: ")
log_in = int(log_in)
if log_in == 1:
    log_in_log_out()

logout = input("Do you want to continue or logout: ")
logout = int(logout)
if logout == 1:
        log_in_log_out()
elif logout == 2:
    print("You are now logged out")
    exit()
 

database.commit()
database.close()
