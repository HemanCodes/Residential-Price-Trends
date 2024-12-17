Residential Price Trends Dashboard

An interactive web tool for visualizing residential property price trends across Indian cities, with geographical mapping and dynamic trend analysis.

Features
	•	Geocode Coordinates:
	•	Fetches geographical coordinates (latitude and longitude) for cities using the geopy library and stores them in a CSV file.
	•	Streamlit Dashboard:
	•	City Map: Displays a map of India with zoomed-in views for selected cities.
	•	Price Comparison: Compares residential prices based on apartment size (1BHK, 2BHK, 3BHK) or city averages.
	•	Interactive Filters: Includes time range sliders for filtering price trends.

 Setup

Prerequisites
	•	Python 3.8+
	•	Required libraries: pandas, geopy, streamlit, plotly

Installation
	1.	Clone the repo and install dependencies:
       git clone <repo-link>
       cd <project-folder>
       pip install pandas geopy streamlit plotly
	2.  Run the coordinate processing script:
       python geocode_coordinates.py
	3.	Run the Streamlit app:
       streamlit run app.py

Data Format
	•	Input CSV (Residex.csv):
Columns: city, quarter, onebhk, twobhk, threebhk, composite.
	•	Output CSV (coordinates.csv):
Adds latitude and longitude.

Example
	1.	Select a city from the dropdown.
	2.	Choose apartment size for price comparison.
	3.	Use the slider to filter by time range.


Author
Hemant Chaudhary