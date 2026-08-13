from data.storage import courses, get_next_course_id, save_all
from models.course import Courses
from schemas.course_schema import CourseCreate, CourseUpdate
from exceptions.custom_exceptions import (CourseNotFoundException, InvalidDataException)


def create_course(course_data: CourseCreate) -> Courses:
    if any(course.code == course_data.code for course in courses.values()):
        raise InvalidDataException("کد درس تکراری است")

    course = Courses(
        id = get_next_course_id(),
        title = course_data.title,
        code = course_data.code,
        units = course_data.units,
        capacity = course_data.capacity,
    )
    courses[course.id] = course
    save_all()
    return course

def get_all_courses():
    return list(courses.values())

def get_course_by_id(course_id: int) -> Courses:
    course = courses.get(course_id)
    if course is None:
        raise CourseNotFoundException("درس پیدا نشد")
    return course

def update_course(course_id : int, course_data: CourseUpdate) -> Courses:
    course = get_course_by_id(course_id)

    if course_data.code is not None:
        duplicate = any(
            c.id != course_id and c.code == course_data.code
            for c in courses.values())

        if duplicate:
            raise InvalidDataException("کد درس تکراری است")
        course.code = course_data.code

    if course_data.capacity is not None:
        if course_data.capacity < len(course.students):
            raise InvalidDataException(
                "ظرفیت جدید نمی تواند کمتر از تعداد دانشجویان ثبت نام شده باشد"
            )
        course.capacity = course_data.capacity


    if course_data.title is not None:
        course.title = course_data.title
    if course_data.units is not None:
        course.units = course_data.units

    save_all()
    return course

def delete_course(course_id: int) -> None:
    course = get_course_by_id(course_id)

    #remove this course from all students
    for student in list(course.students):
        if course in student.selected_courses:
            student.selected_courses.remove(course)

    #remove this course from professor
    if course.professor is not None and course in course.professor.courses:
        course.professor.courses.remove(course)

    del courses[course_id]
    save_all()
