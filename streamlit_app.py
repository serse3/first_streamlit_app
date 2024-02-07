import streamlit
import pandas
import snowflake.connector



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


streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


streamlit.header('Breakfast Menu')
# Read the fruit list from a CSV file
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") 
# Display the table on the page.
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the DataFrame
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


