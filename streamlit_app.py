# Smoothie customization app with Streamlit
# Co-authored with CoCo
# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests
import os

cnx = st.connection("snowflake")


# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your Smoothie wil be", name_on_order)


session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME') ,col('SEaRCH_ON')  )
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect(
    "Choose upto 5 ingredients:", my_dataframe , max_selections=5
     
)
if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients , Name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order+  """')"""
    time_to_insert = st.button('Submit Order')  
    #st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
      
 

