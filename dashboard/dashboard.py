import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# load data 
@st.cache_data
def loaddata(filepath):
    data = pd.read_csv(filepath)
    data["dteday"] = pd.to_datetime(data["dteday"])
    return data

data = loaddata("./data/day.csv")

# create title 
st.title('Dashboard')

st.sidebar.header("select day ranges")

startdate = st.sidebar.date_input('startdate',data['dteday'].min())
enddate = st.sidebar.date_input('startdate',data['dteday'].max())

startdate = pd.to_datetime(startdate)
enddate = pd.to_datetime(enddate)
filterdata = data[(data['dteday'] >= startdate) & (data['dteday'] <= enddate)]
st.write('### rawdata')
st.write(filterdata.head())

# visualisasi data 
st.write('### Apakah Cuaca Mempengaruhi Jumlah Pengguna Sepeda ?')
plt.figure(figsize=(8,4))
data_weathersit = filterdata.groupby('weathersit')['cnt'].sum().sort_values(ascending=False)
plt.bar(data_weathersit.index, data_weathersit.values,tick_label=['Cerah','Mendung','Salju'], color=['orange', 'grey','blue'])
plt.title('Jumlah Pengguna Sepeda Berdasarkan Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)

# visualisasi data 2 
st.write('### Bulan apa penyewaan sepeda paling tertinggi ?')
plt.figure(figsize=(8,4))
filterdata['month_name'] = filterdata['dteday'].apply(lambda x: x.strftime('%b'))
data_viz = filterdata.groupby(["mnth","month_name"])[["cnt"]].mean().reset_index()
plt.figure(figsize=(13,8))
plt.plot(data_viz["month_name"],
         data_viz["cnt"],
         marker="o",
         markersize=9,
         color="#90CAF9",
         linewidth=3,)
plt.title("Average Bike Rented Every Month")
plt.xlabel("Month", fontsize="x-large")
plt.ylabel("Count of rented bikes", fontsize="x-large")
st.pyplot(plt)

st.write("### Conclusion")
st.write("""##### Rekomendasi :
Berdasarkan analisis yang sudah dilakukan, dapat direkomendasikan:
1. Optimalisasi Stok Sepeda:
   - Menambahkan stok sepeda pada Season Summer: memastikan stok sepeda yang tersedia pada bulan Mei-Sep dapat memenuhi demand yang tinggi. Opsi penambahan ini bisa berupa penambahan jumlah sepeda pada setiap titik peminjamannya ataupun menjalin kerjasama seasonal dengan partner.
   - Mengurangi stok sepeda pada Season Winter : dengan demand yang rendah pada Season Winter, pengurangan stok sepeda yang dapat dipinjam akan mengurangi biaya maintenance dan storage yang berlebih. Selain itu, pada saat Season Winter berlangsung perusahaan dapat memprioritaskan maintenance sepeda-sepeda yang ditarik stoknya agar dapat digunakan pada Peak Season berikutnya.  
2. Seasonal Marketing Campaign:
   - Summer Promotions: Melakukan campaign secara aggresive pada Season Spring dengan menargetkan customer local dan tourist untuk mempersiapkan Season Summer. Menawarkan diskon ataupun bundles yang menarik untuk meningkatkan angka peminjaman sepeda
   - Targeted Fall Campaign: Meskipun rata-rata peminjaman pada Season Fall perlahan menurun, perusahaan dapat melakukan campaign dengan tema Season Fall untuk memberikan vibes nature sebelum memasuki Season Winter.
""")
