"""This module handles the connection between front-end and database.

Local import:
    model
"""

from datetime import datetime
import random
import string

import model

_db = model.Model()


# ---------------------------------------------------------------------
def add_manager(adding_type: str, **kwargs) -> int:
    """Manages different kind of adds to database.

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
        case "product":
            table = "products"
        case "receipt":
            table = "receipts"
        case "product_user":
            table = "product_users"
        case _:
            return False

    # Returns the last_row_id of insert
    return _db.insert(table=table, **kwargs)


# ---------------------------------------------------------------------
def get_product(**condition_s) -> list:
    """Select all from database products table.

    Args:
        condition_s: Condition(s) for selecting from database.
    Returns:
        list: The list of gotten data(empty list if None).
    """

    condition = ""
    for key, value in condition_s.items():
        if not value:
            continue
        if key in ("price", "count"):
            condition += str(key) + " >= " + f'"{str(value)}"' + " AND "
            continue
        condition += str(key) + " = " + f'"{str(value)}"' + " AND "
    condition = condition[:-4]  # To exclude last AND_
    if condition:
        condition += " ORDER BY price LIMIT 5"

    return _db.select(column_s="*", table="products", condition=condition)


# ---------------------------------------------------------------------
def get_home_header() -> list:
    """Get top 5 products ordered by price.

    Args:
        None.
    Returns:
        list: The list of gotten data.
    """

    condition = "product_id > 0 ORDER BY price LIMIT 5"
    return _db.select(column_s="*", table="products", condition=condition)


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
def buy_product(products: dict, customer_id: int, total_price: int) -> str:
    """Gets info for purchase, writes to db and returns receipt.

    Args:
        products (dict): "product_id: count" Values.
        customer_id (int): The id of customer which is making the purchase.
        total_price (int): Total price of the purchase.
    Returns:
        str: The unique receipt of the purchase.
    """

    tracing_code = _unique_receipt_creator(
        customer_id=customer_id, total_price=total_price
    )
    receipt_id = add_manager(
        adding_type="receipt",
        customer_id=customer_id,
        buy_datetime=datetime.now().strftime("%Y-%m-%d %H:%M"),
        tracing_code=tracing_code,
        total_price=total_price,
        products_count=sum([int(count) for count in products.values()]),
    )
    for product_id, count in products.items():
        add_manager(
            adding_type="product_user",
            receipt_id=receipt_id,
            product_id=product_id,
            count=count,
        )
        available = int(get_product(product_id=product_id)[0][4])
        _db.update(
            table="products",
            condition=f"product_id = {product_id}",
            count=available - count,
        )

    return tracing_code


# ---------------------------------------------------------------------
def _unique_receipt_creator(customer_id, total_price) -> str:
    receipt = f"c{customer_id}p{total_price}_"
    while True:
        receipt += "".join(random.choices(string.ascii_uppercase, k=12))
        if not _db.select(
            column_s="tracing_code",
            table="receipts",
            condition='tracing_code="{receipt}"',
        ):
            break
    return receipt
