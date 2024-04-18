import streamlit as st
import webbrowser
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import TargetEncoder
from sklearn.preprocessing import StandardScaler

# loading the dataframe
df = pd.read_csv('kaggle-indian-agriculture.csv')
# making all the labels of the df to lowercase for better usability
df = df.apply(lambda x: x.astype(str).str.lower() if x.dtype == "object" else x)

# dropping all null values
df1 = df.dropna(axis=0)


# making the Production values consistent to one measurement
df1 = df1[~df1['Production Units'].str.contains("Nuts", case=False)]
bales = df1['Production Units'] == 'bales'
df1.loc[bales, 'Production'] *= 0.22
df1.loc[bales, 'Production Units'] = 'tonnes'

# dropping the irrelevant features as "Area Units" and "Production Units" are same throughout
df2 = df1.drop(labels=["Area Units", "Production Units", "Year"], axis=1)


# removing the duplicates with respect to District, Season and Crop in the df
no_duplicates = df2.copy()
no_duplicates[['Area', 'Production', 'Yield']] = no_duplicates.groupby(['District', 'Season', 'Crop'])[['Area', 'Production', 'Yield']].transform('mean')
no_duplicates.drop_duplicates(subset=['District', 'Season', 'Crop'], inplace=True)

# reset the indices after initial preprocessing
no_duplicates = no_duplicates.reset_index(drop=True)

# splitting the dataframe into target and independent features
X = no_duplicates.drop(['Yield'], axis=1)
y = no_duplicates['Yield']

numeric_columns = X.select_dtypes(exclude='object').columns.tolist()
categorical_columns = X.select_dtypes(include='object').columns.tolist()

# using target encoder to encode the categorical data
target_encoder = TargetEncoder(random_state=42)
target_encoder.fit(X[categorical_columns], y)
tar_enc = target_encoder.transform(X[categorical_columns])

tar_enc_df = pd.DataFrame(tar_enc, columns=categorical_columns)

tar_enc_df = pd.concat([tar_enc_df, X[numeric_columns]], axis=1)
tar_enc_df = pd.concat([tar_enc_df, y], axis=1)

# production can determined from area and yield so this can be dropped
# production is being dropped as this is the way yield is calculated
# yield = production/area
# so if the model can predict yield from area then production can be estimated through simple math as well

tar_enc_df_prod = tar_enc_df.drop(['Production'], axis=1)

# scaling the obtained numerical values
x = tar_enc_df_prod.drop(['Yield'], axis=1)
y = tar_enc_df_prod['Yield']
scaler = StandardScaler()
scaler.fit(x)

scaled_df = pd.DataFrame(scaler.transform(x))
scaled_df.columns = x.columns.tolist()
scaled_df = pd.concat([scaled_df, y], axis=1)

#removing the outliers
from scipy.stats import zscore
df_zscore = scaled_df.apply(zscore)
thresh = 3

outliers = scaled_df[df_zscore.abs() > thresh].any(axis=1)
without_outliers = scaled_df[~outliers]

# reset the indices after initial preprocessing
without_outliers = without_outliers.reset_index(drop=True)

# splitting the without_outliers dataframe again into target and independent variables
X = without_outliers.drop(labels=['Yield'], axis=1)
y = without_outliers['Yield']

# splitting into test and train
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# choosing random forest regressor to train the model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

rfr = RandomForestRegressor(n_estimators=100, random_state=42)
rfr.fit(X_train,y_train)

y_pred1 = rfr.predict(X_test)


# gui
st.set_page_config(page_title="Yield Estimation", page_icon="leaf.png")
st.title('Your Crop Yield Estimation')

st.caption('Drop in Your Input')
state = st.text_input("Enter your state")
district = st.text_input("Enter your district")
crop = st.text_input("Enter the name of the crop")
season = st.selectbox("Select the season", ["Kharif", "Rabi", "Zaid", "Whole Year"])
area = st.number_input("Enter the area of land (in hectares)", min_value=0.0)
units = st.radio("Select area units", ["Hectares", "Acres"])

if units == "Acres":
    area *= 0.4  # Convert acres to hectares

if st.button("Predict"):
    user_input = pd.DataFrame({
        "State": [state.lower()],
        "District": [district.lower()],
        "Crop": [crop.lower()],
        "Season": [season.lower()],
        "Area": [area]
    })


    # preprocessing the user inputs
    user_categorical = user_input.select_dtypes(include='object').columns.tolist()

    user_enc = target_encoder.transform(user_input[user_categorical])
    user_input_enc = pd.DataFrame(user_enc, columns=categorical_columns)
    user_input_enc = pd.concat([user_input_enc, user_input['Area']], axis=1)

    user_scaled = pd.DataFrame(scaler.transform(user_input_enc))
    user_scaled.columns = user_input_enc.columns.tolist()

    predicted_yield = rfr.predict(user_scaled)
    predicted_production = predicted_yield * user_input['Area'][0]

    rounded_yield = round(predicted_yield[0], 3)
    rounded_production = round(predicted_production[0], 3)

    st.write(f"Your estimated yield is ***{rounded_yield:.3f}*** tonnes per hectare")
    st.write(f"If the odds are on your side, your production would be ***{rounded_production:.3f}*** tonnes!")

    def preprocess_data(df, thresh=0.3):
        graph_df = df.copy()
        scaler = StandardScaler()  # Use StandardScaler for z-score
        df_zscore = pd.DataFrame(scaler.fit_transform(graph_df))
        outliers = df_zscore.abs() > thresh
        graph_df = graph_df[~outliers.any(axis=1)]
        graph_df = graph_df.reset_index(drop=True)
        return graph_df

    def generate_scatter_plot(graph_df, y, predicted_production, predicted_yield):
        y_new = y.sample(n=len(graph_df))
        y_new = y_new.reset_index(drop=True)
        y_new = np.sort(y_new)

        fig = go.Figure()  # Create an empty figure

        fig.add_trace(go.Scatter(x=graph_df['Production'], y=y_new, mode='markers', marker=dict(color='#63b077', opacity=0.5)))
        fig.add_trace(go.Scatter(x=predicted_production, y=predicted_yield, mode='markers', marker_color="black", text="This is You!"))

        return fig

    st.header(f"Where you stand !")
    graph_df = preprocess_data(tar_enc_df)  # Assuming tar_enc_df contains your data
    fig = generate_scatter_plot(graph_df, y, predicted_production, predicted_yield)
    st.plotly_chart(fig)

if st.button("Back to Home"):
    webbrowser.open_new("http://localhost:3000")
