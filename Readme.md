# Residential Price Trends Dashboard

An interactive web application that visualizes residential property price trends across Indian cities, featuring geographical mapping, dynamic trend analysis, and future price forecasting.

## Features

- **Geocode Coordinates**:
  - Fetches geographical coordinates (latitude and longitude) for cities using the `geopy` library and stores them in a CSV file.

- **Streamlit Dashboard**:
  - **City Map**:
    - Displays a map of India with zoomed-in views for selected cities.
  - **Price Comparison**:
    - Compares residential prices based on apartment size (1BHK, 2BHK, 3BHK) or city averages.
  - **Interactive Filters**:
    - Includes time range sliders for filtering price trends.
  - **Forecasted Growth**:
    - Provides future price trend predictions based on historical data.
    - Enables city-level forecasting, offering insights into potential investment opportunities.
    - Displays projected percentage growth over the next four quarters.

## Installation

### Prerequisites

- Python 3.8 or higher
- Required libraries: `pandas`, `geopy`, `streamlit`, `plotly`

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/HemanCodes/Residential-Price-Trends.git
   cd Residential-Price-Trends

	2.	Install dependencies:

pip install -r requirements.txt

	3.	Run the application:

streamlit run Main.py

Access the dashboard at http://localhost:8501 in your web browser.

Usage
	1.	City Map:
	•	Select a city from the dropdown to view its location on the map.
	2.	Price Comparison:
	•	Choose apartment sizes or cities to compare their price trends.
	3.	Interactive Filters:
	•	Adjust the time range slider to filter price trends for the desired period.
  4. Forecasted Growth:
  • Select a city and view projected price growth over the next four quarters.
  • Compare historical and forecasted trends using visual plots.

Data Sources
	•	Residential property price data sourced from National Housing Bank.
	•	Geographical coordinates obtained using the geopy library.
  • Forecasting model leverages historical prices clubbed with ARIMA time-series forecasting model

Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

Contact

For any inquiries or feedback, please contact HemanCodes.

Author
Hemant Chaudhary