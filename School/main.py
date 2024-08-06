"""This is route as terminal.

Local import:
   import view
"""

import view

client = view.FrontEnd()

while True:
    match client.log_in_page():
        case 1:
            # Teacher
            client.teacher_page()
        case 2:
            # Expert
            client.expert_page()
        case 3:
            # Manager
            client.manager_page()
        case _:
            continue
