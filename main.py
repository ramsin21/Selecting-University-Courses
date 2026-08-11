from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from exceptions.custom_exceptions import (
    CourseAlreadySelectedException,
    CourseFullException,
    CourseNotSelectedException,
    CourseSelectionException,
    StudentNotFoundException,
    ProfessorAlreadyAssignedException,
    InvalidDataException,
    ProfessorNotFoundException,
    CourseNotFoundException
)

from routers.students import router as student_router
from routers.professors import router as professor_router
from routers.courses import router as course_router

from data.storage import load_all, save_all, students, professors, courses


app = FastAPI(
    title="Simple Course Selection System",
    description="پروژه پایانی درس برنامه نویسی پیشرفته برای دانشجویان علاقمند دانشگاه لرستان",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(student_router)
app.include_router(professor_router)
app.include_router(course_router)


@app.on_event("startup")
def startup_load_data():
    load_all()


@app.on_event("shutdown")
def shutdown_save_data():
    save_all()


# -----------------------------
# Frontend
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / "front"


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(FRONT_DIR / "index.html")


app.mount(
    "/",
    StaticFiles(directory=FRONT_DIR, html=True),
    name="frontend"
)


@app.get("/debug/storage", tags=["Debug"])
def debug_storage_summary():
    return {
        "students_count": len(students),
        "professors_count": len(professors),
        "course_count": len(courses),
        "storage_folder": "data/files"
    }


@app.get("/debug/storage/all", tags=["Debug"])
def debug_storage_all():
    return {
        "students": [student.to_dict() for student in students.values()],
        "professor": [professor.to_dict() for professor in professors.values()],
        "course": [course for course in courses.values()]
    }


@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(
    request: Request,
    exc: StudentNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "Error": "دانشجو پیدا نشد",
            "message": str(exc)
        },
    )


@app.exception_handler(ProfessorNotFoundException)
async def professor_not_found_handler(
    request: Request,
    exc: ProfessorNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "ProfessorNotFound",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseNotFoundException)
async def course_not_found_handler(
    request: Request,
    exc: CourseNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "CourseNotFound",
            "message": str(exc)
        },
    )


@app.exception_handler(InvalidDataException)
async def invalid_data_exception_handler(
    request: Request,
    exc: InvalidDataException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "InvalidData",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseFullException)
async def course_full_exception_handler(
    request: Request,
    exc: CourseFullException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "CourseFull",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseAlreadySelectedException)
async def course_already_selected_exception_handler(
    request: Request,
    exc: CourseAlreadySelectedException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "CourseAlreadySelected",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseNotSelectedException)
async def course_not_selected_exception_handler(
    request: Request,
    exc: CourseNotSelectedException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "CourseNotSelected",
            "message": str(exc)
        },
    )


@app.exception_handler(ProfessorAlreadyAssignedException)
async def professor_already_assigned_handler(
    request: Request,
    exc: ProfessorAlreadyAssignedException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "ProfessorAlreadyAssigned",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseSelectionException)
async def course_selection_exception_handler(
    request: Request,
    exc: CourseSelectionException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "CourseSelectionException",
            "message": str(exc)
        },
    )


@app.exception_handler(CourseNotSelectedException)
async def course_not_selected_handler(
    request: Request,
    exc: CourseNotSelectedException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "CourseNotSelected",
            "message": str(exc)
        },
    )