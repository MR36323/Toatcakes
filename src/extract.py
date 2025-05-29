from utils.fetch_data import make_connection,close_connection,get_data

def lambda_handler(event, context):
    
    conn = make_connection()
    tables = ['counterparty','currency','department','design',
              'staff','sales_order','address','payment',
              'purchase_order','payment_type', 'transaction']
    
    for table in tables:
        query = f"SELECT * FROM {table}"
        result = get_data(conn, query, table)
     
    close_connection(conn)

lambda_handler({},{})