import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import plotly.graph_objects as go

# Mengatur teks menjadi rata tengah dengan CSS langsung
st.write("""
<style>
    .centered-text {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan teks di tengah
st.write("<h2 class='centered-text'>Visualisasi Kualitas Udara di 12 Kota di China</h2>", unsafe_allow_html=True)
# st.header("Visualisasi Kualitas Udara di 12 Kota di China")
# col1, col2 = st.columns(2)
# col1, col2 = st.columns([1, 2])
tab1, tab2, tab3, tab4 = st.tabs(["Peta", "Grafik 12 Kota Per Tahun","Grafik Kualitas Udara Per Tahun", "Grafik Kualitas Udara Per Bulan",])
with tab1:
    # st.markdown('<h3 style="font-size: 22px;">Visualisasi Kualitas Udara di 12 Kota di China pada Peta</h3>', unsafe_allow_html=True)
    # st.markdown('<h3 style="font-size: 22px;">Peta Tren Perubahan Kualitas Udara 2013-2017 Berdasarkan Rata-rata Per Tahun</h3>', unsafe_allow_html=True)

    # Groupby untuk masing-masing kota
    kota_list = ["Guanyuan", "Dongsi", "Dingling", "Changping", "Aotizhongxin", "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]

    # Perbarui dataframe dengan data yang tersedia
    all_PM25 = pd.read_csv('all_data_PM25.csv')
    all_PM10 = pd.read_csv('all_data_PM10.csv')
    all_SO2 = pd.read_csv('all_data_SO2.csv')
    all_NO2 = pd.read_csv('all_data_NO2.csv')
    all_CO = pd.read_csv('all_data_CO.csv')
    all_O3 = pd.read_csv('all_data_O3.csv')


    # Apply CSS to adjust the width of the selectbox
    st.markdown(
        f"""
        <style>
            div[data-testid="stSelectbox"] {{
                width: 300px !important;
            }}
            
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create dropdown widgets for year and month      
    # year = st.sidebar.selectbox('Year', options=range(2013, 2018), index=4)
    # month = st.sidebar.selectbox('Month', options=range(1, 13), index=0)
    # parameter = st.sidebar.selectbox('Pilih Parameter Kualitas Udara', options=['PM2.5', 'PM10', 'O3'])
    year = st.selectbox('Year', options=range(2013, 2018), index=4)
    if year == 2013:
        month_options = range(3, 13)
        month_index = 0 if month_options[0] != 2 else 1
    elif year == 2017:
        month_options = range(1, 3)
        month_index = 1 if month_options[0] != 2 else 0
    else:
        month_options = range(1, 13)
        month_index = 1

    month = st.selectbox('Month', options=month_options, index=month_index)
    # month = st.selectbox('Month', options=range(1, 13), index=0)
    parameter = st.selectbox('Pilih Parameter Kualitas Udara', options=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

    # Filter data based on selected year and month
    filtered_dataPM25 = all_PM25[(all_PM25['year'] == year) & (all_PM25['month'] == month)]
    filtered_dataPM10 = all_PM10[(all_PM10['year'] == year) & (all_PM10['month'] == month)]
    filtered_dataSO2 = all_SO2[(all_SO2['year'] == year) & (all_SO2['month'] == month)]
    filtered_dataNO2 = all_NO2[(all_NO2['year'] == year) & (all_NO2['month'] == month)]
    filtered_dataCO = all_CO[(all_CO['year'] == year) & (all_CO['month'] == month)]
    filtered_dataO3 = all_O3[(all_O3['year'] == year) & (all_O3['month'] == month)]

    # Convert filtered data to array
    data_arrayPM25 = filtered_dataPM25.values[:, 2:]
    data_arrayPM10 = filtered_dataPM10.values[:, 2:]
    data_arraySO2 = filtered_dataSO2.values[:, 2:]
    data_arrayNO2 = filtered_dataNO2.values[:, 2:]
    data_arrayCO = filtered_dataCO.values[:, 2:]
    data_arrayO3 = filtered_dataO3.values[:, 2:]

    # Combine data into one dictionary
    data = {
        'PM2.5': data_arrayPM25[0],  # Gunakan kunci yang berbeda
        'PM10': data_arrayPM10[0],    # Gunakan kunci yang berbeda
        'SO2': data_arraySO2[0],         # Gunakan kunci yang berbeda
        'NO2': data_arrayNO2[0],
        'CO': data_arrayCO[0],
        'O3': data_arrayO3[0],        # Gunakan kunci yang berbeda
    }

    # Membuat DataFrame dari data yang digabungkan
    df1 = pd.DataFrame(data)

    data = {
        'City': ['Guanyuan', 'Dongsi', 'Dingling', 'Changping', 'Aotizhongxin', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'],
        'Latitude': [39.906217, 39.917545, 40.291537, 40.220585, 40.002227, 39.914818, 40.357388, 39.937217, 40.127572, 39.886087, 39.987872, 39.878935],
        'Longitude': [116.434355, 116.421367, 116.250587, 116.235910, 116.391095, 116.294210, 116.634790, 116.461353, 116.655828, 116.407526, 116.291440, 116.352796],
        'PM2.5': df1['PM2.5'],
        'PM10': df1['PM10'],
        'SO2': df1['SO2'],
        'NO2': df1['NO2'],
        'CO': df1['CO'],
        'O3': df1['O3'],
    }

    # Membuat DataFrame dari data
    df = pd.DataFrame(data)

    # Streamlit app
    # st.title('Visualisasi Kualitas Udara di 12 Kota di China pada Peta')
    # st.markdown('<h1 style="font-size: 24px;">Visualisasi Kualitas Udara di 12 Kota di China pada Peta</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 16px;">Peta Tren Perubahan Kualitas Udara 2013-2017 Berdasarkan Rata-rata Per Tahun</h3>', unsafe_allow_html=True)


    # Create a map centered around the middle of the dataframe
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10, width=700, height=500)
    # m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10, width=map_width, height=map_height)

    # Add circles to the map with radius and color based on air quality parameter
    for i, row in df.iterrows():
        # Hitung radius berdasarkan nilai parameter kualitas udara
        # radius = row[parameter] * 30  # Misalnya, Anda dapat mengalikan dengan 100 untuk menyesuaikan skala
        if parameter == 'CO':
            value = 1
        else:
            value = 30

        radius = row[parameter] * value

        # Tentukan warna lingkaran berdasarkan nilai parameter kualitas udara
        if parameter == 'PM2.5':
            if row[parameter] <= 15.5:
                color = 'green'
            elif row[parameter] <= 55.4:
                color = 'blue'
            elif row[parameter] <= 150.4:
                color = 'yellow'
            elif row[parameter] <= 250.4:
                color = 'red'
            else:
                color = 'black'
        elif parameter == 'PM10':
            if row[parameter] <= 50:
                color = 'green'
            elif row[parameter] <= 150:
                color = 'blue'
            elif row[parameter] <= 350:
                color = 'yellow'
            elif row[parameter] <= 420:
                color = 'red'
            else:
                color = 'black'
        elif parameter == 'SO2':
            if row[parameter] <= 0.14:
                color = 'green'
            else:
                color = 'red'
        elif parameter == 'NO2':
            if row[parameter] <= 0.08:
                color = 'green'
            else:
                color = 'red'
        elif parameter == 'CO':
            if row[parameter] <= 25:
                color = 'green'
            else:
                color = 'red'
        elif parameter == 'O3':
            if row[parameter] <= 120:
                color = 'green'
            else:
                color = 'red'

        # Format teks dengan HTML untuk membuat nama kota tebal/bold dan menambahkan satuan
        popup_text = f"<b>{row['City']}</b><br>{row[parameter]} ug/m<sup>3</sup>"
        # Tambahkan lingkaran dengan radius yang dihitung dan warna yang ditentukan ke peta
        folium.Circle(location=[row['Latitude'], row['Longitude']], radius=radius, color=color, fill=True, fill_opacity=0.2, popup=popup_text).add_to(m)

        # Format teks dengan HTML untuk membuat nama kota tebal/bold dan menambahkan satuan
        # popup_text = f"<b>{row['City']}</b><br>{row[parameter]} ug/m<sup>3</sup>"

        # Tambahkan marker dengan teks yang diformat ke peta
        folium.Marker([row['Latitude'], row['Longitude']], popup=popup_text, icon=folium.Icon(icon='cloud', prefix='fa', icon_size=(5, 5))).add_to(m)

    # Display the map
    folium_static(m)


with tab2:
    # Define list of cities
    kota_list = ["Guanyuan", "Dongsi", "Dingling", "Changping", "Aotizhongxin", "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]

    # Define a function to plot data
    def plot_data(parameter, calculation, plot_type):
        # Read CSV files based on calculation method (Mean or Sum)
        if calculation == 'mean':
            all_PM25 = pd.read_csv("all_data_PM25_Mean.csv")
            all_PM10 = pd.read_csv("all_data_PM10_Mean.csv")
            all_SO2 = pd.read_csv("all_data_SO2_Mean.csv")
            all_NO2 = pd.read_csv("all_data_NO2_Mean.csv")
            all_CO = pd.read_csv("all_data_CO_Mean.csv")
            all_O3 = pd.read_csv("all_data_O3_Mean.csv")
            all_TEMP = pd.read_csv("all_data_TEMP_Mean.csv")
        else:
            all_PM25 = pd.read_csv("all_data_PM25_Sum.csv")
            all_PM10 = pd.read_csv("all_data_PM10_Sum.csv")
            all_SO2 = pd.read_csv("all_data_SO2_Sum.csv")
            all_NO2 = pd.read_csv("all_data_NO2_Sum.csv")
            all_CO = pd.read_csv("all_data_CO_Sum.csv")
            all_O3 = pd.read_csv("all_data_O3_Sum.csv")
            all_TEMP = pd.read_csv("all_data_TEMP_Sum.csv")

        # Merge all dataframes based on 'year' column
        merged_df = all_PM25.merge(all_PM10, on='year').merge(all_SO2, on='year').merge(all_NO2, on='year').merge(all_CO, on='year').merge(all_O3, on='year').merge(all_TEMP, on='year')

        # Define colors for each city
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']

        # Initialize the figure
        fig = go.Figure()
        
        # Loop through each city to add lines or bars to the plot based on plot type
        for i, city in enumerate(kota_list):
            filtered_data = merged_df[(merged_df['year'] >= 2014) & (merged_df['year'] <= 2016)]
            if plot_type == 'bar':
                fig.add_trace(go.Bar(x=filtered_data['year'], y=filtered_data[f"{parameter}_{city}"], name=city, marker_color=colors[i]))
            else:
                fig.add_trace(go.Scatter(x=filtered_data['year'], y=filtered_data[f"{parameter}_{city}"], name=city, line=dict(color=colors[i])))
        
        if calculation_widget == 'mean' and parameter_widget == 'PM2.5':
            st.markdown('<h3 style="font-size: 16px;">Air Quality Index (AQI) PM2.5:</h3>', unsafe_allow_html=True)
            st.image('pm25.jpg', width=750)
        elif calculation_widget == 'mean' and parameter_widget == 'PM10':
            st.markdown('<h3 style="font-size: 16px;">Air Quality Index (AQI) PM10:</h3>', unsafe_allow_html=True)
            st.image('pm10.jpg', width=750)
        elif calculation_widget == 'mean' and parameter_widget == 'SO2':
            st.markdown('<h3 style="font-size: 16px;">Nilai Baku Mutu SO2 : 0.14 ppm</h3>', unsafe_allow_html=True)
        elif calculation_widget == 'mean' and parameter_widget == 'NO2':
            st.markdown('<h3 style="font-size: 16px;">Nilai Baku Mutu NO2 : 0.08 ppm</h3>', unsafe_allow_html=True)
        elif calculation_widget == 'mean' and parameter_widget == 'CO':
            st.markdown('<h3 style="font-size: 16px;">Nilai Baku Mutu CO : 25 ppm</h3>', unsafe_allow_html=True)
        elif calculation_widget == 'mean' and parameter_widget == 'O3':
            st.markdown('<h3 style="font-size: 16px;">Nilai Baku Mutu O3 : 120 ppb</h3>', unsafe_allow_html=True)

        st.markdown('<h3 style="font-size: 16px;">Catatan : Jika ingin tidak menampilkan grafik salah satu kota, maka cukup di KLIK saja Nama Kota di bagian keterangan</h3>', unsafe_allow_html=True)

        # Add layout to the plot
        fig.update_layout(
            title=f"Tren Perubahan Kualitas Udara 2014-2016 Berdasarkan {'Rata-rata' if calculation == 'mean' else 'Total'} {parameter} Per Tahun\nJika",
            title_font=dict(size=16, family="Arial, sans-serif", color="black"),
            xaxis_title="Tahun",
            yaxis_title=f"{'Rata-rata ' if calculation == 'mean' else 'Total '} {parameter}",
            legend_title="Kota",
            template="plotly_white"
        )

        # Show the plot
        st.plotly_chart(fig)

    # Create dropdown widgets for selecting parameter, calculation method, and plot type
    parameter_widget = st.selectbox('Pilih Parameter Kualitas Udara:', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP'])
    calculation_widget = st.selectbox('Perhitungan:', ['mean', 'sum'])
    plot_type_widget = st.radio('Tipe Plot:', ['line', 'bar'])

    # Interactively update the plot based on dropdown selection
    plot_data(parameter_widget, calculation_widget, plot_type_widget)


with tab3:
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go

    city_widget = st.selectbox('Pilih Kota:', ['Guanyuan', 'Dongsi', 'Dingling', 'Changping', 'Aotizhongxin', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'])
    operation_widget = st.selectbox('Pilih Operasi:', ['mean', 'sum'])
    plot_type_widget = st.radio('Pilih Jenis Plot:', ['line', 'bar'])

    # Load data for each city based on the calculation operation
    if operation_widget == 'mean':
        all_Guanyuan = pd.read_csv("all_data_Guanyuan_Mean.csv")
        all_Dongsi = pd.read_csv("all_data_Dongsi_Mean.csv")
        all_Dingling = pd.read_csv("all_data_Dingling_Mean.csv")
        all_Changping = pd.read_csv("all_data_Changping_Mean.csv")
        all_Aotizhongxin = pd.read_csv("all_data_Aotizhongxin_Mean.csv")
        all_Gucheng = pd.read_csv("all_data_Gucheng_Mean.csv")
        all_Huairou = pd.read_csv("all_data_Huairou_Mean.csv")
        all_Nongzhanguan = pd.read_csv("all_data_Nongzhanguan_Mean.csv")
        all_Shunyi = pd.read_csv("all_data_Shunyi_Mean.csv")
        all_Tiantan = pd.read_csv("all_data_Tiantan_Mean.csv")
        all_Wanliu = pd.read_csv("all_data_Wanliu_Mean.csv")
        all_Wanshouxigong = pd.read_csv("all_data_Wanshouxigong_Mean.csv")
    else:
        all_Guanyuan = pd.read_csv("all_data_Guanyuan_Sum.csv")
        all_Dongsi = pd.read_csv("all_data_Dongsi_Sum.csv")
        all_Dingling = pd.read_csv("all_data_Dingling_Sum.csv")
        all_Changping = pd.read_csv("all_data_Changping_Sum.csv")
        all_Aotizhongxin = pd.read_csv("all_data_Aotizhongxin_Sum.csv")
        all_Gucheng = pd.read_csv("all_data_Gucheng_Sum.csv")
        all_Huairou = pd.read_csv("all_data_Huairou_Sum.csv")
        all_Nongzhanguan = pd.read_csv("all_data_Nongzhanguan_Sum.csv")
        all_Shunyi = pd.read_csv("all_data_Shunyi_Sum.csv")
        all_Tiantan = pd.read_csv("all_data_Tiantan_Sum.csv")
        all_Wanliu = pd.read_csv("all_data_Wanliu_Sum.csv")
        all_Wanshouxigong = pd.read_csv("all_data_Wanshouxigong_Sum.csv")

    # Define function to process data based on selected city and operation
    def process_data(city_data, columns_to_process, operation):
        # Filter data for the year range 2014-2016
        filtered_data = city_data[(city_data['year'] >= 2014) & (city_data['year'] <= 2016)]

        # Group the data by year, then calculate the mean/sum of each column
        if operation == 'mean':
            result = filtered_data.groupby('year')[columns_to_process].mean().reset_index()
        elif operation == 'sum':
            result = filtered_data.groupby('year')[columns_to_process].sum().reset_index()

        return result

    # Define columns for mean and sum operations
    columns_to_process = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP"]

    # Define function to plot data based on selected city and operation
    def plot_data(city, operation, plot_type):
        if city == 'Guanyuan':
            city_data = all_Guanyuan
            title_suffix = 'di kota Guanyuan'
        elif city == 'Dongsi':
            city_data = all_Dongsi
            title_suffix = 'di kota Dongsi'
        elif city == 'Dingling':
            city_data = all_Dingling
            title_suffix = 'di kota Dingling'
        elif city == 'Changping':
            city_data = all_Changping
            title_suffix = 'di kota Changping'
        elif city == 'Aotizhongxin':
            city_data = all_Aotizhongxin
            title_suffix = 'di kota Aotizhongxin'
        elif city == 'Gucheng':
            city_data = all_Gucheng
            title_suffix = 'di kota Gucheng'
        elif city == 'Huairou':
            city_data = all_Huairou
            title_suffix = 'di kota Huairou'
        elif city == 'Nongzhanguan':
            city_data = all_Nongzhanguan
            title_suffix = 'di kota Nongzhanguan'
        elif city == 'Shunyi':
            city_data = all_Shunyi
            title_suffix = 'di kota Shunyi'
        elif city == 'Tiantan':
            city_data = all_Tiantan
            title_suffix = 'di kota Tiantan'
        elif city == 'Wanliu':
            city_data = all_Wanliu
            title_suffix = 'di kota Wanliu'
        elif city == 'Wanshouxigong':
            city_data = all_Wanshouxigong
            title_suffix = 'di kota Wanshouxigong'

        # Process data based on selected city and operation
        result = process_data(city_data, columns_to_process, operation)

        # colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']
        fig = go.Figure()
        # Create plot using Plotly Express
        if plot_type == 'line':
            for column in columns_to_process:
                fig.add_trace(go.Scatter(x=result['year'], y=result[column], name=column))
                
        elif plot_type == 'bar':
            for column in columns_to_process:
                fig.add_trace(go.Bar(x=result['year'], y=result[column], name=column))
    
        st.markdown('<h3 style="font-size: 16px;">Catatan : Jika ingin tidak menampilkan grafik salah satu parameter, maka cukup di KLIK saja Nama Parameter di bagian keterangan</h3>', unsafe_allow_html=True)

        fig.update_layout(
            title=f"Tren Perubahan Kualitas Udara 2014-2016 Berdasarkan {'Rata-rata' if operation.capitalize() == 'Mean' else 'Total'} Per Tahun {title_suffix}", 
            title_font=dict(size=16, family="Arial, sans-serif", color="black"),           
            xaxis_title="Tahun",
            yaxis_title=f"{'Rata-rata ' if operation.capitalize() == 'Mean' else 'Total '}",
            legend_title="Parameter",
            template="plotly_white"
        )
        st.plotly_chart(fig)

    # Interactively update the plot based on selected city, operation, and plot type
    plot_data(city_widget, operation_widget, plot_type_widget)


with tab4:
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go

    city_widget2 = st.selectbox('Pilih Kota:', ['Guanyuan', 'Dongsi', 'Dingling', 'Changping', 'Aotizhongxin', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'], key='plot_city_widget_tab4')
    operation_widget2 = st.selectbox('Pilih Operasi:', ['mean', 'sum'], key='plot_operation_widget_tab4')
    plot_type_widget2 = st.radio('Pilih Jenis Plot:', ['line', 'bar'], key='plot_type_widget_tab4')

    # Load data for each city based on the calculation operation
    if operation_widget == 'mean':
        all_Guanyuan = pd.read_csv("all_data_Guanyuan_Mean_Month.csv")
        all_Dongsi = pd.read_csv("all_data_Dongsi_Mean_Month.csv")
        all_Dingling = pd.read_csv("all_data_Dingling_Mean_Month.csv")
        all_Changping = pd.read_csv("all_data_Changping_Mean_Month.csv")
        all_Aotizhongxin = pd.read_csv("all_data_Aotizhongxin_Mean_Month.csv")
        all_Gucheng = pd.read_csv("all_data_Gucheng_Mean_Month.csv")
        all_Huairou = pd.read_csv("all_data_Huairou_Mean_Month.csv")
        all_Nongzhanguan = pd.read_csv("all_data_Nongzhanguan_Mean_Month.csv")
        all_Shunyi = pd.read_csv("all_data_Shunyi_Mean_Month.csv")
        all_Tiantan = pd.read_csv("all_data_Tiantan_Mean_Month.csv")
        all_Wanliu = pd.read_csv("all_data_Wanliu_Mean_Month.csv")
        all_Wanshouxigong = pd.read_csv("all_data_Wanshouxigong_Mean_Month.csv")
    else:
        all_Guanyuan = pd.read_csv("all_data_Guanyuan_Sum_Month.csv")
        all_Dongsi = pd.read_csv("all_data_Dongsi_Sum_Month.csv")
        all_Dingling = pd.read_csv("all_data_Dingling_Sum_Month.csv")
        all_Changping = pd.read_csv("all_data_Changping_Sum_Month.csv")
        all_Aotizhongxin = pd.read_csv("all_data_Aotizhongxin_Sum_Month.csv")
        all_Gucheng = pd.read_csv("all_data_Gucheng_Sum_Month.csv")
        all_Huairou = pd.read_csv("all_data_Huairou_Sum_Month.csv")
        all_Nongzhanguan = pd.read_csv("all_data_Nongzhanguan_Sum_Month.csv")
        all_Shunyi = pd.read_csv("all_data_Shunyi_Sum_Month.csv")
        all_Tiantan = pd.read_csv("all_data_Tiantan_Sum_Month.csv")
        all_Wanliu = pd.read_csv("all_data_Wanliu_Sum_Month.csv")
        all_Wanshouxigong = pd.read_csv("all_data_Wanshouxigong_Sum_Month.csv")


    # Define function to process data based on selected city and operation
    def process_data(city_data, columns_to_process, operation):
        # Filter data for the year range 2014-2016
        # filtered_data = city_data[(city_data['month_year'] >= 2014) & (city_data['month_year'] <= 2016)]
        filtered_data = city_data[(city_data['month_year'].str.slice(0, 4).astype(int) >= 2013) & (city_data['month_year'].str.slice(0, 4).astype(int) <= 2017)]


        # Group the data by year, then calculate the mean/sum of each column
        if operation == 'mean':
            result = filtered_data.groupby('month_year')[columns_to_process].mean().reset_index()
        elif operation == 'sum':
            result = filtered_data.groupby('month_year')[columns_to_process].sum().reset_index()

        return result

    # Define columns for mean and sum operations
    columns_to_process = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP"]

    # Define function to plot data based on selected city and operation
    def plot_data(city, operation, plot_type):
        if city == 'Guanyuan':
            city_data = all_Guanyuan
            title_suffix = 'di kota Guanyuan'
        elif city == 'Dongsi':
            city_data = all_Dongsi
            title_suffix = 'di kota Dongsi'
        elif city == 'Dingling':
            city_data = all_Dingling
            title_suffix = 'di kota Dingling'
        elif city == 'Changping':
            city_data = all_Changping
            title_suffix = 'di kota Changping'
        elif city == 'Aotizhongxin':
            city_data = all_Aotizhongxin
            title_suffix = 'di kota Aotizhongxin'
        elif city == 'Gucheng':
            city_data = all_Gucheng
            title_suffix = 'di kota Gucheng'
        elif city == 'Huairou':
            city_data = all_Huairou
            title_suffix = 'di kota Huairou'
        elif city == 'Nongzhanguan':
            city_data = all_Nongzhanguan
            title_suffix = 'di kota Nongzhanguan'
        elif city == 'Shunyi':
            city_data = all_Shunyi
            title_suffix = 'di kota Shunyi'
        elif city == 'Tiantan':
            city_data = all_Tiantan
            title_suffix = 'di kota Tiantan'
        elif city == 'Wanliu':
            city_data = all_Wanliu
            title_suffix = 'di kota Wanliu'
        elif city == 'Wanshouxigong':
            city_data = all_Wanshouxigong
            title_suffix = 'di kota Wanshouxigong'

        # Process data based on selected city and operation
        result = process_data(city_data, columns_to_process, operation)

        # colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']
        fig = go.Figure()
        # Create plot using Plotly Express
        if plot_type == 'line':
            for column in columns_to_process:
                fig.add_trace(go.Scatter(x=result['month_year'], y=result[column], name=column))
                
        elif plot_type == 'bar':
            for column in columns_to_process:
                fig.add_trace(go.Bar(x=result['month_year'], y=result[column], name=column))

        st.markdown('<h3 style="font-size: 16px;">Catatan : Jika ingin tidak menampilkan grafik salah satu parameter, maka cukup di KLIK saja Nama Parameter di bagian keterangan</h3>', unsafe_allow_html=True)

        fig.update_layout(
            title=f"Tren Perubahan Kualitas Udara 2013-2017 Berdasarkan {'Rata-rata' if operation.capitalize() == 'Mean' else 'Total'} Per Tahun {title_suffix}", 
            title_font=dict(size=16, family="Arial, sans-serif", color="black"),           
            xaxis_title="Tahun",
            yaxis_title=f"{'Rata-rata ' if operation.capitalize() == 'Mean' else 'Total '}",
            legend_title="Parameter",
            template="plotly_white"
        )
        st.plotly_chart(fig)

    # Interactively update the plot based on selected city, operation, and plot type
    plot_data(city_widget2, operation_widget2, plot_type_widget2)