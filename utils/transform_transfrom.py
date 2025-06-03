import pandas as pd

'''
dim_staff -> staff, department
dim_counterparty -> counterparty, address
dim_currency -> currency, (currency_name use switch case)
dim_design -> design
dim_location -> address
dim_date -> sales_order
fact_sales_order -> sales_order


NOTE: to track latest sales record id, it might be easiest to store
      the id as a seperate object in the processed zone s3 bucket.
      We can then decide what to do with the tables in the bucket 
      each time we run the pipeline. But we do NOT clear the id; only 
      get_latest_sales_record_id() may do so, when it is time to 
      increment the sales records id.
'''

def create_dim_staff(staff: str, department: str) -> pd.DataFrame:
    """Create and populate new dimension staff table.

    Args:
      staff: Staff table in the form of a json string.
      department: Department table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a staff dimension table.
    """
    pass

def create_dim_counterparty(counterparty: str, address: str) -> pd.DataFrame:
    """Create and populate new dimension counterparty table.

    Args:
      counterparty: Counterparty table in the form of a json string.
      address: Address table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a counterparty dimension table.
    """
    pass

def create_dim_currency(currency: str) -> pd.DataFrame:
    """Create and populate new dimension currency table.

    Args:
      currency: Currency table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a currency dimension table.
    """
    pass

def create_dim_design(design: str) -> pd.DataFrame:
    """Create and populate new dimension design table.

    Args:
      Design: Design table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a design dimension table.
    """
    pass

def create_dim_location(address: str) -> pd.DataFrame:
    """Create and populate new dimension address table.

    Args:
      Address: Address table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a location dimension table.
    """
    pass

def create_dim_date(sale_order: str) -> pd.DataFrame:
    """Create and populate new sale_order address table.

    Args:
      Sale_order: Sale_order table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a sale_order dimension table.
    """
    pass

def create_fact_sales_order(sales_order: str) -> pd.DataFrame:
    """Create and populate new sales_order address table.

    Args:
      sales_order: Sales_order table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a fact sales_order table.
    """
    pass

def get_latest_sales_record_id() -> int:
    """Get the latest sales record id from processed zone bucket.

    Args: 
      None.

    Returns:
      Integer representing the latest sales_record_id.
    """
