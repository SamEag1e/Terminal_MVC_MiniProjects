"""This module contains one class for database dynamic read/write.

Class:
    Model: An object to read/write dynamically from/to database.
Third party import:
    mysql.connector(for windows, pip install mysql.connector)
"""

import mysql.connector


class Model:
    """DataBase dynamic read/write."""

    def __init__(
        self, user="root", pw="admin", host="localhost", db_name="online_shop"
    ) -> None:
        """Initialize the model.

        Args:
            user: Username for connecting to db. (default="root")
            pw: Password for connecting to db. (default="admin")
            host: Host for connecting to db. (default="localhost")
            db_name: Name of the database that will be connected.
                (default="ali_baba")
        Return:
            None
        """

        self.user = user
        self.pw = pw
        self.host = host
        self.data_base = db_name
        self.connection = None
        self.cursor = None

    # -----------------------------------------------------------------
    def _open(self) -> None:
        connection = mysql.connector.connect(
            user=self.user,
            password=self.pw,
            host=self.host,
            database=self.data_base,
        )
        self.connection = connection
        self.cursor = connection.cursor()

    # -----------------------------------------------------------------
    def _close(self) -> None:
        self.cursor.close()
        self.connection.close()

    # -----------------------------------------------------------------
    def insert(self, table: str, **kwargs) -> int:
        """Inserts to database with given info and returns last_row_id.

        Args:
            table (str): Name of the table which data will be
                written to.
            kwargs: The "column: values" which will be added to the table.
        Returns:
            int: The last_row_id
        """

        columns = kwargs.keys()
        values = kwargs.values()
        query = f"INSERT INTO `{table}` "
        query += (
            "(" + ", ".join(["`%s`"] * len(columns)) % tuple(columns) + ")"
        )
        query += (
            " VALUES ("
            + ", ".join(['"%s"'] * len(values)) % tuple(values)
            + ");"
        )
        # Check
        # print(query)
        self._open()
        self.cursor.execute(query)
        self.connection.commit()
        self._close()

        return self.cursor.lastrowid

    # -----------------------------------------------------------------
    def select(self, column_s: str, table: str, condition: str) -> list:
        """Select the column(s) from table with condition(s).

        Args:
            column_s (str): Contains correct column name(s) which you
                want data from.
            table (str): Name of the table which data will be
                read from it.
            condition (str): Contains condition(s) which will filter
                the result.
        Returns:
            list: List of gotten data(empty list if there is none).
        """

        query = f"SELECT {column_s} FROM `{table}` "
        if condition:
            query += f"WHERE {condition};"
        else:
            query += ";"
        # Check
        # print(query)
        self._open()
        self.cursor.execute(query)
        result = list(self.cursor.fetchall())
        self._close()
        return result

    # -----------------------------------------------------------------
    def update(self, table: str, condition: str, **kwargs) -> None:
        """Update"""
        query = f"UPDATE `{table}` SET "
        for key, value in kwargs.items():
            query += f"`{str(key)}` = {value},"
        query = query[:-1]  # To exclude last comma.
        query += f" WHERE {condition};"
        # Check
        # print(query)
        self._open()
        self.cursor.execute(query)
        self.connection.commit()
        self._close()

    # -----------------------------------------------------------------
    # def complex_query(self, query: str) -> None:
    #     """Use for complex queries"""
    #     self._open()
    #     self.cursor.execute(query)
    #     self.connection.commit()
    #     self._close()


# End of class Model --------------------------------------------------
