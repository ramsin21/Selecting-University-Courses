from pydantic import BaseModel, Field


class ProfessorCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, examples = ["Armin"])
    last_name: str = Field(..., min_length=2, max_length=50, examples = ["Rashno"])
    personal_code: str = Field(..., min_length=3, max_length=20, examples = ["12334"])
    department: str = Field(..., min_length=2, max_length=80, examples = ["Computer"])


class ProfessorUpdate(BaseModel):
    first_name: str | None = Field(default = None, min_length=2, max_length=50)
    last_name: str | None = Field(default = None, min_length=2, max_length=50)
    personal_code: str | None = Field(default = None, min_length=3, max_length=20)
    department: str | None = Field(default = None, min_length=2, max_length=80)