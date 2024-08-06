"""This module handles the connection between front-end and database.

Local import:
    import model
"""

from datetime import datetime
import random
import string

import model

_db = model.Model()


# ---------------------------------------------------------------------
def add_manager(adding_type: str, **kwargs) -> int:
    """Manages different kind of adds to database. Returns last_row_id.

    Args:
        adding_type (str): The table name that will be written to.
        kwargs: The "column: values" to be added to the table.
    Returns:
        int: The id of last add(which will be used for relations in db).
    """

    match adding_type:
        case "admin":
            table = "admins"
        case "customer":
            table = "customers"
        case "ticket":
            table = "tickets"
        case "receipt":
            table = "receipts"
        case "ticket_user":
            table = "ticket_users"
        case _:
            return False

    # Returns the last_row_id of insert
    return _db.insert(table=table, **kwargs)


# ---------------------------------------------------------------------
def get_ticket(**condition_s) -> list:
    """Select all from database tickets table.

    Args:
        condition_s (str): Condition(s) for selecting from database.
    Returns:
        list: The list of gotten data(empty list if None).
    """

    condition = ""
    for key, value in condition_s.items():
        if not value:
            continue
        if key in ("departure", "arrival", "price", "count"):
            condition += str(key) + " >= " + f'"{str(value)}"' + " AND "
            continue
        condition += str(key) + " = " + f'"{str(value)}"' + " AND "
    condition = condition[:-4]  # To exclude last AND_
    if condition:
        condition += " ORDER BY departure LIMIT 5"

    return _db.select(column_s="*", table="tickets", condition=condition)


# ---------------------------------------------------------------------
def get_home_header() -> list:
    """Get tickets which departure is bigger than now.

    Args:
        None.
    Returns:
        list: The list of gotten data.
    """

    condition = f"""`departure` >= "{datetime.now().strftime("%Y-%m-%d %H:%M")}"
            ORDER BY departure
            LIMIT 5"""
    return _db.select(column_s="*", table="tickets", condition=condition)


# ---------------------------------------------------------------------
def get_available_seats(ticket_id: int) -> list:
    """Get ticket_id and return list of not reserved seats.

    Args:
        ticket_id (int): The ticket_id which we want to check its seats.
    Returns:
        list: The list of gotten data(empty list if None).
    """

    reserved = _db.select(
        column_s="seat_number",
        table="ticket_users",
        condition=f"ticket_id={ticket_id}",
    )
    reserved = [num[0] for num in reserved]
    # Check
    # print("reserved:", reserved)
    all_seats = int(
        _db.select(
            column_s="count",
            table="tickets",
            condition=f"ticket_id={ticket_id}",
        )[0][0]
    )
    return [num for num in range(1, all_seats + 1) if num not in reserved]


# ---------------------------------------------------------------------
def authenticate(user, pw, is_user=True) -> dict:
    """Authenticate admin or user and return their info.

    Args:
        user (str): The email/username of customer/admin.
        pw (str): The password related to customer/admin.
        is_user (bool): Declares the type of user.
            True is for customer and False for admin.
    Returns:
        dict: flag, id and username of customer/admin.
            returns False, None and None if it doesn't find any.
    """
    result = _db.select(
        column_s="customer_id, username" if is_user else "admin_id, username",
        table="customers" if is_user else "admins",
        condition=f'(username="{user}" OR email="{user}") AND pw="{pw}"',
    )
    # Check
    # print(result)
    if result:
        return {
            "flag": True,
            "id": result[0][0],
            "username": result[0][1],
        }
    return {"flag": False, "id": None, "username": None}


# ---------------------------------------------------------------------
def buy_ticket(
    ticket_users: dict, buyer_id: str, ticket_info: list, count: int
) -> str:
    """Gets info for purchase, writes to db and returns receipt.

    Args:
        ticket_users (dict): The information for each user of a ticket.
        buyer_id (int): The id of customer which is making the purchase.
        ticket_info (int): The info related to ticket.(id, price, etc.)
        count (int): The count of tickets which is being bought in
            one purchase.
    Returns:
        str: The unique receipt of the purchase.
    """

    tracing_code = _unique_receipt_creator(
        ticket_id=ticket_info[0][0], count=count
    )
    receipt_id = add_manager(
        adding_type="receipt",
        ticket_id=ticket_info[0][0],
        buyer_id=buyer_id,
        buy_datetime=datetime.now().strftime("%Y-%m-%d %H:%M"),
        tracing_code=tracing_code,
        total_price=int(ticket_info[0][6]) * count,
        tickets_count=count,
    )
    for user in ticket_users.values():
        add_manager(
            adding_type="ticket_user",
            receipt_id=receipt_id,
            ticket_id=ticket_info[0][0],
            national_code=user["national_code"],
            phone=user["phone"],
            f_name=user["f_name"],
            l_name=user["l_name"],
            seat_number=user["seat_number"],
        )

    return tracing_code


# ---------------------------------------------------------------------
def _unique_receipt_creator(ticket_id, count) -> str:
    receipt = f"t{ticket_id}c{count}_"
    while True:
        receipt += "".join(random.choices(string.ascii_uppercase, k=12))
        if not _db.select(
            column_s="tracing_code",
            table="receipts",
            condition='tracing_code="{receipt}"',
        ):
            break
    return receipt
