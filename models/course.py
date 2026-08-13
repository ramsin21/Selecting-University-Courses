from exceptions.custom_exceptions import (CourseAlreadySelectedException,
    CourseFullException, CourseNotSelectedException, ProfessorAlreadyAssignedException)

class Courses:
    def __init__(self, id, title : str, code : int, units, capacity, major=None):

        self.id = id
        self.title = title
        self.code = code
        self.units = units
        self.capacity = capacity
        self.major = major
        self.professor = None
        self.students = []
        
    def is_full(self):
        return len(self.students) >= self.capacity
    
    def add_student(self, student):
        if student in self.students:
            raise CourseAlreadySelectedException(
                "دانشجو قبلا در این درس ثبت شده است"
            )
        if self.is_full():
            raise CourseFullException("ظرفیت درس تکمیل شده است")
        self.students.append(student)


    def remove_student(self, student):
        if student not in self.students:
            raise CourseNotSelectedException("دانشجو در این درس ثبت نام نکرده است")
        self.students.remove(student)
            
    def assign_professor(self, professor):
        if self.professor is not None and self.professor.id == professor.id:
            raise ProfessorAlreadyAssignedException(
                "درس قبلا به این استاد اختصاص داده شده است"
            )
        if self.professor is not None and self.professor.id != professor.id:
            raise ProfessorAlreadyAssignedException("این درس قبلا استاد دارد")

        self.professor = professor
        professor.assign_course(self)


    def to_dict(self):
        return {
            "id" : self.id,
            "title": self.title,
            "code": self.code,
            "units": self.units,
            "capacity": self.capacity,
            "major": self.major,
            "remaining_capacity" : self.capacity - len(self.students),
            "professor" : None if self.professor is None else {
                "id" : self.professor.id,
                "first_name" : self.professor.first_name,
                "last_name" : self.professor.last_name,
                "personal_code" : self.professor.personal_code
            },
            "students" : [
                {
                    "id" : student.id,
                    "first_name" : student.first_name,
                    "last_name" : student.last_name,
                    "student_number" : student.student_number
                }
                for student in self.students
            ]
        }