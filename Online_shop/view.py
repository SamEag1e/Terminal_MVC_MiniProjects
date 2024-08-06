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
        shopping_cart (dict): Shopping cart.
    """

    def __init__(self) -> None:
        self.logged_in = False
        self.type = None  # admin or customer
        self.id = None
        self.name = None
        self.shopping_cart = {}

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
                    1. Add product
                    2. Add admin
                    3. Log out
                    Your choice(number):\t"""
                )
            )
            match check:
                case 1:
                    self.admin_add_product_page()
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
    def admin_add_product_page() -> None:
        """Admin add new products to database."""
        print("This is admin_add_product page")
        controller.add_manager(
            adding_type="product",
            product_type=(input("product_type:\t")).lower(),
            product_name=(input("product_name:\t")).lower(),
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
        print("(product_type, product_name, price, count)")
        time.sleep(1)

    # -----------------------------------------------------------------
    @staticmethod
    def tools_home_page() -> int:
        """Navigation page in home page."""
        while True:
            check = int(
                input(
                    """\n\t\tWelcome to ONLINE_SHOP terminal!
                    1. Admin log-in
                    2. User log-in
                    3. User register
                    4. Search products
                    5. Add product(s) to shopping-cart
                    6. Show shopping-cart
                    7. Confirm purchase
                    Your choice(number):\t"""
                )
            )
            if check in range(1, 7 + 1):
                return check
            print("Enter a valid number!")

    # -----------------------------------------------------------------
    @staticmethod
    def search_products_page() -> None:
        """Search products"""
        print("(Just press enter if you don't want to include any of these.)")
        print(
            *controller.get_product(
                product_type=(input("product_type:\t")).lower(),
                product_name=(input("product_name:\t")).lower(),
                price=input("price(bigger than):\t"),
                count=input("count(bigger than):\t"),
            ), sep="\n"
        )
        time.sleep(1)

    # -----------------------------------------------------------------
    def add_to_shopping_cart(self) -> bool:
        """User is asked to enter information to buy products."""
        if not self.logged_in:
            print("You need to log-in first!")
            self.log_in_page(is_user=True)
        if not self.logged_in:
            return False

        while True:
            print("Enter 0 to exit buying")
            product_id = int(input("product_id:\t"))
            count = int(input("count:\t"))
            if (product_id == 0 or
                    count == 0):
                return True
            product_info = controller.get_product(product_id=product_id)
            if product_info:
                if int(product_info[0][4]) > count:
                    self.shopping_cart[product_id] = count
            else:
                print("Enter an available product_id")

    # -----------------------------------------------------------------
    def show_shopping_cart(self) -> bool:
        """Show the shopping"""
        if (not self.logged_in or
                not self.shopping_cart):
            print("You don't have any shopping")
            return False
        print(self.shopping_cart)
        return True

    # -----------------------------------------------------------------
    def confirm_purchase(self) -> None:
        """User confirms buying"""
        total_price = 0
        for pid, count in self.shopping_cart.items():
            total_price += (
                    count * int((controller.get_product(product_id=pid))[0][3])
            )

        if self.payment_page(total_price):
            receipt = controller.buy_product(
                    products=self.shopping_cart,
                    customer_id=self.id,
                    total_price=total_price,
            )
            print(
                f"Thanks for choosing us {self.name}!\
                Keep this receipt: ", receipt
            )
            self.shopping_cart = {}
            time.sleep(1)
        else:
            print("Unsuccessful payment. Returning to home page...")
            time.sleep(1)

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
