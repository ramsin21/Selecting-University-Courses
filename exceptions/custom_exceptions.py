class CourseSelectionException(Exception):
    """Base exception for course selection system."""

class ProfessorAlreadyAssignedException(CourseSelectionException):
    pass

class CourseAlreadySelectedException(CourseSelectionException):
    pass

class CourseNotSelectedException(CourseSelectionException):
    pass

class CourseFullException(CourseSelectionException):
    pass

class InvalidDataException(CourseSelectionException):
    pass

class StudentNotFoundException(CourseSelectionException):
    pass

class ProfessorNotFoundException(CourseSelectionException):
    pass

class CourseNotFoundException(CourseSelectionException):
    pass

