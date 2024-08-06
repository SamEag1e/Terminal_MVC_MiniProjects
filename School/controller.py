"""This module handles the connection between front-end and database.

Local import:
    import model
"""

import model

_db = model.Model()


# ---------------------------------------------------------------------
def authenticate(user, pw) -> dict:
    """Authenticate admin or user and return their info.

    Args:
        user (str): The email/username of staff.
        pw (str): The password related to staff.
    Returns:
        dict: flag, staff_id, username and role_id of staff.
            returns False, None, None and None if it doesn't find any.
    """
    result = _db.select(
        column_s="staff_id, username, role_id",
        table="staff",
        condition=f'(username="{user}" OR email="{user}") AND password="{pw}"',
    )
    # Check
    # print(result)
    if result:
        return {
            "flag": True,
            "staff_id": result[0][0],
            "username": result[0][1],
            "role_id": result[0][2],
        }
    return {
        "flag": False,
        "staff_id": None,
        "username": None,
        "role_id": None,
    }


# ---------------------------------------------------------------------
def add_course(course_name: str) -> int:
    """Add course"""
    return _db.insert(table="courses", course_name=course_name)


# ---------------------------------------------------------------------
def add_student_to_course(course: int, student: str) -> str:
    """Add a student to a course"""
    if not _db.select(
        column_s="*", table="students", condition=f'username="{student}"'
    ):
        student_id = _db.insert(table="students", username=student)
        _db.insert("course_students", course_id=course, student_id=student_id)
        return "New student added to the course"
    student_id = (
        _db.select(
            column_s="student_id",
            table="students",
            condition=f'username="{student}"',
        )
    )[0][0]
    _db.insert("course_students", course_id=course, student_id=student_id)
    return "Existing student added to the course"


# ---------------------------------------------------------------------
def get_student_in_courses() -> dict:
    """Get students in courses"""
    courses = dict(
        _db.select(
            column_s="course_id, course_name", table="courses", condition=""
        )
    )
    result = {}
    for course_id, course_name in courses.items():
        student_usernames = []
        for s_id in _db.select(
            column_s="student_id",
            table="course_students",
            condition=f"course_id={course_id}",
        ):
            student_usernames.append(
                _db.select(
                    column_s="username",
                    table="students",
                    condition=f"student_id={s_id[0]}",
                )[0][0]
            )
        result[course_name] = student_usernames

    return result


# ---------------------------------------------------------------------
def get_all_courses() -> list:
    """Get all courses"""
    return _db.select(
        column_s="course_id, course_name", table="courses", condition=""
    )


# ---------------------------------------------------------------------
def check_courses(course_id: int) -> list:
    """Get all courses"""
    return _db.select(
        column_s="*", table="courses", condition=f"course_id={course_id}"
    )


# ---------------------------------------------------------------------
def get_all_students() -> list:
    """Get all students"""
    return _db.select(
        column_s="student_id, username", table="students", condition=""
    )


# ---------------------------------------------------------------------
def get_teachers() -> list:
    """Get all teachers"""
    return _db.select(
        column_s="staff_id, username", table="staff", condition="role_id=1"
    )
