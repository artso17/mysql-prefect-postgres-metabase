# %%
import numpy as np
import polars as pl

def generate_data(write):
    """ Some data gathered using Generative AI and some using logic that provided by Numpy
    """
    
    # Data generated by generative AI
    users_name = [
    'Lila Mccormick',
    'Kaitlyn Mccarthy',
    'Aubree Mcclain',
    'Maddison Mccormick',
    'Kamryn Mcclure',
    'Kaliyah Mccarthy',
    'Kinsley Mcclain',
    'Kira Mccarthy',
    'Kiana Mcclure',
    'Kyla Mccarthy',
    'Rylan Bruce',
    'Pablo Luis',
    'Vicente Elisha',
    'Kayden Conor',
    'Adriel Ean',
    'Zain Cassius',
    'Kaelin',
    'Kaelum',
    'Kaelan',
    'Kagan',
    ]

    # Data Generated using Numpy
    gender = np.array(['Perempuan']*10 + ['Laki-laki']* 10)

    pahlawan = ['Soekarno', 'Sudirman','Suparman','Hatta']
    address = np.array([f'jl. {np.random.choice(pahlawan,1)[0]} No. {i+1}' for i in range(20)])
    address

    orderid_df = pl.DataFrame({'Name':users_name,'Gender':gender,'Address':address})
    orderid_df=orderid_df.with_row_index('id',offset=1)

    # Number of data to be generated
    k = 5000

    date_dum = np.array([f'{np.random.choice(np.arange(1,31),1)[0]}/12/2001' for _ in range(k)])

    users = np.random.choice(np.arange(1,21),k,replace=True)


    price = np.random.choice(np.arange(5,100,.1),k,replace=True)

    quantity = np.random.choice(np.arange(2,30),k,replace=True)

    # Data generated by Generative AI
    parfumes = [
    'Scented Delight',
    'Whiff of Bliss',
    'Aroma Essence',
    'Fresh Blend',
    'Pure Bliss',
    'Scent Haven',
    'Fresh Petals',
    'Starlight Dreams',
    'Perfumed Poetry',
    'Flower Power',
    ]
    productName = np.random.choice(parfumes,k,replace = True)

    # Join all data to Data frame using polars
    orders = pl.DataFrame({'CreatedAt':date_dum,'Users':users,'ProductName':productName, 'Price':price,'Quantity':quantity})

    # Create column TotalPrice from Price and Quantity columns
    orders_df = orders.with_columns((pl.col('Price')* pl.col('Quantity')).alias('TotalPrice'))

    # Cast String to Date
    orders_df = orders_df.with_columns(pl.col('CreatedAt').str.to_date('%d/%m/%Y'))

    # Write data if True
    if write == True:
        orders_df.write_csv('order.csv')
        orderid_df.write_csv('orderid.csv')

if __name__ == '__main__':
    generate_data(False)