from data.storage import save_all
from services.student_services import get_student_by_id
from services.professor_services import get_professor_by_id
from services.course_services import get_course_by_id

def select_course_for_student(student_id : int, course_id : int):
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_id)
    student.select_course(course)
    save_all()
    return student

def drop_course_for_student(student_id : int, course_id : int):
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_id)
    student.drop_course(course)
    save_all()
    return student

def get_student_courses(student_id : int):
    student = get_student_by_id(student_id)
    return student.get_courses()

def assign_professor_to_course(course_id : int, professor_id : int):
    course = get_course_by_id(course_id)
    professor = get_professor_by_id(professor_id)
    course.assign_professor(professor)
    save_all()
    return course
