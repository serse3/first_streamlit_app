import streamlit
import pandas

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
import requests



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())


