import streamlit
import pandas

streamlit.header('Breakfast Menu')

# Read the fruit list from a CSV file
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Display the DataFrame
streamlit.dataframe(my_fruit_list)
