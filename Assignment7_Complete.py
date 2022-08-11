import sqlite3
database = sqlite3.connect("assignment5.db")
cursor = database.cursor()

####### Add a column under courses names PROFESSOR
####### Insert professor names into column


# 1 • Add/remove course from semester schedule (based on course ID number).

def add_remove_course_from_schedule():
    print("You have selected option 1. Add/remove course from semester schedule (based on course ID number).")
    choice2 = input("Do you want to add (1) or remove(2) this course from your schedule: ")
    while choice2 == 1 or 2:
       
        choice2 = int(choice2)
        if choice2 == 1:

            course = input("Enter course ID number: ")
            course = int(course)
            cursor.execute("""SELECT crn FROM COURSE WHERE crn=?""", [course])
            for row in iter(cursor.fetchone, None):
                print(row)
                
        elif choice2 == 2:
            course = input("Enter course ID number: ")
            course = int(course)
            cursor.execute("""SELECT crn FROM COURSE WHERE crn=?""", [course])
            for row in iter(cursor.fetchone, None):
                print(row)
                

# 2 • Assemble and print course roster (instructor).
def print_course():
    print("You have selected option 2. Assemble and print course roster (instructor).")
    instructor = input("Enter the name of the instructor: \n")
    cursor.execute("""SELECT * FROM COURSE WHERE PROFESSOR = '%s';""" % (instructor)) 
    course_list = cursor.fetchall()
    for c in course_list:
        print(c)

# 3 • Add/remove courses from the system (admin). ##### DONE #########

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
        #sql = """DELETE FROM COURSE WHERE CRN = '%s' """ 
        cursor.execute("""DELETE FROM COURSE WHERE CRN = '%d' ;""" % (course))
        print("The course has been deleted")

# Add/Remove student/teacher from system
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






# 5 • Search all courses (all users) . ###### DONE #########

def search_all_courses():
    print("You have selected option 5. Search all courses (all users).")

    cursor.execute("""SELECT title FROM COURSE""")
    course_list = cursor.fetchall()
    for c in course_list:
        print(c)

# 6 • Search courses based on parameters (all users). ######## DONE #########

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


# 4 • Log-in, log-out (all users).
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

    elif choice == 2:
        cursor.execute("""SELECT email FROM INSTRUCTOR WHERE email=?""", [name])
        for row in iter(cursor.fetchone, None):
            print(row)
            print("You are now logged in")
            user_input = input("Please select an option \n 1. Assemble and print course roster (instructor). \n 2. Search courses based on parameters (all users): \n 3. Search/Print teaching schedule \n")
            user_input = int(user_input)
            if user_input == 1:
                print_course()  ########## Good Enough ########
            elif user_input == 2:
                search_specific_courses() ### Works
            elif user_input == 3: ## Works
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
                search_all_courses() ### Works
            elif user_input == 3:
                search_specific_courses() ## Works
            elif user_input == 4:
                add_remove_student_teacher_from_schedule() ## Works

      
 
log_in = input("WELCOME, please log-in: ")
log_in = int(log_in)
if log_in == 1:
    log_in_log_out()

database.commit()
database.close()

