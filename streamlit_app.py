import streamlit
import pandas
import requests
import snowflake.connector
from   urllib.error import URLError

streamlit.title('My parents new healthy Diner')
streamlit.header ('Breakfast Favourites')
streamlit.text ('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text ('🥗 Kale Spinach Rocket Smoothie')
streamlit.text ('🐔 Hard Boiled Free Range Egg')
streamlit.text ('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#set the index
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
#display selections
streamlit.dataframe(fruits_to_show)
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

#create a function which is a repeatable code block
def get_fruityadvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized 
  
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get info")
  else:
     back_from_function = get_fruityadvice_data(fruit_choice)
    # normalized version gets displayed in a table
    streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruitload list contains")
streamlit.dataframe(my_data_rows)
streamlit.header('Fruityvice Fruit Addition from customer!')
add_my_fruit = streamlit.text_input('What fruit would you like to add')
streamlit.write('Thank you for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

