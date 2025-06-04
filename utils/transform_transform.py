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
      the id as a seperate object in the processed zone bucket.
      We can then decide what to do with the tables in the bucket 
      each time we run the pipeline. But we do NOT clear the id each time we
      run the pipeline; only get_latest_sales_record_id() may change this value,
      when it is time to increment the sales records id.
'''

def create_dim_staff(staff: list, department: list) -> pd.DataFrame:
    """Create and populate new dimension staff table.

    Args:
      staff: Staff table in the form of a json listing.
      department: Department table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a staff dimension table.
    """
    pass

def create_dim_counterparty(counterparty: list, address: list) -> pd.DataFrame:
    """Create and populate new dimension counterparty table.

    Args:
      counterparty: Counterparty table in the form of a json listing.
      address: Address table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a counterparty dimension table.
    """
    pass

def create_dim_currency(currency: list) -> pd.DataFrame:
    """Create and populate new dimension currency table.

    Args:
      currency: Currency table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a currency dimension table.
    """

    currency_name = {
        "GBP": "British pound sterling",
        "USD":  "United States dollar",
        "EUR":  "Euro"
    }

    dim_currency_df = pd.DataFrame(currency)
    dim_currency_df = dim_currency_df.drop(['created_at', 'last_updated'], axis=1)

    dim_currency_df['currency_name'] = dim_currency_df['currency_code'].map(currency_name)
    dim_currency_df = dim_currency_df.fillna("Unknown")
    
    return dim_currency_df



def create_dim_design(design: list) -> pd.DataFrame:
    """Create and populate new dimension design table.

    Args:
      Design: Design table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a design dimension table.
    """
    pass

def create_dim_location(address: list) -> pd.DataFrame:
    """Create and populate new dimension address table.

    Args:
      Address: Address table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a location dimension table.
    """
    pass

def create_dim_date(sale_order: list) -> pd.DataFrame:
    """Create and populate new dimension date table.

    Args:
      Sale_order: Sale_order table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a sale_order dimension table.
    """
    pass

def create_fact_sales_order(sales_order: list) -> pd.DataFrame:
    """Create and populate new fact sales_order table.

    Args:
      sales_order: Sales_order table in the form of a json listing.

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

    Raises:
      Exception.
    """

def update_latest_sales_record_id(sales_record_id: int):
    """Put the latest sales record id into processed zone bucket.

    Args: 
      sales_record_id: The latest sales record id.

    Returns:
      None.
    """

