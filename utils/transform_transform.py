import pandas as pd
from boto3 import client
import os
from dotenv import load_dotenv
import json 
from io import BytesIO

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
    staff_df = pd.DataFrame(staff)
    department_df = pd.DataFrame(department)
    dim_staff_df = pd.merge(staff_df,department_df,on='department_id')
    dim_staff_df = dim_staff_df.drop(['department_id','manager','created_at_x','last_updated_y','created_at_y','last_updated_x'],axis=1)
    return dim_staff_df

def create_dim_counterparty(counterparty: list, address: list) -> pd.DataFrame:
    """Create and populate new dimension counterparty table.

    Args:
      counterparty: Counterparty table in the form of a json listing.
      address: Address table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a counterparty dimension table.
    """
    counterparty_df = pd.DataFrame(counterparty)
    address_df = pd.DataFrame(address)
    dim_counterparty_df = pd.merge(counterparty_df,address_df,left_on='legal_address_id',right_on='address_id')
    dim_counterparty_df = dim_counterparty_df.drop(['address_id','legal_address_id','commercial_contact','delivery_contact','created_at_x','last_updated_y','created_at_y','last_updated_x',],axis=1)
    
    dim_counterparty_df.rename(columns={'address_line_1': 'counterparty_legal_address_line_1',
                                        'address_line_2':'counterparty_legal_address_line_2',
                                        'district':'counterparty_legal_district',
                                        'city':'counterparty_legal_city',
                                        'postal_code':'counterparty_legal_postal_code',
                                        'country':'counterparty_legal_country',
                                        'phone':'counterparty_legal_phone_number'}, inplace=True)
    return dim_counterparty_df

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
      Address: Address table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a location dimension table.
    """
    address_df = pd.DataFrame(address)
    dim_location_df = address_df.drop(['created_at', 'last_updated'], axis=1)
    dim_location_df.rename(columns={'address_id': 'location_id'}, inplace=True)
    return dim_location_df

def create_dim_date(sale_order: list) -> pd.DataFrame:
    """Create and populate new dimension date table.

    Args:
      Sale_order: Sale_order table in the form of a json listing.

    Returns:
      Pandas DataFrame object representing a sale_order dimension table.
    """
    pass

def create_fact_sales_order(sales_order: list, previous_df_json: list) -> pd.DataFrame:
    """Create and populate new fact sales_order table.

    Args:
      sales_order: Sales_order table in the form of a json listing.
      current_record: current highest record_id

    Returns:
      Pandas DataFrame object representing a fact sales_order table.
    """
    previous_df = pd.DataFrame(previous_df_json)
    if previous_df_json:
        previous_df = previous_df.drop(['sales_record_id'],axis=1)
    new_df = pd.DataFrame(sales_order)
    created_at_list = list(new_df['created_at'])
    new_df['created_date'] = [date_time.split(' ')[0] for date_time in created_at_list]
    new_df['created_time'] = [date_time.split(' ')[1] for date_time in created_at_list]
    last_updated_list = list(new_df['last_updated'])
    new_df['last_updated_date'] = [date_time.split(' ')[0] for date_time in last_updated_list]
    new_df['last_updated_time'] = [date_time.split(' ')[1] for date_time in last_updated_list]
    new_df = new_df.drop(['created_at', 'last_updated'], axis=1)
    new_df.rename(columns={'staff_id': 'sales_staff_id'}, inplace=True)
    fact_sales_df = pd.concat([previous_df, new_df],ignore_index=True)
    fact_sales_df.drop_duplicates(inplace=True,ignore_index=True)
    fact_sales_df['sales_record_id'] = range(1, len(fact_sales_df) + 1)
    fact_sales_df = fact_sales_df[['sales_record_id','sales_order_id','created_date' ,'created_time', 'last_updated_date','last_updated_time','sales_staff_id', 'counterparty_id', 'units_sold', 'unit_price', 'currency_id','design_id', 'agreed_payment_date' ,'agreed_delivery_date','agreed_delivery_location_id' ]]
    return fact_sales_df

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

# lambda_handler():
#     util gets most recent from tranform bucket as json converted to dataframe. get current      record id from key.
# create_fact_sales_order(sales_order, current_record, current_df) 

def get_latest_transformed_object_from_S3():
    load_dotenv()

    s3_client = client('s3')
    
    objects_response = s3_client.list_objects_v2(Bucket=os.environ.get('BUCKET'), Prefix='fact_sales_order')
    print(objects_response)
    if objects_response['KeyCount'] == 0:
        return None
    
    times_list = [obj['LastModified'] for obj in objects_response['Contents']]
    
    most_recent = max(times_list)
    most_recent_key = [obj['Key'] for obj in objects_response['Contents'] if obj['LastModified'] == most_recent][0]
    
    current_data = s3_client.get_object(Bucket=os.environ.get('BUCKET'), Key=most_recent_key)['Body'].read()
    return pd.read_parquet(current_data)

