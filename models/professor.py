from models.person import Person
from exceptions.custom_exceptions import ProfessorAlreadyAssignedException


class Professor(Person):

    def __init__(
        self,
        id,
        first_name,
        last_name,
        personal_code,
        department
    ):
        super().__init__(id, first_name, last_name)

        self.personal_code = personal_code
        self.department = department
        self.courses = []

    def assign_course(self, course):

        if course in self.courses:
            raise ProfessorAlreadyAssignedException(
                "این درس قبلا به استاد اختصاص داده شده است"
            )

        self.courses.append(course)

    def get_courses(self):
        return self.courses

    def to_dict(self):

        data = super().to_dict()

        data.update({
            "personal_code": self.personal_code,
            "department": self.department,

            "courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "code": course.code,
                    "units": course.units
                }

                for course in self.courses
            ]
        })

        return data