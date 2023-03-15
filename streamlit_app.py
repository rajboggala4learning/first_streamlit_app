import streamlit
streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')

# Test the code with 'Apple'
fruit_choice = streamlit.text_input('What fruit would you like information about?','Apple')
streamlit.write('The user entered ', fruit_choice)

import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# use the 'fruit_choice' variable to pass instead of hardcoding the value as 'Kiwi'
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

#streamlit.text(fruityvice_response.json()) # just writed the data to the screen - json as string to display

# use pandas package to normalize/flatten/parse the json data for fitting it into a dataframe/tabular form
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#  Display the fruityvice table on the page
streamlit.dataframe(fruityvice_normalized)

# Added code line to import snowflake python connector package or library
import snowflake.connector

# Added code lines to query Our Trial Account Metadata 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

# Query the data on snowflake table connected
my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchone()
# code line to display all the lines
my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains:")
# streamlit.text(my_data_row)

# Change the Streamlit Components to Make Things Look a Little Nicer
streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

# Add a Second Text Entry Box
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)


# Control of flow test 
# This will not work correctly, but just go with it for now
my_cur.execute"'insert into fruit_load_list values ('from streamlit')")
