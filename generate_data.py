# %%
import numpy as np
import polars as pl

# %%
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



# %%
gender = np.array(['Perempuan']*10 + ['Laki-laki']* 10)
gender

# %%
pahlawan = ['Soekarno', 'Sudirman','Suparman','Hatta']
address = np.array([f'jl. {np.random.choice(pahlawan,1)[0]} No. {i+1}' for i in range(20)])
address

# %%
orderid_df = pl.DataFrame({'Name':users_name,'Gender':gender,'Address':address})
orderid_df=orderid_df.with_row_index('id',offset=1)

# %%
# orderid_df.write_csv('orderid.csv')

# %%
k = 5000

# %%
date_dum = np.array([f'{np.random.choice(np.arange(1,31),1)[0]}/12/2001' for _ in range(k)])

# %%
users = np.random.choice(np.arange(1,21),k,replace=True)
users

# %%
price = np.random.choice(np.arange(5,100,.1),k,replace=True)

# %%
quantity = np.random.choice(np.arange(2,30),k,replace=True)

# %%
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

# %%
orders = pl.DataFrame({'CreatedAt':date_dum,'Users':users,'ProductName':productName, 'Price':price,'Quantity':quantity})

# %%
orders_df = orders.with_columns((pl.col('Price')* pl.col('Quantity')).alias('TotalPrice'))

# %%
orders_df = orders_df.with_columns(pl.col('CreatedAt').str.to_date('%d/%m/%Y'))

# %%
# orders_df.write_csv('order.csv')


