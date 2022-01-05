# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.graph_objects as go
import streamlit as st

st.sidebar.subheader('Table of contents')
st.sidebar.write('1. ','<a>Introduction</a>', unsafe_allow_html=True)
st.sidebar.write('2. ','<a>Line graph of happiness</a>', unsafe_allow_html=True)
st.sidebar.write('3. ','<a>Other graphs</a>', unsafe_allow_html=True)
st.sidebar.write('4. ','<a>More graphs</a>', unsafe_allow_html=True)

happiness2021 = pd.read_csv("world-happiness-report-2021.csv")
happiness = pd.read_csv("world-happiness-report.csv")

countries_dict = [country for country in happiness["Country name"].unique() if country in happiness2021["Country name"].values]

mapdata = gpd.read_file("custom.geo.json")

happiness = happiness.loc[happiness["Country name"].isin(countries_dict)].reset_index(drop=True)

happiness2021["year"] = 2021

happiness2021.rename({"Ladder score":"Life Ladder",
                      "Healthy life expectancy":"Healthy life expectancy at birth",
                      "Logged GDP per capita":"Log GDP per capita"}, axis=1, inplace=True)

columns = list(happiness.drop(["Positive affect", "Negative affect"], axis=1).columns) + ["Regional indicator"]

happy = pd.concat([happiness, happiness2021[columns]])

regional_dict = {k:v for k,v in zip(happiness2021["Country name"], happiness2021["Regional indicator"])}

happy["Region"] = happy["Country name"].replace(regional_dict)

happy.drop(["Positive affect","Negative affect","Regional indicator"], axis = 1, inplace = True)

spfrit = happy[happy["Country name"].isin(["Afghanistan","Italy","France", "China","Sweden", "United States"])]
fig1 = px.line(spfrit, 
        x="year", 
        y="Life Ladder", 
        color="Country name", 
        text="Life Ladder",
       title="Life score of countries across years")

st.title("How different values within a country correlates to its happiness score")


fig2 = px.bar(spfrit, 
       x="year",
       y="Life Ladder",
       color="Country name",
       animation_frame = "year",
       barmode="group")



happy_c = happy.corr().sort_values("Life Ladder", ascending = False)
ladder_c = happy_c["Life Ladder"]

def scatter(df,xAxis,yAxis):
    df.plot(kind = "scatter", x = xAxis, y = yAxis)

pie_happy = happy.groupby(["Region"]).mean().reset_index().drop(["year"],axis=1)



happy_no_region = happy.drop(["Region"], axis = 1)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

country_code = {k:v for k,v in zip(df["COUNTRY"], df["CODE"])}

happy["CODE"] = happy["Country name"].replace(country_code)



st.plotly_chart(fig1)
#st.plotly_chart(fig2)

option_select = st.selectbox('Statistic to compare', ['Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='country name')

#TODO Add px.update for fig 3

fig3 = px.scatter(happy, "Life Ladder", 
           option_select, 
           hover_name = "Country name", 
           color = "Region", 
           color_discrete_sequence = px.colors.qualitative.Pastel,
           labels = {"Life Ladder" : "Happiness Value"})
st.plotly_chart(fig3)


st.subheader("Type a country to display the line graph of happiness factors")
option_country = st.text_input("")
country = happy.loc[happy["Country name"] == option_country]
country = pd.melt(country, id_vars=["Country name", "year"], value_vars=country.drop(["Country name", "year"], axis=1).columns)

grouped = happy.groupby(['Country name']).mean().sort_values("Life Ladder", ascending = False)
happy.groupby(["Country name"]).sum()

if(option_country == ""):
    option_country = "a country"
else:
    fig7 = px.line(country, 
        x="year", 
        y="value", 
        color="variable", 
       title="Values of different life ladder factors in " + option_country,
       labels={"variable":"Happiness factors"},
       log_y=True)
    fig7.update_traces(mode='markers+lines')
    st.plotly_chart(fig7)

        

st.subheader("Select a feature to display the pie chart")

option_select_pie = st.selectbox('', ["Select a value","Life Ladder",'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='bbb')



if(option_select_pie != "Select a value"):
    fig_pie = px.pie(pie_happy,
    names = "Region",
    values = option_select_pie,
    color = "Region",
    title = "Pie chart of " + option_select_pie + " across Regions",
    hole = 0.0)

    fig_pie.update_layout(title_font=dict(color="lightblue", size=20))
    st.plotly_chart(fig_pie)


st.subheader("Select a feature to display the 'choropleth map'")

option_select_choro = st.selectbox('', ["Life Ladder",'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='ccc')

fig8 = go.Figure(data=go.Choropleth(locations=happy["CODE"],z=happy[option_select_choro], text = happy['Country name'], colorscale = px.colors.sequential.Aggrnyl))

st.plotly_chart(fig8)
