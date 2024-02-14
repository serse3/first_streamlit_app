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
SELECT SCM.NAME, sum(TIMEPOINT.VALUE) as "SUM" FROM TIMEPOINT 
JOIN SERIES AS SCM ON SCM.SERIES_CODE = TIMEPOINT.SERIES_CODE GROUP BY SCM.NAME
""")
#Df con mis datos: 
my_data_row = my_cur.fetch_pandas_all()

streamlit.dataframe(my_data_row)

# Crear un gráfico de barras
fig, ax = plt.subplots()
ax.bar(my_data_row['NAME'], my_data_row['SUM'])

# Añadir título y etiquetas a los ejes
ax.set_title('Gráfico de Barras')
ax.set_xlabel('NAME')
ax.set_ylabel('SUM')

# Mostrar el gráfico en Streamlit
streamlit.pyplot(fig)

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



