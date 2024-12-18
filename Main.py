import pandas as pd
import streamlit as st
import plotly.express as px

#setting streamlit page configurations
st.set_page_config(page_title = 'Residential Price Trends', layout = 'wide')

#reading data from csv
data = pd.read_csv('geocode_coordinates.csv')
data['quarter'] = pd.to_datetime(data['quarter'])            #converting quarter column to datetime format

#adding dashboard title and r=description
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

    #default map if no selection
    if city_select == '--- Select City ---':
        st.map(
            data, 
            zoom = 3.3,                                      #showing zoomed-out map of India
            height = 485
        )
    #map showing selected city
    else:
        st.map(
            data = data[data['city'] == city_select],       #showing selected city on map
            height = 450, 
            zoom = 10
        )
        

with col2:
    tab1, tab2 = st.tabs(['Price Comparision based on Appartment Size', 'Price Comparision based on City Average'])
   
   #tab showing comparision between different appartment size
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
    #tab showing comparision between different cities
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

        #adding range slider and selector
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

        #hiding all traces expept Delhi
        for trace in fig.data:
            if trace.name != 'Delhi':
                trace.visible = 'legendonly'

        # Display the chart in Streamlit
        st.plotly_chart(fig)

st.write('---')                                     #creating a horizontal divider

# -------------- work in Progress / more features coming ------------------

Tier_1_cities = ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']
Tier_2_cities = ['Bhopal', 'Bhubaneswar', 'Chandigarh', 'Coimbatore', 'Dehradun', 'Faridabad', 'Gandhinagar', 'Ghaziabad', 'Greater Noida', 'Gurugram', 'Indore', 'Jaipur', 'Kanpur', 'Kochi', 'Lucknow', 'Nagpur', 'Nashik', 'Navi Mumbai', 'Noida', 'Patna', 'Pimpri Chinchwad', 'Raipur', 'Rajkot', 'Ranchi', 'Surat', 'Thane', 'Vadodara', 'Vijayawada', 'Vizag']
Tier_3_cities = ['Bhiwadi', 'Bidhan Nagar', 'Chakan', 'Guwahati', 'Howrah', 'Kalyan Dombivli', 'Ludhiana', 'Meerut', 'Mira Bhayander', 'New Town Kolkata', 'Panvel']


col3, col2 = st.columns([6.5, 3.5], gap = 'small', vertical_alignment = 'top', border = True)

with col3:
    col5, col6, col7 = st.columns([3.1, 3, 3.8], gap = 'small', border = True, vertical_alignment = 'bottom')
    
    with col5:
        st.write('###### Tier based price trends')
        tier_select = st.segmented_control(
            label = 'N/A',
            options = ['Tier_1', 'Tier_2', 'Tier_3'], 
            selection_mode = 'single',
            default = 'Tier_1', 
            label_visibility = 'collapsed'
        )
        metric_delta = None
        if tier_select == 'Tier_1':
            selected_cities = Tier_1_cities 
            metric_delta = 'Constant Growth pattern'
        elif tier_select == 'Tier_2':
            selected_cities = Tier_2_cities
            metric_delta = 'Recent growth surge'
        elif tier_select == 'Tier_3':
            selected_cities = Tier_3_cities
            metric_delta = '-Low growth + recent slowdown'
  
    with col6:
        quarter_select = st.segmented_control(
            label = 'Select Quarter', 
            options = ['Q1', 'Q2', 'Q3', 'Q4'], 
            selection_mode = 'single', 
            default = 'Q2', 
            help = 'Percentage growth between the selected quarters of consecutive years'
        )
        
        if quarter_select == 'Q1':
            selected_quarter = 3
        elif quarter_select == 'Q2':
            selected_quarter = 6
        elif quarter_select == 'Q3':
            selected_quarter = 9
        elif quarter_select == 'Q4':
            selected_quarter = 12
        
        filtered_data = (
            data[
                data['city'].isin(selected_cities) 
                & data['quarter'].dt.month.isin([selected_quarter])
                ]
            .groupby('quarter')[['%change_onebhk', '%change_twobhk', '%change_threebhk']]
            .mean()
            .assign(avg_YoY_change = lambda x: x.mean(axis = 1))
            .round(2)
            .reset_index()
        )
        
    with col7:
        st.metric(
            label = 'Average return of last 5 years',
            value = filtered_data[['avg_YoY_change']].tail(5).mean(axis = 0).round(2),
            delta = metric_delta
        )

        

    fig1 = px.bar(
        filtered_data, 
        x = 'quarter', 
        y = 'avg_YoY_change', 
        labels = {'quarter' : 'Quarter', 'avg_YoY_change' : '% change QoQ'}, 
        height = 370, 
        color = 'avg_YoY_change', 
        color_continuous_scale = ['Red', 'Green']
    )
    fig1.update_layout(
        bargap=0.25,
    )
    fig1.update_coloraxes(
        cmid = 0, 
        cmin = -1, 
        cmax = 6
    )

    st.plotly_chart(
        fig1, 
        use_container_width = False
    )