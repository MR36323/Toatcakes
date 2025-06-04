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
      staff: Staff table in the form of a json string.
      department: Department table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a staff dimension table.
    """
    staff_df = pd.DataFrame(staff)
    department_df = pd.DataFrame(department)
    dim_staff_df = pd.merge(staff_df,department_df,on='department_id')
    dim_staff_df = dim_staff_df.drop(['department_id','manager','created_at_x','last_updated_y','created_at_y','last_updated_x'],axis=1)
    return dim_staff_df

def create_dim_counterparty(counterparty: list, address: list) -> pd.DataFrame:
    """Create and populate new dimension counterparty table.

    Args:
      counterparty: Counterparty table in the form of a json string.
      address: Address table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a counterparty dimension table.
    """
    counterparty_df = pd.DataFrame(counterparty)
    address_df = pd.DataFrame(address)
    dim_counterparty_df = pd.merge(counterparty_df,address_df,left_on='legal_address_id',right_on='address_id')
    dim_counterparty_df = dim_counterparty_df.drop(['address_id','legal_address_id','commercial_contact','delivery_contact','created_at_x','last_updated_y','created_at_y','last_updated_x',],axis=1)
    print(dim_counterparty_df)

def create_dim_currency(currency: str) -> pd.DataFrame:
    """Create and populate new dimension currency table.

    Args:
      currency: Currency table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a currency dimension table.
    """
    pass

def create_dim_design(design: list) -> pd.DataFrame:
    """Create and populate new dimension design table.

    Args:
      Design: Design table in the form of a list of data.

    Returns:
      Pandas DataFrame object representing a design dimension table.
    """
    design_df = pd.DataFrame(design)
    dim_design_df = design_df.drop(['created_at', 'last_updated'], axis=1)
    return dim_design_df

def create_dim_location(address: list) -> pd.DataFrame:
    """Create and populate new dimension address table.

    Args:
      Address: Address table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a location dimension table.
    """
    address_df = pd.DataFrame(address)
    dim_location_df = address_df.drop(['created_at', 'last_updated'], axis=1)
    dim_location_df.rename(columns={'address_id': 'location_id'}, inplace=True)
    return dim_location_df

def create_dim_date(sale_order: str) -> pd.DataFrame:
    """Create and populate new dimension date table.

    Args:
      Sale_order: Sale_order table in the form of a json string.

    Returns:
      Pandas DataFrame object representing a sale_order dimension table.
    """
    pass

def create_fact_sales_order(sales_order: str) -> pd.DataFrame:
    """Create and populate new fact sales_order table.

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

