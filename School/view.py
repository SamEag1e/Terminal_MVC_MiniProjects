"""Front-end as terminal for users to interact with database.

Class:
    FrontEnd: An object simulating front-end as terminal.

Local import:
    import controller
"""

import time

import controller


class FrontEnd:
    """An object simulating front-end as terminal.

    Attributes:
        logged_in (bool): Initialized as False.
        type (int): Role_id of client (if logged in).
        id (int): customer_id or admin_id from database.
        name (str): Username from database.
    """

    def __init__(self) -> None:
        self.logged_in = False
        self.type = None  # Teacher:1, expert:2 or manager:3
        self.name = None
        self.id = None

    # -----------------------------------------------------------------
    def log_in_page(self) -> int:
        """Login interface for staff."""
        print("user: M1(Manager), E1(Expert) or T1(Teacher). pw: 1234")
        user_data = controller.authenticate(
            user=input("Username or email:\t"),
            pw=input("Password:\t"),
        )

        if user_data["flag"]:
            self.logged_in = True
            self.id = user_data["staff_id"]
            self.name = user_data["username"]
            self.type = user_data["role_id"]
            print(f"Successful login!\nWelcome {self.name} !")
            time.sleep(1)
            return self.type

        print("Wrong username or pw! Returning to home page...\n")
        time.sleep(1)
        return 404

    # -----------------------------------------------------------------
    def log_out(self) -> None:
        """Log out"""
        print(f"Bye {self.name} !")
        self.logged_in = False
        self.type = None
        self.name = None
        self.id = None

    # -----------------------------------------------------------------
    def teacher_page(self) -> None:
        """Teacher tools page"""
        while True:
            match int(input("1. Log out 2. All students:\t")):
                case 1:
                    self.log_out()
                    break
                case 2:
                    print(*controller.get_all_students())
                case _:
                    print("Enter a valid number")
                    continue

    # -----------------------------------------------------------------
    def expert_page(self) -> None:
        """Expert tools page"""
        while True:
            check = int(
                input(
                    """\t\t\t1. Log out 2. Courses
                    3. Course_students 4. Add students to a course
                    """
                )
            )
            match check:
                case 1:
                    self.log_out()
                    break
                case 2:
                    print(*controller.get_all_courses())
                case 3:
                    print(controller.get_student_in_courses())
                case 4:
                    while True:
                        course = int(
                            input(
                                "ID of the course you want to add students:\t"
                            )
                        )
                        if controller.check_courses(course):
                            break
                        print("Course_ID does not exist!")
                    while True:
                        student = (
                            input("Student username(finish to end):\t")
                        ).lower()
                        if student == "finish":
                            break
                        print(
                            controller.add_student_to_course(
                                course=course, student=student
                            )
                        )
                case _:
                    print("Enter a valid number")
                    continue

    # -----------------------------------------------------------------
    def manager_page(self) -> None:
        """Manager tools page"""
        while True:
            check = int(
                input(
                    """\t\t\t1. Log out 2. Courses
                    3. Course_students 4. Add course
                    """
                )
            )
            match check:
                case 1:
                    self.log_out()
                    break
                case 2:
                    print(*controller.get_all_courses())
                case 3:
                    print(controller.get_student_in_courses())
                case 4:
                    while True:
                        course_name = input("Course name(finish to end):\t")
                        if course_name == "finish":
                            break
                        controller.add_course(course_name=course_name)

                case _:
                    print("Enter a valid number")
                    continue
