# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st



st.sidebar.subheader('Table of contents')
st.sidebar.write('1. ','<a href=#case-study-on-the-correlation-between-happiness-factors-and-world-happiness>Introduction</a>', unsafe_allow_html=True)
st.sidebar.write('2. ','<a href=#interactive-scatter-graph>Scatter graph</a>', unsafe_allow_html=True)
st.sidebar.write('3. ','<a>Other graphs</a>', unsafe_allow_html=True)
st.sidebar.write('4. ','<a>More graphs</a>', unsafe_allow_html=True)

happiness2021 = pd.read_csv("C:\\Users\\r3ktmlg\\world-happiness-report-2021.csv")
happiness = pd.read_csv("C:\\Users\\r3ktmlg\\world-happiness-report.csv")

countries_dict = [country for country in happiness["Country name"].unique() if country in happiness2021["Country name"].values]

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

st.title("Case study on the correlation between happiness factors and world happiness")

st.markdown("#### In this case study, we explore how factors of world happiness for instance Log GDP per capita will affect the overall happiness score of different countries. We found many interesting observations while comparing different regions/countries' factors to each other. While I focus on China versus the United States, we also provide interactive graphs that allows you, the reader, to explore the data and make as many graphs as your heart desires. For example,below is a line graph of a few countries of interest to me! Later you will be able to add countries of interest to you!") 

spfrit = happy[happy["Country name"].isin(["Afghanistan","Italy","France", "China","Sweden", "United States"])]
fig1 = px.line(spfrit, 
        x="year", 
        y="Life Ladder", 
        color="Country name",
       title="Life score of countries across years")



fig1.update_traces(mode='markers+lines')



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

st.header("Interactive scatter graph")

st.markdown("#### Here is an interactive scatter graph that compares a happiness factor (e.g Log GDP per Capita) to the overall happiness value!! Click the select box to select a fappiness factor")

option_select = st.selectbox('Statistic to compare', ['Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='country name')



#TODO Add px.update for fig 3

fig3 = px.scatter(happy, "Life Ladder", 
           option_select, 
           hover_name = "Country name", 
           color = "Region", 
           color_discrete_sequence = px.colors.qualitative.Pastel,
           labels = {"Life Ladder" : "Happiness Value"},
           hover_data=["year"])



st.plotly_chart(fig3)

country = happy.loc[happy["Country name"].isin(["China", "United States"])]
country = pd.melt(country, id_vars=["Country name", "year"], value_vars=country.drop(["Country name", "year"], axis=1).columns)

fig7_2 = px.line(country.loc[country["variable"] != "Healthy life expectancy at birth"], 
        x="year", 
        y="value", 
        color="variable", 
       title="Here, we see the values of different life ladder factors between " + "China" + " and " + "the United States",
       labels={"variable":"Happiness factors"},
       facet_col = "Country name",
       width = 800)
fig7_2.update_traces(mode='markers+lines')

st.plotly_chart(fig7_2)

st.markdown("#### As you can visualize, the United States has a significantly higher Log GDP per capita (around 10.9) than China does (9.3), there isn't that much of a difference between the other happiness factors other than the fact that the US has 0.5 less perception of corruption. Those two factors increase the average happiness score of the US to 7.1, which is 1.9 higher than China's average of 5.2. Have a try comparing other countries with another in the interactable boxes below!!! :)") 

st.subheader("Type 2 countries to compare their happiness factors")
option_country1 = st.text_input(label = "Country 1", value = "").title()

valid_countries = list(happy["Country name"].unique()) + [""] 

if option_country1 not in valid_countries:
    st.error(f"{option_country1} is not a valid option, it is either misspelled or no happiness data")

option_country2 = st.text_input(label = "Country 2", value = "").title()

if option_country2 not in valid_countries:
    st.error(f"{option_country2} is not a valid option, it is either misspelled or no happiness data")



country = happy.loc[happy["Country name"].isin([option_country1, option_country2])]
country = pd.melt(country, id_vars=["Country name", "year"], value_vars=country.drop(["Country name", "year"], axis=1).columns)

if(option_country1 == ""):
    option_country1 = "a country"
else:
    fig7 = px.line(country.loc[country["variable"] != "Healthy life expectancy at birth"], 
        x="year", 
        y="value", 
        color="variable", 
       title="Values of different life ladder factors between " + option_country1 + " and " + option_country2,
       labels={"variable":"Happiness factors"},
       facet_col = "Country name",
       width = 800)
    fig7.update_traces(mode='markers+lines')
    
    fig7_1 = px.line(country.loc[country["variable"] == "Healthy life expectancy at birth"], 
        x="year", 
        y="value", 
        color="variable", 
       title="Most correlated factor: Healthy life expectancy between " + option_country1 + " and " + option_country2,
       labels={"variable":"Happiness factors"},
       facet_col = "Country name")
    fig7_1.update_traces(mode='markers+lines')
    
    st.plotly_chart(fig7)
    st.plotly_chart(fig7_1)
    
    
    #fig7_1["Healthy life expectancy at birth"]


fig_pie_life = px.pie(pie_happy,
    names = "Region",
    values = "Life Ladder",
    color = "Region",
    title = "Pie chart of " + "Life Ladder" + " across Regions",
    hole = 0.95)

fig_pie_life.update_layout(title_font=dict(color="lightblue", size=20, family="Arial Black"))

fig_pie_life.update_layout(
    # Add annotations in the center of the donut pies.,
    annotations=[dict(text='<i>This pie chart shows if the total sum of the <br> score of the entire world is 100, <br> how much would the average of each region <br> have as  a share or percentage in the 100?</i>', x=0.5, y=0.5, font_size=13, showarrow=False)])


st.plotly_chart(fig_pie_life)

st.markdown("#### From the pie chart above, we can clearly see that Western Europe and North America and ANZ have the most percentage of the total happiness score! This means that on average, they are happier than an average person who lives in Sub-Saharan Africa (7.7%). However, whilst investigating this, there is a fatal flaw to the logic of the region grouping of this data. North America is grouped with ANZ (Australia and New Zealand) Which doesn’t make sense at all due to the two being 9,000 km apart from each other! It would be more sensible to put ANZ in their own region but even group the Americas together. Here! You can even try to compare different regions with different happiness factors in the interactive pie chart below! :) :)") 

st.subheader("Select a feature to display the pie chart")

option_select_pie = st.selectbox('', ["Select a value","Life Ladder",'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='bbb')



if(option_select_pie != "Select a value"):
    
    if(option_select_pie == "Generosity"):
        pyhappygen = pie_happy.copy()
        pyhappygen["newgen"] = pyhappygen["Generosity"] + 0.11
        
        fig_pie = px.pie(pyhappygen,
        names = "Region",
        values = "newgen",
        color = "Region",
        title = "Pie chart of " + option_select_pie + " across Regions",
        custom_data=["Generosity"],
        hole = 0.95)
        
        
        fig_pie.update_traces(hovertemplate = "Region:%{label} <br>Generosity: %{customdata[0][0]:.4f}", textinfo='percent+label')
        fig_pie.update_layout(showlegend=False)
    else:
        
        
        fig_pie = px.pie(pie_happy.apply(lambda x: f"{x:.4f}" if x.name == option_select_pie else x, axis=1),
        names = "Region",
        values = option_select_pie,
        color = "Region",
        title = "Pie chart of " + option_select_pie + " across Regions",
        hole = 0.95)
    
    
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(title_font=dict(color="lightblue", size=20, family="Arial Black"),showlegend=False)
    
    # Add annotations in the center of the donut pies.
    
    


    st.plotly_chart(fig_pie)
    


st.subheader("Select a feature to display the 'choropleth map'")

option_select_choro = st.selectbox('', ["Life Ladder",'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth','Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], key='ccc')

fig8 = go.Figure(data=go.Choropleth(locations=happy["CODE"],z=happy[option_select_choro], text = happy['Country name'], colorscale = px.colors.sequential.Aggrnyl))

st.plotly_chart(fig8)
