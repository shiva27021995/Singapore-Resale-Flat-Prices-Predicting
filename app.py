import pickle
import pandas as pd
import numpy as np
import streamlit as st

def load_model(model_file):
    with open(model_file, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

def convert_storey_range(storey_range):
    return (int(storey_range.split(' TO ')[0]) + int(storey_range.split(' TO ')[1])) / 2

flat_type_mapping = {'1 ROOM': 1,'2 ROOM': 2,'3 ROOM': 3,'4 ROOM': 4,'5 ROOM': 5,'EXECUTIVE': 6,'MULTI GENERATION': 7}

month_mapping = {
  'January': 1,'February': 2,'March': 3,'April': 4,'May': 5,'June': 6,'July': 7,'August': 8,'September': 9,'October': 10,'November': 11,'December': 12
}

storey = ['01 TO 03', '01 TO 05', '04 TO 06', '06 TO 10', '07 TO 09',
          '10 TO 12', '11 TO 15', '13 TO 15', '16 TO 18', '16 TO 20',
          '19 TO 21', '21 TO 25', '22 TO 24', '25 TO 27', '26 TO 30',
          '28 TO 30', '31 TO 33', '31 TO 35', '34 TO 36', '36 TO 40',
          '37 TO 39', '40 TO 42', '43 TO 45', '46 TO 48', '49 TO 51']


all_towns = ['ANG MO KIO','BEDOK','BISHAN','BUKIT BATOK','BUKIT MERAH',
            'BUKIT PANJANG','BUKIT TIMAH','CENTRAL AREA','CHOA CHU KANG',
            'CLEMENTI','GEYLANG','HOUGANG','JURONG EAST','JURONG WEST',
            'KALLANG/WHAMPOA','LIM CHU KANG','MARINE PARADE','PASIR RIS','PUNGGOL',
            'QUEENSTOWN','SEMBAWANG','SENGKANG','SERANGOON','TAMPINES',
            'TOA PAYOH','WOODLANDS','YISHUN']


all_flat_model = ['2-Room','3Gen','Adjoined Flat','Apartment','Dbss',
                  'Improved','Improved-Maisonette','Maisonette','Model A','Model A-Maisonette',
                  'Model A2','Multi Generation','New Generation','Premium Apartment','Premium Apartment Loft',
                  'Premium Maisonette','Simplified','Standard','Terrace','Type S1','Type S2']

def get_user_input():
    user_input = {}

    st.write("#### Enter the Details:")

    # Display "Month" as a dropdown with month names
    month = st.selectbox("Month", list(month_mapping.keys()))
    user_input['month'] = month_mapping[month]
    year = st.number_input("Year (YYYY)", min_value=1990, max_value=2023)

    user_input['floor_area_sqm'] = st.number_input("Floor Area (sqm)")
    user_input['lease_commence_date'] = st.number_input("Lease Commencement Year (YYYY)", min_value=1966, max_value=2023)

    user_input['remaining_lease'] = None
    user_input['year'] = year

    user_input['remaining_lease'] = user_input['lease_commence_date'] + 99 - user_input['year']

    # Display "storey_range" as a select box with input as "01 TO 03"
    storey_range = st.selectbox("Storey Range", storey)

    # Convert storey range to the average of the range
    user_input['storey_range'] = convert_storey_range(storey_range)

    # Display "flat_type" as a dropdown with user-friendly names
    flat_type = st.selectbox("Flat Type", list(flat_type_mapping.keys()))
    user_input['flat_type'] = flat_type_mapping[flat_type]

    town = st.selectbox("Town", all_towns)
    all_town_columns = []
    for i in all_towns:
        all_town_columns.append(f'town_{i}')

    for town_column in all_town_columns:
        if town_column != f'town_{town}':
            user_input[town_column] = 0
        else:
            user_input[f'town_{town}'] = 1


    flat_model = st.selectbox("Flat Model", all_flat_model)
    all_flat_model_columns = []
    for i in all_flat_model:
        all_flat_model_columns.append(f'flat_model_{i}')

    for flat_model_column in all_flat_model_columns:
        if flat_model_column != f'flat_model_{flat_model}':
            user_input[flat_model_column] = 0
        else:
            user_input[f'flat_model_{flat_model}'] = 1

    return user_input

def main():
    st.set_page_config(page_title="Singapore Resale Flat Price Prediction - Made by: Pranit Akhade",layout="wide",initial_sidebar_state="auto")

    st.title("Singapore Resale Flat Price Prediction")

    user_input_data = get_user_input()

    if st.button("Predict"):
        user_input_df = pd.DataFrame([user_input_data])
        loaded_model = load_model('Resale_Flat_Prices_Model_1.pkl')
        predicted_price = loaded_model.predict(user_input_df)
        st.write(f"### Predicted Resale Price: S$ {predicted_price[0]:.2f}")

if __name__ == "__main__":
    main()
     