import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError
import matplotlib.pyplot as plt
import numpy as np

#Starting: 
streamlit.header('China population view:')
#Estoy realizando una conexión con snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
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
my_data_row = my_data_row.sort_values(by='SUM', ascending = False)
#Si no tienen mas de 50 k los filtro.
my_data_row = my_data_row[my_data_row['SUM']>50]
#Tengo que añadir una columna con los datos de ubicación. 

#Muestro el df -> Pero lo comento porque no quiero un df ahora. 
#streamlit.dataframe(my_data_row)



# Crear un gráfico de barras
fig, ax = plt.subplots()
bars = ax.bar(my_data_row['NAME'], my_data_row['SUM'])

# Añadir título y etiquetas a los ejes
ax.set_title('Gráfico de Barras')
ax.set_xlabel('NAME')
ax.set_ylabel('SUM')
plt.xticks(rotation=90)

# Mostrar el gráfico en Streamlit
streamlit.pyplot(fig, use_container_width=True)

# Capturar la selección del usuario
bar_clicked = streamlit.pyplot()
if bar_clicked:
    # Obtener la barra seleccionada
    index = bar_clicked.image_data.element.get_cursor_data()
    if index:
        # Obtener los detalles de la barra seleccionada
        bar_details = my_data_row.iloc[index[0]]
        streamlit.write(f'Detalles de la barra seleccionada: {bar_details}')


streamlit.stop()
def Top():    
  # Read the fruit list from a CSV file
  my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") 
  # Display the table on the page.
  my_fruit_list = my_fruit_list.set_index('Fruit')
  fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
  fruits_to_show = my_fruit_list.loc[fruits_selected]
  # Display the DataFrame
  streamlit.dataframe(fruits_to_show)
def getFruit():
  try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a furit to get information.")
    else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # write your own comment -what does the next line do? 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # write your own comment - what does this do?
      streamlit.dataframe(fruityvice_normalized)
  except URLError as e:
    streamlit.error()
streamlit.write('The user entered ', fruit_choice)


#Defino la tabla principal
Top()
streamlit.header("Fruityvice Fruit Advice!")

streamlit.markdown("<style>h1{color: red; font-style:italic;}</style>",unsafe_allow_html=True)

getFruit()


#Hacemos otra llamada a snowflake para recuperar datos:
streamlit.header("The fruit load list contains:")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)






add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_my_fruit)

streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")



