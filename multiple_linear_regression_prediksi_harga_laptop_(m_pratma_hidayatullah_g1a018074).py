# -*- coding: utf-8 -*-
"""Multiple Linear Regression - Prediksi Harga Laptop (M. Pratma Hidayatullah G1A018074).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-eo0Xi99GmNd5PifhYq0xgXuLtQ1YkYL

#CONTOH KASUS
Aat tinggal dan belajar di eropa. Dia kurang ahli dalam membeli barang elektronik, tetapi dia ingin membeli Laptop seken untuk belajar, sehingga dia bertanya ke teman-teman nya, perangkat apa saja yang harus dimiliki laptop. dan akhirnya setelah banyak masukan Aat menarik kesimpulan spek minimum laptop yang ingin dia beli sebagai berikut:

*   Keluaran    = Asus
*   Ram         = 6 GB
*   OS          = Windows 10
*   Memory Size = 128 GB
*   SSD/HDD/Both= SSD
*   GPU         = AMD
*   CPU         = Intel core i7

Data harga Laptop dapat diambil dari dataset kaggle : 
https://www.kaggle.com/muhammetvarl/laptop-price

#Penyelesaian Kasus
Pada kasus kali ini, jika dilihat dari spek minimum yang diinginkan oleh Aat, kita dapat menggunakan metode Multiple Linear Regression, karena memiliki lebih dari satu variabel bebas.

* Variabel bebas yaitu Keluaran, RAM, OS, Memory Size, SSD/HDD/Both, GPU, dan CPU
* Variabel terikat yaitu harga laptop(euro)

Langkah Pengerjaan Menggunakan Python

Import Library yang akan digunakan :
"""

import re
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor,LinearRegression
from sklearn.model_selection import train_test_split

"""Panggil Dataset yang akan digunakan :"""

df = pd.read_csv("/content/laptop_price.csv", encoding = "ISO-8859-1", engine='python')
df

"""#Data understanding

Penjelasan atribut sebagai berikut :

* Company = Perusahan yang mengeluarkan Laptop
* Product = Model
* TypeName = Type (Notebook, Ultrabook, Gaming, etc.)
* Inches = Ukuran ayar
* ScreenResolution = Resolusi layar
* Cpu = Central Processing Unit (CPU) yang digunakan
* Ram = RAM laptop
* Memory = Hard Disk / SSD Memory
* GPU = Graphics Processing Units (GPU) yang digunakan
* OpSys = Operating System yang digunakan
* Weight = berat laptop
* Price_euros = Harga laptop(euro)

Melihat informasi dari data seperti jumlah data, tipe data, dsb.
"""

df.info()

"""Melihat data kita apakah memiliki missing values atau tidak"""

df.isnull().sum()

"""#Analisis data eksploratif
Kita tambah fitur untuk lebih mudah membaca data dan memahaminya
"""

df['Ram']=df['Ram'].str.strip('GB').astype(int)
df['Memory_size']=df['Memory'].apply(lambda x: re.sub(r'\.0|GB','',str(x).replace('TB','000')))
df['Memory_size']=df['Memory_size'].apply(lambda x: sum(int(re.search(r'\d+',s).group()) for s in x.split('+')))
df['Weight']=df['Weight'].str.strip('kg').astype(float)
df['Memory']=df['Memory'].astype(str)
df['SSD or Not or Both']=df.Memory.apply(lambda x: 'both' if 'SSD' in x and 'HDD' in x else 'Yes' if 'SSD' in x else 'No')
df['Gpu_company'] = df.Gpu.apply(lambda x: x.split(' ')[0])
df['Cpu_company']=df['Cpu'].str.split(' ', 1, expand=True)[0]
df['Cpu_type']=df['Cpu'].str.split(' ', 1, expand=True)[1].apply(lambda x: x.split(' ')[1] if x.split(' ')[0]=='Core' else x.split(' ')[0])
df

"""Buang data yang sekiranya tidak kita gunakan"""

df.drop(['Cpu','Weight','laptop_ID','Product','Inches','ScreenResolution','Memory','Gpu','TypeName'],inplace=True,axis=1)
df

"""Untuk mempermudah proses linier regression, maka kita perlu mengubah tipe data yang object menjadi int"""

le={}
for col in set(df.columns).difference({'Price_euros','Memory_size','Ram'}):
    le[col] = LabelEncoder()
    df[col]  = le[col].fit_transform(df[col])
df

"""Dapat dilihat data sudah berubah :"""

df.info()

"""#Analisis Univariat
Melihat distribusi dari Price_euros
"""

f = plt.figure(figsize=(12,4))

f.add_subplot(1,2,1)
sns.countplot(df["Price_euros"])

f.add_subplot(1,2,2)
plt.boxplot(df["Price_euros"])
plt.show()

"""Harga laptop dari data price_euros yang ada berkisar dari 0-2500 an

Banyak terdapat data outliers (Data yang menyimpang terlalu jauh)

Karena, data price_euros yang seharusnya menjadi harga acuan kita memiliki banyak data yang menyimpang. Maka, kita hapus data yang terdapat di outliers supaya data yang digunakan tidak memiliki penyimpangan yang berlebihan
"""

df=df.drop(df[df.Price_euros>2500].index)

"""Setelah itu kita lihat kembali distribusi dari price_euros, dapat dilihat tidak ada data pada outliers. Yang artinya tidak ada data yang menyimpang terlalu jauh"""

f = plt.figure(figsize=(12,4))

f.add_subplot(1,2,1)
sns.countplot(df["Price_euros"])

f.add_subplot(1,2,2)
plt.boxplot(df["Price_euros"])
plt.show()

"""#Analisis bivariat

Melihat hubungan antara variabel x dan variabel y
"""

plt.figure(figsize=(10,8))
sns.pairplot(data=df, x_vars=["Company","Ram","OpSys","Memory_size","SSD or Not or Both","Gpu_company","Cpu_company","Cpu_type"], y_vars=["Price_euros"], height=5, aspect=0.75)
plt.show()

"""Mengetahui nilai korelasi dari variabel x dan variabel y"""

df.corr().style.background_gradient().set_precision(2)

"""Dari tabel korelasi di atas; 
* Dapat dilihat bahwa Ram mempunyai hubungan linear positif yang sangat kuat dengan price_euros. Sedangkan,
* Memory_size memiliki nilai kolerasi mendekati nol yang menandakan bahwa ukuran memori tidak terlalu berpengaruh pada harga

#Modelling
"""

df.head()

"""1. buat variabel x dan y"""

x = df.drop(columns="Price_euros")
y = df["Price_euros"]

"""2. Bagi dataset menjadi 80% training & 20% testing (angka random yang digunakan adalah 5)"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

"""Check shape dari data training dan testing"""

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

"""3. Buat objek linear regresi"""

lin_reg = LinearRegression()

""" 4. Train model menggunakan data training yang sudah dibagi"""

lin_reg.fit(x_train, y_train)

"""5. Cari tau nilai koefisien (m) dan intercept (b)"""

print(lin_reg.coef_)
print(lin_reg.intercept_)

"""Buat ke dalam DataFrame"""

coef_dict = {
    "features": x.columns,
    "coef_value": lin_reg.coef_
}
coef = pd.DataFrame(coef_dict, columns=["features", "coef_value"])
coef

"""Dari nilai m dan b di atas, jika dimasukkan ke dalam rumus akan menjadi :

y = 7.789236 + 68.955081 + 66.886493 - 0.176918 + 143.114424 + 42.629682 - 177.492650 + 38.536322
"""

y_pred = lin_reg.predict(x_test)

"""6. Cari tau akurasi dari model yang telah kita buat menggunakan data testing"""

lin_reg.score(x_test, y_test)

"""Akurasi dari model yang telah kita buat yaitu 64.07%

# Prediksi

Prediksi harga laptop yang sesuai dengan spek minimum Aat :
*   Keluaran    = Asus
*   Ram         = 6 GB
*   OS          = Windows 10
*   Memory Size = 128 GB
*   SSD/HDD/Both= SSD
*   GPU         = AMD
*   CPU         = Intel core i7
"""

lin_reg.predict([[2,6, 5, 128, 1,0,1,17]])

"""Prediksi harga laptop yang sesuai dengan spek Aat adalah 986.85 euro"""