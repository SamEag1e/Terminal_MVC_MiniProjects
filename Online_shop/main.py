# The docstrings are written in almost all module, class
# function, etc. Even though type annotations are almost complete
# anywhere possible. Just for practice purposes.
"""This is route as terminal.

Local import:
    view
"""

import view

client = view.FrontEnd()

while True:
    client.header_home_page()
    match client.tools_home_page():
        case 1:
            # Admin log-in page
            client.log_in_page(is_user=False)
        case 2:
            # Customer log-in page
            client.log_in_page(is_user=True)
            # Admin and customer log-in have the same UI,
            # but different URL.
        case 3:
            client.user_register_page()
        case 4:
            client.search_products_page()
        case 5:
            client.add_to_shopping_cart()
        case 6:
            client.show_shopping_cart()
        case 7:
            client.confirm_purchase()
        case _:
            continue

# ToDo-----------------------------------------------------------------

# Make username, email ... (anything necessary)
# in admins and customers UNIQUE

# Exception handling for wrong inputs...

# Handle the annoying indexes(like [0][0], [0][6]) with making dict ?!

# Extreme points in app (like when products count is 0)
