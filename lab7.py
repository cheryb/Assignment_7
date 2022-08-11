import sqlite3
import time
database = sqlite3.connect("assignment7.db")
cursor = database.cursor()

class User:
    def __init__(self,fname=None,lname=None,id=None, user_type=None):
        self.firstname = fname
        self.lastname = lname
        self.id = id
        self.user_type = user_type
        self.logged_in = False

    def view(self):
        print(self.firstname,self.lastname,self.id,self.user_type)

    def add_user_info(self):
        self.firstname = input("Enter user's first name: ") 
        self.lastname = input("Enter user's last name: ") 
        self.id = input("Enter user's id: ") 
        self.user_type = input("Enter user type (student, instructor, or admin): ") 
    
    # Login
    def login(self, email):
        cursor.execute("""SELECT * FROM '%s' WHERE EMAIL='%s';""" % (self.user_type, email))
        response = cursor.fetchall()
        if response == []:
            print("User with this email does not exist")
        else:
            self.logged_in = True
            print("You have logged in")
    
    # Logout
    def logout(self):
        if self.logged_in is True:
            self.logged_in = False
            print("You have logged out")
        else:
            print("You have not logged in")

    # Search for courses (all or based on some parameter)
    def searchCourses(self, crn, title, department, time, day, semester, year, credits, instructor):
        cursor.execute("""SELECT * FROM COURSE WHERE CRN = '%d' OR TITLE = '%s' OR DEPARTMENT = '%s' OR TIME = '%d' OR DAY = '%s' OR SEMESTER = '%s' OR YEAR = '%d' OR CREDITS = '%d' OR INSTRUCTOR = '%s';""" % (crn, title, department, time, day, semester, year, credits, instructor)) 

        course_list = cursor.fetchall()
        for c in course_list:
            print(c)

class Student(User):
     
    def __init__(self,fname,lname,id):
        self.firstname = fname
        self.lastname = fname
        self.id = id
  
    # Add/remove course from semester schedule (based on course ID number)
    def addCourse(self, courseID):
        cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % self.id)
        response = cursor.fetchall()
        course_list = response[0][0].split(", ")
        course_list.append(courseID)
        course_list = (', ').join(course_list)

        cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list, self.id))

    def removeCourse(self, courseID):
        cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % self.id)
        response = cursor.fetchall()
        course_list = response[0][0].split(", ")
        course_list.remove(courseID)
        course_list = (', ').join(course_list)

        cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list, self.id))

    # Check conflicts in course schedule
    def checkConflicts(self):
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
        

    # Print individual schedule
    def printSchedule(self):
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
          
class Instructor(User):
        
    def __init__(self,fname,lname,id):
        self.firstname = fname
        self.lastname = lname
        self.id = id
          
    # Print course teaching schedule
    def printSchedule(self):
        fullname = self.firstname + " " + self.lastname
        cursor.execute("""SELECT TITLE, TIME, DAY FROM COURSE WHERE INSTRUCTOR='%s';""" % fullname)
        schedule = cursor.fetchall()
        for s in schedule:
            print(s)

    # Print/search course roster(s)
    def printRoster(self):
        fullname = self.firstname + " " + self.lastname
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
            roster.append(curr_roster)
        
        
        for i in range(len(courses_prof)):
            print(courses_prof[i])
            print(roster[i])


     
class Admin(User):
    
    def __init__(self,fname,lname,id):
        self.firstname = fname
        self.lastname = lname
        self.id = id
          
    # Add courses to the system
    def addCourse(self, crn, title, department, time, day, semester, year, credits, instructor):
        cursor.execute("""INSERT INTO COURSE VALUES('%d', '%s', '%s', '%d', '%s', '%s', '%d', '%d', '%s');""" % (crn, title, department, time, day, semester, year, credits, instructor))

    # Remove courses from the system
    def removeCourse(self, title):
        cursor.execute("""DELETE FROM COURSE WHERE title = '%s';""" % title)
        
    # Add instructor
    def addInstructor(self, id, name, surname, title, hireyear, department, email):
        cursor.execute("""INSERT INTO INSTRUCTOR VALUES('%d', '%s', '%s', '%s', '%d', '%s', '%s');""" % (id, name, surname, title, hireyear, department, email))

    # Add student
    def addStudent(self, id, name, surname, gradyear, major, email, course_list):
        cursor.execute("""INSERT INTO STUDENT VALUES('%d', '%s', '%s', '%d', '%s', '%s', '%s');""" % (id, name, surname, gradyear, major, email, course_list))

    # Link instructor/student to course
    def linkStudent(self, studentID, CRN):
        cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % studentID)
        response = cursor.fetchall()
        course_list = response[0][0].split(", ")
        course_list.append(str(CRN))
        course_list = (', ').join(course_list)

        cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list, studentID))
    
    # Unlink student from course
    def unlinkStudent(self, studentID, CRN):
        cursor.execute("""SELECT `COURSE LIST` FROM STUDENT WHERE ID='%d';""" % studentID)
        response = cursor.fetchall()
        course_list = response[0][0].split(", ")
        course_list.remove(str(CRN))
        course_list = (', ').join(course_list)

        cursor.execute("""UPDATE STUDENT SET 'COURSE LIST'='%s' WHERE ID='%d';""" % (course_list, studentID))
    
    # link instructor from course
    def linkInstructor(self, instructorName, CRN):
        cursor.execute("""UPDATE COURSE SET INSTRUCTOR='%s' WHERE CRN='%d';""" % (instructorName, CRN))

    # Unlink instructor from course
    def unlinkInstructor(self, instructorName, CRN):
        cursor.execute("""UPDATE COURSE SET INSTRUCTOR='%s' WHERE INSTRUCTOR='%s' AND CRN='%d';""" % ('---', instructorName, CRN))


# User class demo
isaac = User('Isaac', 'Newton', 10001, 'student')
email = 'newtoni'
# isaac.login(email)
# time.sleep(5)
# isaac.logout()

# return all HUSS courses
# crn, title, department, time, day, semester, year, credits, instructor = 0, None, 'HUSS', 0, None, None, 0, 0, None
# isaac.searchCourses(crn, title, department, time, day, semester, year, credits, instructor)

# return all BSME courses and all courses taught by Jones Yu
# crn, title, department, time, day, semester, year, credits, instructor = 0, None, 'BSME', 0, None, None, 0, 0, 'Jones Yu'
# isaac.searchCourses(crn, title, department, time, day, semester, year, credits, instructor)
   
         
# Student class demo
marie = Student("Marie", "Curie", 10002)
# marie.addCourse('12345')
# marie.removeCourse('12345')
# marie.printSchedule()
# marie.checkConflicts()


# Instructor class demo
jones = Instructor("Jones", "Yu", 20007)
# jones.printSchedule()
# jones.printRoster()


# Admin class demo
mike = Admin("Mike", "Kelly", 10001)
crn, title, department, time, day, semester, year, credits, instructor = 23312, 'ACTUARIAL MATH', 'BSMA', 1400, 'TR', 'SUMMER', 2022, 4, 'Alan Turing'  
# mike.addCourse(crn, title, department, time, day, semester, year, credits, instructor)
# mike.removeCourse(title)

id, name, surname, title, hireyear, department, email = 20008, 'Saurav', 'Basnet', 'Full Prof.', 2017, 'ENGR', 'basnets'
# mike.addInstructor(id, name, surname, title, hireyear, department, email)
id, name, surname, gradyear, major, email, course_list = 10013, 'Don', 'Smith', 2022, 'BSME', 'smithd', '23300, 678980, 23237'
# mike.addStudent(id, name, surname, gradyear, major, email, course_list)

studentID = 10005
new_course = 12345
# mike.linkStudent(studentID, new_course)
# mike.unlinkStudent(studentID, new_course)

instructorName = 'Alan Turing'
CRN = 23236
# mike.linkInstructor(instructorName, CRN)
# mike.unlinkInstructor(instructorName, CRN)

database.commit()
database.close()
