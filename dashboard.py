import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
seasons = ['Spring', 'Summer', 'Fall', 'Winter']

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.freevector.com/uploads/vector/preview/27655/rental3.jpg")
    
    # Mengambil start_date & end_date dari date_input untuk day_df
    start_date, end_date = st.date_input(
        label='Rentang Waktu (day_df)',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Mengambil start_date & end_date dari date_input untuk hour_df
    start_date_hour, end_date_hour = st.date_input(
        label='Rentang Waktu (hour_df)',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data day_df berdasarkan tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                     (day_df["dteday"] <= str(end_date))]

# Filter data hour_df berdasarkan tanggal
main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date_hour)) & 
                       (hour_df["dteday"] <= str(end_date_hour))]

st.title('Proyek Analisis Data: Bike Sharing Dataset')
# Menampilkan informasi nama, email, dan ID
st.write("**Nama:** Ramadhanul Husna  |  **Email:** danuldanul22@gmail.com  |  **ID Dicoding:** ramadhanul")

def visualize_seasonal_data(df):
    # Preprocessing data
    df['yr'] = df['yr'].replace({0: '2011', 1: '2012'})
    df['season'] = df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    # Menyiapkan data untuk plot
    seasonal_data = df.groupby(['season', 'yr'])['cnt'].sum().unstack()

    # Memvisualisasikan pola perilaku peminjaman sepeda berdasarkan musim menggunakan bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    seasonal_data.plot(kind='bar', ax=ax)
    plt.title('Pola Perilaku Peminjaman Sepeda Berdasarkan Musim')
    plt.xlabel('Season')
    plt.ylabel('Total Rental Count')
    plt.legend(title='Year')
    plt.xticks(rotation=0)
    st.pyplot(fig)  # Menampilkan plot menggunakan Streamlit

def visualize_seasonal_data_casual(df):
    # Preprocessing data
    df['yr'] = df['yr'].replace({0: '2011', 1: '2012'})
    df['season'] = df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    # Menyiapkan data untuk plot
    seasonal_data = df.groupby(['season', 'yr'])['casual'].sum().unstack()

    # Memvisualisasikan pola perilaku peminjaman sepeda berdasarkan musim menggunakan bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    seasonal_data.plot(kind='bar', ax=ax)
    plt.title('Pola Perilaku Peminjaman Sepeda (casual) Berdasarkan Musim')
    plt.xlabel('Season')
    plt.ylabel('Total Rental Count')
    plt.legend(title='Year')
    plt.xticks(rotation=0)
    st.pyplot(fig)  # Menampilkan plot menggunakan Streamlit

def visualize_seasonal_data_registered(df):
    # Preprocessing data
    df['yr'] = df['yr'].replace({0: '2011', 1: '2012'})
    df['season'] = df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    # Menyiapkan data untuk plot
    seasonal_data = df.groupby(['season', 'yr'])['registered'].sum().unstack()

    # Memvisualisasikan pola perilaku peminjaman sepeda berdasarkan musim menggunakan bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    seasonal_data.plot(kind='bar', ax=ax)
    plt.title('Pola Perilaku Peminjaman Sepeda (Registered) Berdasarkan Musim')
    plt.xlabel('Season')
    plt.ylabel('Total Rental Count')
    plt.legend(title='Year')
    plt.xticks(rotation=0)
    st.pyplot(fig)  # Menampilkan plot menggunakan Streamlit

# Fungsi untuk memvisualisasikan data dan melakukan preprocessing
def visualize_monthly_data(day_df):
    # Ekstrak tahun dari kolom 'dteday'
    day_df['year'] = pd.to_datetime(day_df['dteday']).dt.year

    # Menghitung total nilai 'casual' dan 'registered' pada setiap bulan dan tahun
    total_per_month_year = day_df.groupby(['year', 'mnth'])[['casual', 'registered']].sum().reset_index()

    # Mengatur ukuran plot
    plt.figure(figsize=(10, 6))

    # Memisahkan data casual dan registered
    casual_data = total_per_month_year['casual']
    registered_data = total_per_month_year['registered']
    months = total_per_month_year['mnth']
    years = total_per_month_year['year']

    # Memplot casual
    plt.plot(casual_data, label='Casual', marker='o')

    # Memplot registered
    plt.plot(registered_data, label='Registered', marker='o')

    # Memberikan judul dan label sumbu
    plt.title('Total Casual vs Registered per Month and Year')
    plt.xlabel('Month and Year')
    plt.ylabel('Total Count')

    # Menambahkan label bulan dan tahun di sumbu x
    plt.xticks(ticks=range(len(months)), labels=[f'{months[i]}-{years[i]}' for i in range(len(months))], rotation=45)

    # Menambahkan legenda
    plt.legend()

    # Menampilkan plot
    plt.tight_layout()
    st.pyplot(plt)  # Menampilkan plot menggunakan Streamlit

# Fungsi untuk memvisualisasikan data dan melakukan preprocessing
def visualize_hourly_data(hour_df):
    # Menyiapkan data untuk plot
    hour_vs_workingday = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().unstack()

    # Membuat label jam dalam format yang diinginkan
    hour_labels = [f"{i}-{i+1} AM" if i < 12 else f"{i-12}-{i-11} PM" if i < 23 else '11-12 PM' for i in range(24)]

    # Memvisualisasikan perbandingan pola peminjaman sepeda antara hari kerja dan hari libur
    plt.figure(figsize=(14, 8))
    hour_vs_workingday.plot(kind='line', marker='o', markersize=5)
    plt.title('Perbandingan Pola Peminjaman Sepeda antara Hari Kerja dan Hari Libur')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Rental Count')
    plt.xticks(range(24), labels=hour_labels, rotation=45)  # Mengubah label menjadi jam
    plt.legend(['Non-Working Day', 'Working Day'], title='Workingday')
    plt.tight_layout()
    st.pyplot(plt)  # Menampilkan plot menggunakan Streamlit

def visualize_hourly_data_casual(hour_df):
    # Menyiapkan data untuk plot
    hour_vs_workingday = hour_df.groupby(['hr', 'workingday'])['casual'].mean().unstack()

    # Membuat label jam dalam format yang diinginkan
    hour_labels = [f"{i}-{i+1} AM" if i < 12 else f"{i-12}-{i-11} PM" if i < 23 else '11-12 PM' for i in range(24)]

    # Memvisualisasikan perbandingan pola peminjaman sepeda antara hari kerja dan hari libur
    plt.figure(figsize=(14, 8))
    hour_vs_workingday.plot(kind='line', marker='o', markersize=5)
    plt.title('Perbandingan Pola Peminjaman Sepeda (Casual) antara Hari Kerja dan Hari Libur')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Rental Count')
    plt.xticks(range(24), labels=hour_labels, rotation=45)  # Mengubah label menjadi jam
    plt.legend(['Non-Working Day', 'Working Day'], title='Workingday')
    plt.tight_layout()
    st.pyplot(plt)

def visualize_hourly_data_registered(hour_df):
    # Menyiapkan data untuk plot
    hour_vs_workingday = hour_df.groupby(['hr', 'workingday'])['registered'].mean().unstack()

    # Membuat label jam dalam format yang diinginkan
    hour_labels = [f"{i}-{i+1} AM" if i < 12 else f"{i-12}-{i-11} PM" if i < 23 else '11-12 PM' for i in range(24)]

    # Memvisualisasikan perbandingan pola peminjaman sepeda antara hari kerja dan hari libur
    plt.figure(figsize=(14, 8))
    hour_vs_workingday.plot(kind='line', marker='o', markersize=5)
    plt.title('Perbandingan Pola Peminjaman Sepeda (Registered) antara Hari Kerja dan Hari Libur')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Rental Count')
    plt.xticks(range(24), labels=hour_labels, rotation=45)  # Mengubah label menjadi jam
    plt.legend(['Non-Working Day', 'Working Day'], title='Workingday')
    plt.tight_layout()
    st.pyplot(plt)

def analyze_and_visualize_clusters(day_df):
    # Ekstrak tahun dari kolom 'dteday'
    day_df['year'] = pd.to_datetime(day_df['dteday']).dt.year

    # Menghitung total nilai 'casual' dan 'registered' pada setiap bulan dan tahun
    total_per_month_year = day_df.groupby(['year', 'mnth'])[['casual', 'registered']].sum().reset_index()

    cluster_centers = {
        1: {'casual': 10000, 'registered': 50000},
        2: {'casual': 25000, 'registered': 100000},
        3: {'casual': 40000, 'registered': 150000}
    }

    # Alokasikan data ke kluster terdekat
    for index, row in total_per_month_year.iterrows():
        min_distance = float('inf')
        assigned_cluster = None

        for cluster_id, center in cluster_centers.items():
            distance = ((row['casual'] - center['casual']) ** 2 + (row['registered'] - center['registered']) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                assigned_cluster = cluster_id

        total_per_month_year.at[index, 'cluster'] = assigned_cluster

    # Analisis karakteristik cluster
    cluster_characteristics = total_per_month_year.groupby('cluster')[['casual', 'registered']].describe().fillna(0)

    # Visualisasi cluster
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=total_per_month_year, x='casual', y='registered', hue='cluster')
    plt.xlabel('Casual')
    plt.ylabel('Registered')
    plt.title('Clustering Results')
    st.pyplot(plt)  # Menampilkan plot menggunakan Streamlit

    # Analisis perbedaan antar cluster
    cluster_comparison = total_per_month_year.groupby('cluster')[['casual', 'registered']].mean().fillna(0)

    # Menampilkan hasil analisis
    st.write("Karakteristik Cluster:")
    st.write(cluster_characteristics)
    st.write("Perbandingan Rata-Rata Antara Cluster:")
    st.write(cluster_comparison)

def visualize_total_count(day_df):
    # Ekstrak tahun dari kolom 'dteday'
    day_df['year'] = pd.to_datetime(day_df['dteday']).dt.year

    # Menghitung total nilai 'casual' dan 'registered' pada setiap bulan dan tahun
    total_per_month_year = day_df.groupby(['year', 'mnth'])[['casual', 'registered']].sum().reset_index()

    # Mengatur ukuran plot
    plt.figure(figsize=(10, 6))

    # Memisahkan data count dan registered
    count_data = total_per_month_year['casual'] + total_per_month_year['registered']
    registered_data = total_per_month_year['registered']
    months = total_per_month_year['mnth']
    years = total_per_month_year['year']

    # Memplot count
    plt.plot(count_data, label='Count (Casual + Registered)', marker='o')

    # Memberikan judul dan label sumbu
    plt.title('Total Count (Casual + Registered)')
    plt.xlabel('Month and Year')
    plt.ylabel('Total Count')

    # Menambahkan label bulan dan tahun di sumbu x
    plt.xticks(ticks=range(len(months)), labels=[f'{months[i]}-{years[i]}' for i in range(len(months))], rotation=45)

    # Menambahkan legenda
    plt.legend()

    # Menampilkan plot
    plt.tight_layout()
    st.pyplot(plt)  # Menampilkan plot menggunakan Streamlit


tab1, tab2, tab3, tab4 = st.tabs(["**Home**", "**Pertanyaan 1**", "**Pertanyaan 2**", "**Cluster Analisis**"])
 
with tab1:
    st.header('Monthly Casual vs Registered Count')
    visualize_monthly_df = visualize_monthly_data(main_df)
    st.header('Total Count (Casual + Registered) Analysis')
    visualize_total_df = visualize_total_count(main_df)
 
with tab2:   
    with st.expander("Apakah terdapat pola perilaku peminjaman sepeda yang berbeda antara musim (season) yang berbeda di Washington D.C. selama dua tahun (2011-2012)?"):
        st.write(
        """Ya, Terdapat pola yang berbeda. Peminjaman sepeda yang paling sedikit itu baik di tahun 2011 maupun 2012 yaitu pada season spring sedangkan peminjaman sepeda yang terbanyak baik di 2011 maupun 2012 yaitu pada season fall. Dilihat dari eksplorasi yang dialkukan memang pada musim spring terjadi penurunan signifikan pada peminjaman sepeda sehingga dengan kesimpulan ini perusahaan dapat mencari penyebaba dari penurunan tersebut. Penyebab tersebut mungkin saja karena weathersit, temp, dan lainnya karena semua itu kita tau musim itu akan berpengaruh terhadap semua hal tersebut"""
    )
    st.header('Bike Rental Behavior by Season')
    visualize_seasonal_df = visualize_seasonal_data(main_df)
    st.header('Bike Rental Behavior (Casual) by Season')
    visualize_seasonal_casual_df = visualize_seasonal_data_casual(main_df)
    st.header('Bike Rental Behavior (Registered) by Season')
    visualize_seasonal_registered_df = visualize_seasonal_data_registered(main_df)
    
with tab3:
    with st.expander("Apakah terdapat perbedaan pola jam saat peminjaman sepeda antara hari kerja dan hari libur?"):
        st.write(
        """Ya, Terdapat pola yang berbeda. keseluruhan baik pengguna biasa maupun pengguna baru itu peminjaman sepeda pada hari kerja itu tinggi pada jam pagi dan sore dan itu dapat dilihat juga bahwa itu jam pergi bekerja dan pulang bekerja jadi orang meminjam sepeda kemungkinan besar untuk pergi dan pulang bekerja. Sedangkan pada hari tidak bekerja secara keseluruhan dari pagi hingga sore orang meminjam sepeda yang banayk dan puncaknya tengah hari/siang hari. Jika dilihat dari register atau orang yang baru mendaftar itu hampir sama namun jika dilihat pada casual saja pengguna biasa itu tidak terlalu menggunakan sepeda pada saat bekerja namun pada saat tidak bekerja mereka banyak menggunakannya. Ini bisa jadi pertanda bahwa orang orang menggunakan terkadang mengikuti hype saja dan perusahaan belum mampu mempertahankan pengguna lama untuk terus menggunakannya.""")
    st.header('Hourly Bike Rental Comparison')
    visualize_hourly_df = visualize_hourly_data(main_df_hour)
    st.header('Hourly Bike Rental Comparison (Casual)')
    visualize_hourly_casual_df = visualize_hourly_data_casual(hour_df)
    st.header('Hourly Bike Rental Comparison (Registered)')
    visualize_hourly_registered_df = visualize_hourly_data_registered(hour_df)

with tab4:
    with st.expander("Tren dan Pola yang dapat diamati"):
        st.write(
        """Cluster 3 menunjukkan kecenderungan memiliki nilai 'casual' dan 'registered' yang tinggi, yang menunjukkan tingkat aktivitas yang tinggi.\n\n Cluster 2 memiliki nilai 'registered' yang lebih tinggi daripada Cluster 1, tetapi nilai 'casual' lebih rendah dari Cluster 3.\n\n Cluster 1 memiliki rata-rata nilai 'casual' dan 'registered' yang lebih rendah daripada Cluster 2 dan 3.\n\n Keterkaitan antara 'Casual' dan 'Registered': Secara umum, cluster yang memiliki nilai 'casual' yang tinggi cenderung memiliki nilai 'registered' yang tinggi juga, dan sebaliknya. Namun, dalam contoh ini, Cluster 3 menonjol dengan nilai 'casual' dan 'registered' yang tinggi secara bersamaan.""")
    st.header('Cluster Analysis')
    analyze_and_visualize_df = analyze_and_visualize_clusters(main_df)
