
import json
from pathlib import Path


students = {}
professors = {}
courses = {}


_next_student_id = 1
_next_professor_id = 1
_next_course_id = 1


BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

FILES_DIR.mkdir(exist_ok=True)


STUDENTS_FILE = FILES_DIR / "students.json"
PROFESSORS_FILE = FILES_DIR / "professors.json"
COURSES_FILE = FILES_DIR / "courses.json"


# =========================
# ID GENERATORS
# =========================

def get_next_student_id() -> int:

    global _next_student_id

    current_id = _next_student_id

    _next_student_id += 1

    return current_id


def get_next_professor_id() -> int:

    global _next_professor_id

    current_id = _next_professor_id

    _next_professor_id += 1

    return current_id


def get_next_course_id() -> int:

    global _next_course_id

    current_id = _next_course_id

    _next_course_id += 1

    return current_id


# =========================
# JSON
# =========================

def _read_json(file_path: Path):

    if not file_path.exists():
        return []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        try:
            return json.load(file)

        except json.JSONDecodeError:
            return []


def _write_json(file_path: Path, data) -> None:

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================
# SAVE
# =========================

def save_all() -> None:

    # -------------------------
    # Students
    # -------------------------

    students_data = []

    for student in students.values():

        students_data.append({

            "id": student.id,

            "first_name": student.first_name,

            "last_name": student.last_name,

            "student_number": student.student_number,

            "major": student.major,

            "selected_course_ids": [
                course.id
                for course in student.selected_courses
            ],

        })


    # -------------------------
    # Professors
    # -------------------------

    professors_data = []

    for professor in professors.values():

        professors_data.append({

            "id": professor.id,

            "first_name": professor.first_name,

            "last_name": professor.last_name,

            "personal_code": professor.personal_code,

            "department": professor.department,

            "course_ids": [
                course.id
                for course in professor.courses
            ],

        })


    # -------------------------
    # Courses
    # -------------------------

    courses_data = []

    for course in courses.values():

        courses_data.append({

            "id": course.id,

            "title": course.title,

            "code": course.code,

            "unit": course.units,

            "capacity": course.capacity,

            # اصلاح اصلی این قسمت
            "professor_id":
                None
                if course.professor is None
                else course.professor.id,

            "student_ids": [
                student.id
                for student in course.students
            ],

        })


    _write_json(
        STUDENTS_FILE,
        students_data
    )

    _write_json(
        PROFESSORS_FILE,
        professors_data
    )

    _write_json(
        COURSES_FILE,
        courses_data
    )


# =========================
# RESET
# =========================

def reset_storage(
    delete_files: bool = False
) -> None:

    global \
        _next_student_id, \
        _next_professor_id, \
        _next_course_id


    students.clear()

    professors.clear()

    courses.clear()


    _next_student_id = 1

    _next_professor_id = 1

    _next_course_id = 1


    if delete_files:

        for file_path in [
            STUDENTS_FILE,
            PROFESSORS_FILE,
            COURSES_FILE
        ]:

            if file_path.exists():

                file_path.unlink()


# =========================
# LOAD
# =========================

def load_all() -> None:

    """
    Load data from JSON files
    and rebuild object relationships.
    """

    global \
        _next_student_id, \
        _next_professor_id, \
        _next_course_id


    from models.student import Student

    from models.professor import Professor

    from models.course import Courses


    students.clear()

    professors.clear()

    courses.clear()


    students_data = _read_json(
        STUDENTS_FILE
    )

    professors_data = _read_json(
        PROFESSORS_FILE
    )

    courses_data = _read_json(
        COURSES_FILE
    )


    # =========================
    # Students
    # =========================

    for item in students_data:

        student = Student(

            id=int(item["id"]),

            first_name=item["first_name"],

            last_name=item["last_name"],

            student_number=item["student_number"],

            major=item["major"],

        )

        students[student.id] = student


    # =========================
    # Professors
    # =========================

    for item in professors_data:

        professor = Professor(

            id=int(item["id"]),

            first_name=item["first_name"],

            last_name=item["last_name"],

            personal_code=item["personal_code"],

            department=item["department"]

        )

        professors[professor.id] = professor


    # =========================
    # Courses
    # =========================

    for item in courses_data:

        course = Courses(

            id=int(item["id"]),

            title=item["title"],

            code=item["code"],

            units=int(item["unit"]),

            capacity=int(item["capacity"]),

        )

        courses[course.id] = course


    # =========================
    # Rebuild relationships
    # =========================

    for item in courses_data:

        course = courses.get(
            int(item["id"])
        )

        if course is None:
            continue


        # -------------------------
        # Professor
        # -------------------------

        professor_id = item.get(
            "professor_id"
        )

        if (
            professor_id is not None
            and int(professor_id) in professors
        ):

            professor = professors[
                int(professor_id)
            ]

            course.professor = professor


            if course not in professor.courses:

                professor.courses.append(
                    course
                )


        # -------------------------
        # Students
        # -------------------------

        student_ids = item.get(
            "student_ids",
            item.get("student_id", [])
        )


        for student_id in student_ids:

            student = students.get(
                int(student_id)
            )

            if student is None:
                continue


            if student not in course.students:

                course.students.append(
                    student
                )


            if course not in student.selected_courses:

                student.selected_courses.append(
                    course
                )


    # =========================
    # Next IDs
    # =========================

    _next_student_id = (
        max(students.keys()) + 1
        if students
        else 1
    )


    _next_professor_id = (
        max(professors.keys()) + 1
        if professors
        else 1
    )


    _next_course_id = (
        max(courses.keys()) + 1
        if courses
        else 1
    )

