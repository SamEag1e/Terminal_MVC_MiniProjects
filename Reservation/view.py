"""Front-end as terminal for users to interact with database.

Class:
    FrontEnd: An object simulating front-end as terminal.

Local import:
    controller
"""

import time

import controller


class FrontEnd:
    """An object simulating front-end as terminal.

    Attributes:
        logged_in (bool): Initialized as False.
        type (str): Type of client (if logged in).
        id (int): customer_id or admin_id from database.
        name (str): Username from database.
    """

    def __init__(self) -> None:
        self.logged_in = False
        self.type = None  # admin or customer
        self.id = None
        self.name = None

    # -----------------------------------------------------------------
    def log_in_page(self, is_user=True) -> None:
        """Login interface for customer and admin.

        Args:
            is_user: Declares the type of login. True is for customer
                and False for admin login.
        Returns:
            None
        """
        user_data = controller.authenticate(
            user=input("Username or email:\t"),
            pw=input("Password:\t"),
            is_user=is_user,
        )

        if user_data["flag"]:
            self.logged_in = True
            self.type = "customer" if is_user else "admin"
            self.id = user_data["id"]
            self.name = user_data["username"]
            print("Successful login!")
            time.sleep(1)
            if not is_user:
                self.admin_tools_page()
        else:
            print("Wrong username or pw! Returning to home page...\n")
            time.sleep(1)

    # -----------------------------------------------------------------
    def admin_tools_page(self) -> None:
        """Navigation page for admin."""
        while True:
            check = int(
                input(
                    f"""\n\t\tWelcome {self.name}!
                    1. Add ticket
                    2. Add admin
                    3. Log out
                    Your choice(number):\t"""
                )
            )
            match check:
                case 1:
                    self.admin_add_ticket_page()
                case 2:
                    self.admin_add_admin_page()
                case 3:
                    self.logged_in = False
                    self.type = None
                    self.id = None
                    self.name = None
                    print("See you soon! Redirecting to home page...")
                    time.sleep(1)
                    break
                case _:
                    print("Enter a valid number!")
                    time.sleep(1)

    # -----------------------------------------------------------------
    @staticmethod
    def admin_add_ticket_page() -> None:
        """Admin add new tickets to database."""
        print("This is admin_add_ticket page")
        controller.add_manager(
            adding_type="ticket",
            transport_mode=(input("transport_mode:\t")).lower(),
            origin=(input("origin:\t").lower()).lower(),
            destination=(input("destination:\t")).lower(),
            departure=input("departure:\t"),
            arrival=input("arrival:\t"),
            price=input("price:\t"),
            count=input("count:\t"),
        )

    # -----------------------------------------------------------------
    @staticmethod
    def admin_add_admin_page() -> None:
        """Admin add new admin(s) to database."""
        print("This is admin_add_admin page")
        controller.add_manager(
            adding_type="admin",
            national_code=input("national_code:\t"),
            phone=input("phone:\t"),
            email=input("email:\t"),
            username=input("username:\t"),
            pw=input("pw:\t"),
            f_name=input("f_name:\t"),
            l_name=input("l_name:\t"),
        )

    # -----------------------------------------------------------------
    @staticmethod
    def user_register_page() -> None:
        """User register and add their info to database."""
        print("This is user_login page")
        controller.add_manager(
            adding_type="customer",
            national_code=input("national_code:\t"),
            phone=input("phone:\t"),
            email=input("email:\t"),
            username=input("username:\t"),
            pw=input("pw:\t"),
            f_name=input("f_name:\t"),
            l_name=input("l_name:\t"),
        )

    # -----------------------------------------------------------------
    def header_home_page(self) -> None:
        """Header of home page."""
        print("=" * 64)
        print(f'\n\n\t\tWelcome {self.name if self.name else ""}!')
        print("\tThis is the home page.")
        print(*controller.get_home_header(), sep="\n")
        print(
            "(ticket_id, transport_mode, origin, destination,\
            departure, arrival, price, count)"
        )
        time.sleep(1)

    # -----------------------------------------------------------------
    @staticmethod
    def tools_home_page() -> int:
        """Navigation page in home page."""
        while True:
            check = int(
                input(
                    """\n\t\tWelcome to ALIBABA terminal!
                    1. Admin log-in
                    2. User log-in
                    3. User register
                    4. Search tickets
                    5. Buy ticket(s)
                    Your choice(number):\t"""
                )
            )
            if check in range(1, 5 + 1):
                return check
            print("Enter a valid number!")

    # -----------------------------------------------------------------
    @staticmethod
    def filter_tickets_page() -> None:
        """Search tickets"""
        print("(Just press enter if you don't want to include any of these.)")
        print(
            controller.get_ticket(
                transport_mode=(input("transport_mode:\t")).lower(),
                origin=(input("origin:\t").lower()).lower(),
                destination=(input("destination:\t")).lower(),
                departure=input("departure(bigger than):\t"),
                arrival=input("arrival(bigger than):\t"),
                price=input("price(bigger than):\t"),
                count=input("count(bigger than):\t"),
            )
        )
        time.sleep(1)

    # -----------------------------------------------------------------
    def buy_ticket_page(self) -> str:
        """User is asked to enter information to buy tickets."""
        if not self.logged_in:
            print("You need to log-in first!")
            self.log_in_page(is_user=True)
        if not self.logged_in:
            return "Unsuccessful log-in. Returning to home page..."

        ticket_info = controller.get_ticket(ticket_id=input("ticket_id:\t"))
        print("Ticket info: ", ticket_info)
        available_seats = controller.get_available_seats(
            ticket_id=ticket_info[0][0]
        )
        print("Available seats: ", available_seats)
        count = int(input("How many tickets you want to buy:\t"))

        print("Enter ticket users information(including yourself if so).")
        ticket_users = {}
        for ticket_user in range(1, count + 1):
            print(f"Information of user number {ticket_user}:")
            ticket_users[ticket_user] = {
                "national_code": input("national_code:\t"),
                "phone": input("phone:\t"),
                "f_name": input("f_name:\t"),
                "l_name": input("l_name:\t"),
            }
            while True:
                seat = int(input("Seat number:\t"))
                if seat in available_seats:
                    ticket_users[ticket_user]["seat_number"] = seat
                    available_seats.remove(seat)
                    # We need to handle the situation where
                    # someone is reserving the seat
                    # but in the meantime someone else buys it,
                    # so it's not available anymore.
                    break
                print("Choose an available seat!")
        # Check
        # print(ticket_users)

        if self.payment_page(int(ticket_info[0][6]) * count):
            receipt = controller.buy_ticket(
                ticket_users=ticket_users,
                buyer_id=self.id,
                ticket_info=ticket_info,
                count=count,
            )
            print(
                f"Have a safe travel {self.name}. Keep this receipt: ", receipt
            )
            time.sleep(1)
            return "Successful"
        print("Unsuccessful payment. Returning to home page...")
        time.sleep(1)
        return "Unsuccessful"

    # -----------------------------------------------------------------
    @staticmethod
    def payment_page(total_price) -> bool:
        """User is asked to pay the total price."""
        while True:
            payment = int(
                input(f"Pay {total_price}(Enter the number or 0 to exit):\t")
            )
            if payment == 0:
                return False
            if payment == total_price:
                return True
            print("Invalid number")
