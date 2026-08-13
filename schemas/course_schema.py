from pydantic import BaseModel, Field, field_validator


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, examples=["Advanced Python Programming"])
    code: str | None = Field(default=None, min_length=2, max_length=20, examples=["CS301"])
    units: int = Field(..., ge=1, le=5, examples=["3"])
    capacity: int = Field(..., ge=1, le=200, examples=["35"])
    major: str | None = Field(default=None, max_length=80, examples=["Computer Engineering"])

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("نام درس الزامی است")
        return v.strip()

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("کد درس نمی‌تواند خالی باشد")
        return v.strip() if v else v


class CourseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    code: str | None = Field(default=None, min_length=2, max_length=20)
    units: int | None = Field(default=None, ge=1, le=5)
    capacity: int | None = Field(default=None, ge=1, le=200)
    major: str | None = Field(default=None, max_length=80)