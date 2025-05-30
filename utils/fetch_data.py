from pg8000.native import Connection
from pg8000.exceptions import InterfaceError, DatabaseError
import os
from dotenv import load_dotenv

def make_connection():
    """Connects to the database.

    Args:
      None.

    Returns:
      Pg8000 connection object.

    Raises:
      InterfaceError: If credentials are incorrect.
    """

    load_dotenv()
    try:
        conn = Connection(
            user=os.getenv("PG_USER"), 
            password=os.getenv("PG_PASSWORD"),
            database=os.getenv("PG_DATABASE"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        return conn
    except (InterfaceError, Exception) as e:
        print(f'An error occured: {e}')
        raise e

def close_connection(conn):
    """Closes connection to database.

    Args:
      conn: Pg8000 connection object.

    Returns:
      None.

    Raises:
      InterfaceError: When connection has been closed.
      AtrributeError: Argument is not connection object.
    """

    try:
        conn.close()
    except (AttributeError, InterfaceError, Exception) as e:
        print(f'An error occured: {e}')
        raise e

def zip_rows_and_columns(rows, columns):
    """Maps the data in rows and column names.

    Args:
      rows: All rows in table.
      columns: All column names in table.

    Returns:
      Dictionary with data from rows and columns are mapped.
    """
    return [dict(zip(columns, row)) for row in rows]

def get_data(conn, query, table_name):
    """Gets rows and columns from table in database.

    Args:
      conn: Pg8000 connection object.
      query: Selects all queries.
      table_name: Tables name.

    Returns:
      Dictionary with table name as key and data as value.

    Raises:
      DatabaseError: Table does not exist.
    """
    try:
        rows = conn.run(query)
        columns = [row['name'] for row in conn.columns]
        data = zip_rows_and_columns(rows, columns)
        return {table_name: data}
    except (DatabaseError, Exception) as e:
        print(f'An error occured: {e}')
        raise e