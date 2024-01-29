# Import all necessary libraries
from prefect import flow, task
from dwh_models import User,Product,Order,ps_engine

# Define tasks
@task
def extract(**kwargs ):
    """The extract function uses polars \n
    to read source database and convert the data to LazyFrame then return it.

    Returns:
        polars.LazyFrame: source table
    """
    import polars as pl 
    
    # Define uri
    uri = 'mysql://root:mysql@localhost:3307/divistant'
    
    # Define query
    query = f"select * from {kwargs['table']}"
    
    # Convert to LazyFrame
    df = pl.read_database_uri(query,uri).lazy()
    return df 

@task
def transform(**kwargs):
    """The transform function manages to clean data from duplicated dan null values.\n
    Additionally, map gender to english if any.

    Returns:
        polars.LazyFrame: transformed data
    """
    import polars as pl 
    
    # Grab the kwargs value and store it to variable
    df = kwargs['df']
    
    # Drop duplicated and null values
    df= df.unique().drop_nulls()
    
    # Execute code if kwargs has gender and it is dict data type and it is not blank dict
    if 'gender' in kwargs and type(kwargs['gender']) == dict and kwargs['gender'] != {}:
        # Defin variable gender
        gender = kwargs['gender']
        
        # Replace gender value to new gender value
        df = df.with_columns(pl.col('Gender').replace(gender))
    return df
    
    
@task
def normalize(**kwargs) -> tuple:
    """The normalize functions manages to normalize function to 1NF, 2NF

    Returns:
        tuple: Contains 2 polars.LazyFrame
    """
    
    # Define variables
    df = kwargs['df']
    s_col = kwargs['s_col']
    t_col = kwargs['t_col']
    
    # Retrieve given source col and drop duplicates then set the index start from 1
    product = df.select(s_col).unique().with_row_index('id',offset=1)
    
    # Self join to normalize source col
    df_merge = df.join(product,on = s_col, how = 'left').rename({'id_right':t_col,'Users':'UserId'})
    return product, df_merge
    
    
@task
def load(**kwargs) -> None:
    """The load function manages to execute LazyFrame to DataFrame and transform it to dict data type \n
    then load it to Target table in Data Warehouse
    """
    from sqlalchemy import insert
    
    # Execute LazyFrame to DataFrame then to dict data type
    df = kwargs['df'].collect().to_dicts()
    
    # Define variable table
    table = kwargs['table']
    
    # Open Connection
    with ps_engine.connect() as conn:
        try:
            # Insert Table
            conn.execute(insert(table),df)
        except Exception as e:
            # Print the error
            print(e.orig)
        # Commit the transactions
        conn.commit()

# Define Flow
@flow(retries = 0, retry_delay_seconds = 0, log_prints = False)
def etl() -> None:
    """The etl function as a flow manages to execute all task in correct order and concurrancy.
    """
    
    # Define source tables
    tables = ['OrdersId','Orders']
    
    # Loop through each table
    for i in tables:
        # if the table is Orders
        if i != 'Orders':
            # Execute sequence of tasks extract >> transform
             df_users = transform.submit(df=extract.submit(table = i), gender = {'Laki-laki':'Male','Perempuan': 'Female'})
        else:
            # If not then execute the sequence of tasks extract >> transform >> normalize then unpack the result to 2 LazyFrame
            df_product,df_orders = normalize.submit(
                df = transform.submit(df=extract.submit(table = i))
                ,s_col = 'ProductName',
                t_col = 'Productid'
            ).result()
    
    # Define models and their LazyFrames
    t_tables = [
        {
            'table': User,
            'df' : df_users 
        },{
            'table': Product,
            'df': df_product
        }
    ]
    
    # Loop through defined variable
    for i in t_tables:
        # Load dimantional table to Data Warehouse concurrancy
        load.submit(df = i['df'],table = i['table'])
    
    # Load fact table to Data Warehouse after dimentional table
    load(df = df_orders,table = Order)
    
    
if __name__ == '__main__':
    # Deploy the flow
    etl.serve(
        name = 'Extract-Transform-Load-1',
    )