import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError
import matplotlib.pyplot as plt
import numpy as np

#Starting: 
streamlit.header('World data view')

#Quiero ver si la comunicación con snowflake funciona correctamente:

#Estoy realizando una conexión con snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#Creo un cursor para ejecutar una consulta. 
my_cur = my_cnx.cursor()
#Ejecuto la consulta
my_cur.execute("""
SELECT TIMEPOINT.SERIES_CODE, SCM.NAME, TIMEPOINT.VALUE FROM TIMEPOINT 
JOIN SERIES AS SCM ON SCM.SERIES_CODE = TIMEPOINT.SERIES_CODE
WHERE TIMEPOINT.SERIES_CODE ='SR1223104' ORDER BY DATE DESC;

""")

#Recupero la primera fila de mi consulta: 
my_data_row = my_cur.fetch_pandas_all()
#Muestro por pantalla un texto:
streamlit.text("Hello from Snowflake:")
#Muestro la primera fila recuperada
streamlit.dataframe(my_data_row)


# Generar datos de muestra
x = np.linspace(0, 10, 50)
y = np.sin(x)

# Crear un gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, '-b', label='Sinusoidal')
ax.legend()

# Mostrar el gráfico en Streamlit
streamlit.pyplot(fig)


#Ahora hago un gráfico de barras: 
df = pd.DataFrame({
    'categoria': ['A', 'B', 'C', 'D'],
    'valor': [10, 20, 30, 40]
})

# Crear un gráfico de barras
fig, ax = plt.subplots()
ax.bar(df['categoria'], df['valor'])

# Añadir título y etiquetas a los ejes
ax.set_title('Gráfico de Barras')
ax.set_xlabel('Categoría')
ax.set_ylabel('Valor')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

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



