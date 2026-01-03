import pandas as pd
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_excel(r'C:\Users\User\Downloads\Customer-Purchase-History.xlsx', sheet_name='Sheet1')

# TAHAP CLEANING DATA

# cek missing value kolom dataframe
# print(df.isnull().sum())

# cek tipe data dataframe
df=df.convert_dtypes()
# print(df.dtypes)

# cek list kolom dataframe
# print(df.columns.tolist())

# hapus value kolom missing jika ada
df=df.dropna(subset=['CustomerID', 'Product', 'PurchaseDate', 'Quantity', 'UnitPrice', 'CustomerName', 'ProductCategory', 'PaymentMethod', 'ReviewRating', 'TotalPrice'])

# Mengubah header kolom
# df.rename(columns={'CustomerID': 'ID_Pelanggan', 'Product': 'Produk', 'PurchaseDate': 'Tanggal_Pembelian',
#                  'Quantity': 'Kuantitas', 'UnitPrice': 'Harga_Per_Unit', 'CustomerName': 'Nama_Pelanggan',
#                   'ProductCategory': 'Kategori_Produk', 'PaymentMethod': 'Metode_Pembayaran',
#                    'ReviewRating': 'Peringkat_Ulasan', 'TotalPrice': 'Total_Harga'}, inplace=True)

# TAHAP ANALISIS DATA

# Menganalsis banyaknya pembelian kategori produk berdasarkan metode pembayaran
def customer(id, column):
    data=df[df['PaymentMethod'].str.contains(id, case=False, na=False)]

    if data.empty:
        return None
    return data[column].value_counts()
# print(customer('Cash', 'ProductCategory'))

# Menganalisis peringkat pembelian kategori produk berdasarkan id customer
def top_sales(column):
    data=df.sort_values(column, ascending=False).head(20)
    if data.empty:
        return None
    data=data.reset_index(drop=True)
    data.insert(0, 'No', range(1, len(data)+1))
    return data[['No', 'CustomerID', 'ProductCategory', column]]
# sumber=top_sales('Quantity')
# if sumber is not None:
#     print(tabulate(sumber, headers='keys', tablefmt='pretty', showindex=False))
# else:
#     print('None')

# Analisis popularitas metode pembayaran
def search(column):
    return df[column].value_counts()
# print(search('PaymentMethod'))

# Analisis prioritas customer berdasarkan total harga dan rating
conditions=[
    (df['TotalPrice']>= 3000) & (df['ReviewRating'] >= 4),
    (df['TotalPrice']>= 1000) & (df['TotalPrice'] <= 3000),
    (df['TotalPrice'] <1000)
]
criteria=['High Priority', 'Standard', 'Low Priority']
df['Clasification']=np.select(conditions, criteria, default='Excluded')
# print(df[['CustomerID', 'TotalPrice', 'ReviewRating', 'Clasification']].head(20))

# Analisis labelisasi kriteria review rating interval 1-5 dengan nested logic
def condition(column):
    data=df[column].values
    result=[]

    for x in data:
        if x == 1:
            result.append('Very Poor')
        elif x ==2:
            result.append('Dissatisfied')
        elif x ==3:
            result.append('Neutral')
        elif x ==4:
            result.append('Satisfied')
        else:
            result.append('Exceptional')
    return result
# df['Status']=condition('ReviewRating')
# display=df[['CustomerID', 'ProductCategory', 'ReviewRating', 'Status']].head(20)
# if not display.empty:
#     print(tabulate(display, headers='keys', tablefmt='pqsql', showindex=False))
# else:
#     print('Invalid Table')

# Analisis hitung jumlah kriteria review rating interval 1-5 dengan nested logic
def calc(column):
    data=df[column].values
    condition=[
        (data == 5),
        (data == 4),
        (data == 3),
        (data == 2),
        (data == 1)
    ]
    status=['Exceptional', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Poor']
    choose=np.select(condition, status, default='Excluded')
    quantity=np.unique(choose, return_counts=True)
    return dict(zip(*quantity))
# print(calc('ReviewRating'))


# Tren total penjualan dengan matplotlib
def trend(column, date):
    key=df[df['PurchaseDate']==date]
    data=key.groupby(['PurchaseDate', 'ProductCategory'])[column].sum().unstack()
    plt.figure(figsize=(10,5))
    data.plot(kind='line', marker='o', ax=plt.gca())
    plt.ylabel("$")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.title(f'Trend Sales {column}')
    plt.xticks(rotation=35)
    plt.show()
trend('TotalPrice')
    