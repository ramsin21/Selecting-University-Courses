from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, examples = ["Advanced Python Programming"])
    code: str = Field(..., min_length=2, max_length=20, examples = ["CS301"])
    units: int = Field(..., ge=1, le=5, examples = ["3"])
    capacity: int = Field(..., ge=1, le=200, examples = ["35"])


class CourseUpdate(BaseModel):
    title: str | None = Field(default = None, min_length=2, max_length=100)
    code: str | None = Field(default = None, min_length=2, max_length=20)
    units: int | None = Field(default = None, ge=1, le=5)
    capacity: int | None = Field(default = None, ge=1, le=200)