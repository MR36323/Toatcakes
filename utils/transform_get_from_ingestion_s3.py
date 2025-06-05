from botocore.exceptions import ClientError

def get_data(table_name: str) -> str:
    """Fetches data of table from ingestion zone.

    Args:
      table_name: A string representing the table name.

    Returns:
      A json-complient string of data from table.

    Raises:
      botocore.exceptions.ClientError. 
    """
    pass
