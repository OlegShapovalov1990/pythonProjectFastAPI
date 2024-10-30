from fastapi import FastAPI
from pydantic import BaseModel

from utils import json_to_dict_list
import os
from typing import Optional, List

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'students.json')

app = FastAPI()


@app.get("/students")
def get_all_students():
    return json_to_dict_list(path_to_json)


@app.get("/students/{course}")
def get_all_students_course(course: int):
    students = json_to_dict_list(path_to_json)
    return_list = []
    for student in students:
        if student["course"] == course:
            return_list.append(student)
    return return_list


@app.get("/students")
def get_all_students(course: Optional[int] = None):
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list


@app.get("/major/{major}")
def get_majors(major: str):
    students = json_to_dict_list(path_to_json)
    if major is None:
        return students
    else:
        return [i for i in students if i.get("major") == major]


class Special(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    email: str
    phone_number: str
    address: str
    enrollment_year: int
    major: str
    course: int
    special_notes: str


@app.post("/special")
def add_special(students: List[Special]):
    student = json_to_dict_list(path_to_json)
    student.extend(students)
    return {"status": 200, "data": student}
