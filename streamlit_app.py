import streamlit as st
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError
import matplotlib.pyplot as plt
import numpy as np

#Starting: 
st.header('China population view:')
#Estoy realizando una conexión con snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#Creo un cursor para ejecutar una consulta. 
my_cur = my_cnx.cursor()
#Ejecuto la consulta
my_cur.execute("""
WITH ranked_data AS (
    SELECT SCM.NAME, 
           TIMEPOINT.VALUE,
           RANK() OVER (PARTITION BY SCM.SERIES_CODE ORDER BY TIMEPOINT.DATE DESC) AS rank
    FROM SERIES AS SCM 
    JOIN TIMEPOINT ON SCM.SERIES_CODE = TIMEPOINT.SERIES_CODE
)
SELECT NAME, SUM(VALUE) AS "SUM"
FROM ranked_data
WHERE rank = 1
GROUP BY NAME
""")
#Df con mis datos: 
my_data_row = my_cur.fetch_pandas_all()
#Ordeno por cantidad
my_data_row = my_data_row.sort_values(by='SUM', ascending = False)
st.dataframe(my_data_row)
#Si no tienen mas de 50 k los filtro.
my_data_row = my_data_row[my_data_row['SUM']>50]
#Inicio el geolocalizador: 
geolocator = Nominatim(user_agent ="geoapiExercises")
#Hago una función para obtener la longitud y latitud: 
def get_lat_lon(region):
    location = geolocator.geocode(region +", China")
    if location: 
        return location.latitude,location.longitude
    else: 
        return None,None
#Función para eliminar las palabras clave: 
def eliminar_palabras_clave(texto): 
    for palabra in palabras_clave:
        texto = texto.replace(palabra, '')
    return texto
#Añado la lista de palabras clave: 
palabras_a_eliminar =['CN:','Population:', 'Registered:', 'more than Half Year:']
#Llamo a la función para eliminar: 
st.dataframe(my_data_row)
my_data_row['Region_Name'] = my_data_row['NAME'].apply(eliminar_palabras_clave)
st.dataframe(my_data_row)
#Aplico la función en todo el df: 
my_data_row['lat_lon'] = my_data_row['Region_Name'].apply(get_lat_lon)
st.dataframe(my_data_row)
# Aplica la función para obtener latitud y longitud
my_data_row[['lat','lon']] = pd.DataFrame(my_data_row['lat_lon'].tolist(),index = my_data_row.index)                       
#Muestro el df -> Pero lo comento porque no quiero un df ahora. 
st.dataframe(my_data_row)



# Crear un gráfico de barras
fig, ax = plt.subplots()
bars = ax.bar(my_data_row['NAME'], my_data_row['SUM'])

# Añadir título y etiquetas a los ejes
ax.set_title('Gráfico de Barras')
ax.set_xlabel('NAME')
ax.set_ylabel('SUM')
plt.xticks(rotation=90)

# Mostrar el gráfico en Streamlit
st.pyplot(fig, use_container_width=True)

# Capturar la selección del usuario
bar_clicked = st.pyplot()
if bar_clicked:
    # Obtener la barra seleccionada
    index = bar_clicked.image_data.element.get_cursor_data()
    if index:
        # Obtener los detalles de la barra seleccionada
        bar_details = my_data_row.iloc[index[0]]
        st.write(f'Detalles de la barra seleccionada: {bar_details}')


st.stop()
def Top():    
  # Read the fruit list from a CSV file
  my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") 
  # Display the table on the page.
  my_fruit_list = my_fruit_list.set_index('Fruit')
  fruits_selected =st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
  fruits_to_show = my_fruit_list.loc[fruits_selected]
  # Display the DataFrame
  st.dataframe(fruits_to_show)
def getFruit():
  try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
      st.error("Please select a furit to get information.")
    else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # write your own comment -what does the next line do? 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # write your own comment - what does this do?
      st.dataframe(fruityvice_normalized)
  except URLError as e:
    st.error()
st.write('The user entered ', fruit_choice)


#Defino la tabla principal
Top()
st.header("Fruityvice Fruit Advice!")

st.markdown("<style>h1{color: red; font-style:italic;}</style>",unsafe_allow_html=True)

getFruit()


#Hacemos otra llamada a snowflake para recuperar datos:
st.header("The fruit load list contains:")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
st.text("The fruit load list contains:")
st.dataframe(my_data_row)






add_my_fruit = st.text_input('What fruit would you like to add?')
st.write('The user entered ', add_my_fruit)

st.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")



