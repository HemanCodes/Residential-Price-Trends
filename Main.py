import pandas as pd
import streamlit as st
import plotly.express as px

#setting streamlit page configurations
st.set_page_config(page_title = 'Residential Price Trends', layout = 'wide')

#reading data from csv
data = pd.read_csv('/Users/hemantchaudhary/Developer/PortfolioProjects/coordinates.csv')

st.write('''
         # Residential Price Trends :chart_with_upwards_trend:
         ''')
st.write('This tool provides a comprehensive view of residential property price trends across various cities in India. We have taken a sample-set of 50 cities from different states and segments (Tier 1, Tier 2, and Tier 3). The dasbhoard offers a deeper understanding of market patterns and provides insights into price dynamics by enabling users to compare price trends between cities and apartment sizes (1BHK, 2BHK, 3BHK). This tool equips users with a data-driven approach to understanding the evolving real estate markets in India.')

#creating page layout
col1, col2 = st.columns(2, gap = 'large', vertical_alignment = 'top', border = True)

with col1:
    #Selecting City Name
    city_select = st.selectbox(
    label = 'Select City Name',
    options = ['--- Select City ---'] + list(data['city'].unique()),
    index = 0, 
    label_visibility = 'collapsed'
    )

    if city_select == '--- Select City ---' or city_select == None:
        st.map(
            data, 
            zoom = 3.3,                          #showing zoomed-out map of India
            height = 485
        )
    else:
        st.map(
            data = data[data['city'] == city_select],       #showing selected city on map
            height = 450, 
            zoom = 10
        )
        

with col2:
    tab1, tab2 = st.tabs(['Price Comparision based on Appartment Size', 'Price Comparision based on City Average'])
   
    with tab1:
        size_select = st.pills(
        label = 'Select Appartment Size',
        options = ['onebhk', 'twobhk', 'threebhk'], 
        selection_mode = 'multi',
        default = ['threebhk'],
        )

        st.line_chart(
            data = data[data['city'] == city_select],
            x = 'quarter', 
            y = size_select, 
            x_label='Quarter', 
            y_label='Per fq. ft. price', 
            color=None, 
            height= 400, 
            use_container_width= True
        )
    
    with tab2:
        st.markdown(
        "<p style='text-align: center; font-size: 14px; color: gray;'><em>Start comparing by selecting cities from the legend</em></p>",
            unsafe_allow_html = True
        )
        # Create the line plot
        fig = px.line(
            data,
            x='quarter',              
            y='composite',            
            color='city',             # Differentiate by city
            height = 445
        )

        #adding range slider
        fig.update_xaxes(
            rangeslider=dict(
                visible=True,  # Enable the range slider
                bordercolor = 'Black',
                borderwidth = 1,
                thickness = 0.05,
            ),

            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(count=5, label='5Y', step='year', stepmode='backward'),
                    dict(count=10, label='10Y', step='year', stepmode='backward'),
                    dict(label='All', step='all')
                ])
            )
        )

        #tweeking city legend
        for trace in fig.data:
            if trace.name not in ['Delhi']:
                trace.visible = 'legendonly'

        # Display the chart in Streamlit
        st.plotly_chart(fig)

st.write('---')                     #creating a horizontal divider

col1, col2 = st.columns(2, gap = 'small', vertical_alignment = 'top')

# tier1 = data[data['city'].isin(['Delhi', 'Pune'])]
# st.write(tier1)


with col1:
    st.segmented_control(
        label = 'N/A',
        options = ['Tier-1', 'Tier-2', 'Tier-3'], 
        selection_mode = 'single',
        default = 'Tier-1', 
        label_visibility = 'collapsed'
    )

    st.bar_chart(
    data = data[data['city'] == 'Delhi'], 
    x = 'quarter', 
    y = '%change_onebhk', 
    )
    




