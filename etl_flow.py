from prefect import flow, task
from dwh_models import User,Product,Order,ps_engine


@task
def extract(**kwargs ):
    import polars as pl 
    uri = 'mysql://root:mysql@localhost:3307/divistant'
    query = f"select * from {kwargs['table']}"
    df = pl.read_database_uri(query,uri).lazy()
    return df 


@task
def transform(**kwargs):
    df = kwargs['df']
    df= df.unique().drop_nulls()
    return df
    
    
@task
def normalize(**kwargs):
    df = kwargs['df']
    s_col = kwargs['s_col']
    t_col = kwargs['t_col']
    product = df.select(s_col).unique().with_row_index('id',offset=1)
    df_merge = df.join(product,on = s_col, how = 'left').rename({'id_right':t_col,'Users':'UserId'})
    return product, df_merge
    
    
@task
def load(**kwargs):
    from sqlalchemy import insert
    df = kwargs['df'].collect().to_dicts()
    table = kwargs['table']
    with ps_engine.connect() as conn:
        try:
            conn.execute(insert(table),df)
        except Exception as e:
            print(e.orig)
        conn.commit()


@flow(retries = 0, retry_delay_seconds = 0, log_prints = False)
def etl():
    tables = ['OrdersId','Orders']
    for i in tables:
        if i != 'Orders':
             df_users = transform.submit(df=extract.submit(table = i))
        else:
            df_product,df_orders = normalize.submit(
                df = transform.submit(df=extract.submit(table = i))
                ,s_col = 'ProductName',
                t_col = 'Productid'
            ).result()
            
    t_tables = [
        {
            'table': User,
            'df' : df_users 
        },{
            'table': Product,
            'df': df_product
        }
    ]
    
    for i in t_tables:
        load.submit(df = i['df'],table = i['table'])
    
    load(df = df_orders,table = Order)
    
    
if __name__ == '__main__':
    etl.serve(
        name = 'Extract-Transform-Load-1',
    )