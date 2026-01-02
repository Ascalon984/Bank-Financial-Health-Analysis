Bagian ini memaparkan sejumlah fungsi bahasa pemprogaman Python yang secara mutakhir digunakan untuk kebutuhan analisis data.
Melalui sejumlah proses yang meliputi persiapan data, pemprosesan data mentah hingga insight secara profesional.

#--- TAHAP PERSIAPAN DAN PEMBERSIHAN DATA ---#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

df=pd.read_excel(r'C:\Users\Users\Downloads\Data.xlsx')                         # Ekstrak Dataset tipe excel


# 1. Cleaning Data / Preprocessing Data

## Deskripsi
Menghapus spasi tersembunyi dan menyederhanakan nama kolom untuk mencegah error pada tahap pemrosesan data selanjutnya.

### Implementasi Kode
                                                                
df.columns = df.columns.str.strip()                                             # Menghapus spasi tersembunyi di awal atau akhir nama kolom

df = df.rename(columns={'Total Modal': 'Modal'})                                # Mengubah nama kolom yang panjang menjadi lebih sederhana agar mudah dipanggil


# 2. Pembersihan dan Standarisasi Data

## Deskripsi
Menggunakan Regex untuk menghapus atribut hukum (PT/Tbk) agar tampilan nama objek lebih bersih dan ringkas tanpa mengubah esensi informasi.

### Implementasi Kode

df['Bank'] = (df['Bank'].str.replace(r'^PT\s+', '', regex=True, case=False)     # Menghapus 'PT' di awal, 'Tbk' di akhir, dan merapikan spasi agar tersisa nama inti bank
                        .str.replace(r'\s+Tbk$', '', regex=True, case=False)
                        .str.strip())


# 3. Penanganan Data Kosong

## Deskripsi
Menjaga akurasi analisis melalui penghapusan baris tanpa informasi kunci dan pengisian nilai nol pada kolom tertentu untuk menjamin kelancaran perhitungan statistik.

### Implementasi kode

df = df.dropna(subset=['TA', 'Kredit', 'Modal'])                                # Strategi A: Menghapus baris jika kolom keuangan utama (TA, Kredit, Modal) kosong

df['Kredit'] = df['Kredit'].fillna(0)                                           # Strategi B: Mengisi nilai kosong dengan angka 0 agar tidak menyebabkan error saat perhitungan


# 4. Optimasi Tipe Data (Data Type Optimization)

## 4.a Deskripsi
Memastikan setiap kolom memiliki format yang sesuai (numerik atau string) secara otomatis guna meningkatkan stabilitas sistem, efisiensi memori, dan mencegah kesalahan kalkulasi matematis.

### 4.b Implementasi kode
df = df.convert_dtypes()                                                        # Mengonversi seluruh tipe data dalam DataFrame secara otomatis ke format yang paling tepat


#--- TAHAP ANALISIS DATA ---#
# 5. Fungsi Pencarian Data Multi Kriteria

# 5.a Deskripsi
Fungsi pencarian dinamis yang menyaring data berdasarkan nama entitas (insensitif huruf) dan periode tahun untuk mengambil nilai spesifik pada kolom yang diinginkan secara instan.

# 5.b Implementasi Kode
def xlookup(bank, kolom, periode):                                              # Mendefinisikan fungsi dengan parameter pencarian
    objek=df[df['Bank'].str.contains(bank, case=False)]                         # Mencari nama bank yang mengandung kata kunci (tidak peka huruf besar/kecil)

    if objek.empty:                                                             # Memeriksa jika hasil pencarian bank kosong
        return f'Data {bank} tidak ditemukan'                                   # Mengembalikan pesan error jika bank tidak ada di dataframe

    if periode is not None:                                                     # Mengecek apakah parameter periode (tahun) diisi atau tidak
        objek=objek[objek['Tahun']==periode]                                    # Menyaring data lebih spesifik berdasarkan tahun yang ditentukan
    
    return objek[kolom].iloc[0]                                                 # Mengambil nilai pertama yang ditemukan pada kolom yang dituju

# 5.c Eksekusi kode
print(xlookup('Bank Mega', 'ROA', 2023))                                        # Memanggil fungsi dan menampilkan hasil ROA Bank Mega tahun 2023


# 6. Klasifikasi Otomatis dengan Nested Logic

# 6.a Deskripsi
Fungsi ini mereplikasi logika **Nested IF** untuk melakukan klasifikasi otomatis terhadap objek data string. 
Sistem akan mengevaluasi nilai pencarian dan memberikan label tertentu.

### Implementasi Kode
def if_kategori(kolom):                                                     # Mendefinisikan fungsi untuk mengelompokkan data berdasarkan nilai
    data = df[kolom].values                                                 # Mengambil semua nilai dari kolom yang dipilih menjadi sebuah list/array
    hasil = []                                                              # Menyiapkan list kosong untuk menampung hasil kategori

    for nilai in data:                                                      # Melakukan perulangan (looping) untuk mengecek setiap nilai satu per satu
        if nilai >= 1.5:                                                    # Logika pertama: jika nilai 1.5 ke atas
            hasil.append('Sangat Sehat')                                    # Masukkan kategori 'Sangat Sehat' ke dalam list
        elif nilai >= 1.25:                                                 # Logika kedua: jika nilai antara 1.25 sampai 1.49
            hasil.append('Sehat')                                           # Masukkan kategori 'Sehat'
        elif nilai >= 0.5:                                                  # Logika ketiga: jika nilai antara 0.5 sampai 1.24
            hasil.append('Cukup Sehat')                                     # Masukkan kategori 'Cukup Sehat'
        elif nilai >= 0.0:                                                  # Logika keempat: jika nilai antara 0.0 sampai 0.49
            hasil.append('Kurang Sehat')                                    # Masukkan kategori 'Kurang Sehat'
        else:                                                               # Logika terakhir: jika nilai di bawah 0 (negatif)
            hasil.append('Tidak Sehat')                                     # Masukkan kategori 'Tidak Sehat'

    return hasil                                                            # Mengembalikan daftar kategori yang sudah selesai diproses

df['Kesehatan'] = if_kategori('ROA')                                        # Membuat kolom baru 'Kesehatan' di DataFrame berdasarkan hasil fungsi
temuan = df[['Bank', 'ROA', 'Tahun', 'Kesehatan']]                          # Memilih kolom tertentu untuk ditampilkan dalam laporan ringkas

if not temuan.empty:                                                        # Mengecek apakah ada data yang tersedia untuk ditampilkan
    print(tabulate(temuan, headers='keys', tablefmt='pretty', 
    showindex=False))                                                       # Menampilkan tabel dengan format kotak (pretty) yang rapi
else:                                                                       # Debugging Jika DataFrame kosong
    print('Data tidak ditemukan')                                           # Menampilkan pesan peringatan bahwa data kosong


# 7. Diagnosa Data Spesifik Kombinasi Xlookup dan Nested Logic

# 7.a Deskripsi
Fungsi ini menggabungkan pencarian data dan logika Nested IF untuk menilai satu objek secara instan. 
Sistem menyaring data berdasarkan nama serta tahun, lalu memberikan label kategori otomatis berdasarkan nilai yang ditemukan.

# 7.b Implementasi Kode

def if_spesifik(bank, kolom, tahun=None):                                   # Membuat fungsi pencarian sekaligus penilaian kategori
    data = df[df['Bank'].str.contains(bank, case=False)]                    # Mencari data bank tertentu (tidak peka huruf besar/kecil)

    if data.empty: # Jika nama bank tidak ada dalam daftar
        return f'Bank {bank} tidak ditemukan'                               # Memberikan laporan bahwa bank tidak terdaftar
    
    if tahun is not None: # Jika parameter tahun diisi
        data = data[data['Tahun'] == tahun]                                 # Menyaring data agar hanya menampilkan tahun yang diminta
    
    variabel = data[kolom].iloc[0]                                          # Mengambil satu angka spesifik dari hasil pencarian

                                                                            # Bagian di bawah ini mengevaluasi angka yang ditemukan ke dalam kategori teks
    if variabel >= 1.5:                                                     # Jika angka 1.5 atau lebih
        return 'Sangat Sehat'
    elif variabel >= 1.25:                                                  # Jika angka 1.25 sampai 1.49
        return 'Sehat'
    elif variabel >= 0.5:                                                   # Jika angka 0.5 sampai 1.24
        return 'Cukup Sehat'
    elif variabel >= 0.0:                                                   # Jika angka 0.0 sampai 0.49
        return 'Kurang Sehat'
    else:                                                                   # Jika angka di bawah 0 (negatif)
        return 'Tidak Sehat'

# 7.c Eksekusi kode
print(if_spesifik('Bank Mega', 'ROA', 2023))                                # Menampilkan hasil akhir kategori kesehatan Bank Mega tahun 2023

##--- TAHAP OPTIMASI DAN PELAPORAN DATA
# 8. Vektorisasi Data Sederhana

# 8.a Deskripsi
Fungsi ini menerapkan logika Binary Classification menggunakan teknik vektorisasi. 
Sistem mengevaluasi seluruh kolom secara instan untuk memisahkan data ke dalam dua kategori utama berdasarkan ambang batas tertentu
.Serta merangkum total frekuensi setiap label secara otomatis.

# 8.b Implementasi Kode
def vektorisasi(kolom):
    return df[kolom].values                                                 # Mengonversi kolom DataFrame menjadi array NumPy

data = vektorisasi('ROA')                                                   # Mengambil data nilai ROA
                                                                            # Melakukan pelabelan instan: 'Sangat Sehat' jika >= 1.5, selain itu 'Sehat'
kondisi = np.where(data >= 1.5, 'Sangat Sehat', 'Sehat')    

jumlah = np.unique(kondisi, return_counts=True)                             # Menghitung total kemunculan setiap label yang dihasilkan
                                                            
frekuensi = dict(zip(*jumlah))                                              # Menggabungkan hasil perhitungan ke dalam format dictionary (Ringkasan Frekuensi)

# 8.c Eksekusi kode
print(frekuensi)            


# 9. Vektorisasi Data Secara Massal

# 9.a Deskripsi
Fungsi ini menggunakan teknik Vektorisasi untuk memproses ribuan baris data secara serentak tanpa perulangan (looping). 
Sistem melakukan pelabelan otomatis berdasarkan kriteria tertentu dan langsung merangkum total statistik setiap kategori dalam bentuk ringkasan laporan (dictionary).

# 9.b Implementasi Kode
def vektorisasi(kolom):
    data = df[kolom].values                                             # Mengambil data kolom sebagai array untuk proses cepat
    kondisi = [                                                         # Menyusun daftar aturan penilaian angka
        (data >= 1.5),
        (data >= 1.25),
        (data >= 0.5),
        (data >= 0.0),
        (data < 0.0)
    ]
    kesehatan = [                                                       # Menyusun daftar label teks sebagai hasil klasifikasi
        'Sangat Sehat', 'Sehat', 'Cukup Sehat', 
        'Kurang Sehat', 'Tidak Sehat'
    ]
    
    kategori = np.select(kondisi, kesehatan, default='Gagal Pelabelan') # Memberikan label ke seluruh data secara instan berdasarkan kondisi
    
    jumlah = np.unique(kategori, return_counts=True)                    # Menghitung total kemunculan setiap kelompok label kesehatan
    
    return dict(zip(*jumlah))                                           # Menggabungkan hasil statistik ke dalam format ringkas

# 9.c Eksekusi Kode
print(vektorisasi('ROA))                                                # Menampilkan ringkasan total kesehatan dari kolom tertentu


# 10. Analisis Peringkat Teratas Secara Umum

# 10.a Deskripsi
Fungsi ini dirancang untuk melakukan pemeringkatan data secara otomatis berdasarkan kriteria tertentu. 
Sistem mengurutkan data dari nilai tertinggi, mengambil 10 entitas teratas, dan menyusunnya ke dalam tabel laporan yang rapi lengkap dengan penomoran urut.

# 10.c Implementasi Kode
def top_general(kolom):
                                                                        # Mengurutkan data dari nilai terbesar ke terkecil dan mengambil 10 baris pertama
    data = df.sort_values(by=kolom, ascending=False).head(10)
    
    if data.empty:                                                      # Mengecek jika data tidak tersedia
        return None
    
    data = data.reset_index(drop=True)                                  # Mengatur ulang indeks agar bersih
                                                            
    data.insert(0, 'No', range(1, len(data) + 1))                       # Membuat kolom nomor urut (1-10) untuk tampilan peringkat
    
    return data[['No', 'Bank', 'Tahun', kolom]]                         # Mengembalikan kolom pilihan untuk laporan

target = top_general('ROA')                                             # Membuat peringkat berdasarkan nilai ROA

if target is not None:
                                                                        # Menampilkan tabel peringkat dengan format visual yang profesional
    print(tabulate(target, headers='keys', tablefmt='pretty', showindex=False))
else:
    print('Gagal Memproses Data')                                             # Pesan jika proses gagal


# 11. Pemeringkatan Kinerja Berbasis Periode Secara Unik

# 11.a Deskripsi
Fungsi ini digunakan untuk menyusun peringkat 10 besar performa tiap bank dengan fleksibilitas pemilihan tahun. 
Sistem melakukan penyaringan periode, pengurutan nilai tertinggi, serta pembulatan angka desimal untuk menghasilkan laporan yang lebih presisi dan mudah dianalisis.

# 11.b Implementasi kode
def top_kinerja_unik(kolom, tahun=None):
    if tahun is not None:                                               # Jika tahun ditentukan
        data = df[df['Tahun'] == tahun].copy()                          # Filter data berdasarkan tahun tersebut
    else:
        data = df.copy()                                                # Jika tidak, gunakan seluruh data yang ada
                 
    data = data.sort_values(by=kolom, ascending=False).head(10)         # Mengurutkan data dari nilai tertinggi dan mengambil 10 besar
    data = data.reset_index(drop=True)                                  # Merapikan urutan indeks data
    data.insert(0, 'Nomor', range(1, len(data) + 1))                    # Menambahkan kolom nomor urut peringkat
    
    return data[['Nomor', 'Bank', 'Tahun', kolom]]                      # Menampilkan kolom informasi utama

variabel = top_kinerja_unik('ROE').round(1)                             # Menjalankan fungsi untuk ROE dan membulatkan hasil ke 1 angka di belakang koma

if variabel is not None:                                                # Menampilkan tabel peringkat profesional menggunakan format 'pretty'
    print(tabulate(variabel, headers='keys', tablefmt='pretty', showindex=False))
else:
    print('Gagal tabulasi')


# 12. Visualisasi Kinerja Teratas dengan Grafik Batang (Bar Chart)

# 12.a Deskripsi
Fungsi ini dirancang untuk menciptakan laporan visual yang informatif mengenai 10 bank dengan kinerja tertinggi pada tahun tertentu. 
Selain menampilkan grafik, sistem secara otomatis menghitung nilai rata-rata sebagai pembanding serta menambahkan label angka langsung di atas batang grafik untuk memudahkan pembacaan data.

# 12.b Implementasi
def top_kinerja(kolom, tahun=None):
    data = df[df['Tahun'] == tahun]                                     # Menyaring data berdasarkan tahun terpilih
                                                                        # Mengelompokkan data per bank dan mengambil 10 nilai tertinggi
    grup = data.groupby('Bank')[kolom].sum().sort_values(ascending=False).head(10)
    
    tema = plt.cm.tab20(range(len(grup)))                               # Menyiapkan variasi warna grafik yang profesional
    rata2 = grup.mean()                                                 # Menghitung nilai rata-rata dari 10 bank teratas
    
    plt.figure(figsize=(12, 6.5), facecolor='aliceblue')                # Mengatur ukuran dan warna latar belakang grafik
    plt.bar(grup.index, grup.values, color=tema)                        # Membuat grafik batang dengan warna-warni

    for i, v in enumerate(grup.values):                                 # Menambahkan label nilai persentase di tengah setiap batang grafik
        nominal = '{:,.2f}%'.format(v).replace(',', '.')                # Format angka ke dalam persentase (Gaya Indonesia)
        plt.text(i, v/2, nominal, color='white', fontweight='bold', va='center', ha='center')
    
    plt.ylabel('Persen')                                                # Memberi label pada sumbu Y
    plt.xlabel('Daftar Bank')                                           # Memberi label pada sumbu X
    plt.title(f'Laporan Kinerja {kolom} pada {tahun}')                  # Menambahkan judul laporan grafik
    plt.axhline(rata2, linestyle='--', color='red', label=f'Rata-Rata: {rata2:.2f}') # Garis rata-rata
    plt.xticks(rotation=15)                                             # Memutar nama bank agar tidak saling bertumpukan
    plt.grid(True, linestyle='-', alpha=0.3)                            # Menambahkan garis bantu tipis pada latar belakang
    plt.show()                                                          # Menampilkan grafik akhir

top_kinerja('ROA', 2023)                                                # Menghasilkan visualisasi ROA untuk tahun 2023



