import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError



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
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
      streamlit.error("Please select a furit to get information.")
    else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
      # write your own comment -what does the next line do? 
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # write your own comment - what does this do?
      streamlit.dataframe(fruityvice_normalized)
  except URLError as e:
    streamlit.error()

#Starting: 
streamlit.header('Breakfast Menu')
#Defino la tabla principal
Top()


streamlit.stop()
streamlit.header("Fruityvice Fruit Advice!")
getFruit()






streamlit.stop()



  

streamlit.write('The user entered ', fruit_choice)







#Quiero ver si la comunicación con snowflake funciona correctamente:

#Estoy realizando una conexión con snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#Creo un cursor para ejecutar una consulta. 
my_cur = my_cnx.cursor()
#Ejecuto la consulta
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#Recupero la primera fila de mi consulta: 
my_data_row = my_cur.fetchone()
#Muestro por pantalla un texto:
streamlit.text("Hello from Snowflake:")
#Muestro la primera fila recuperada
streamlit.text(my_data_row)

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



