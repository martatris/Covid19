COVID-19 Trend Dashboard
========================

An interactive and comprehensive dashboard built with Python, Pandas, Dash, and Plotly to visualize and analyze global COVID-19 data.
This version includes additional visualizations such as interactive maps, bar charts, and scatter plots, along with dynamic data cards.

Features
--------
- Interactive Choropleth Map — Visualize the global spread of COVID-19.
- Dynamic Metric Selector — Choose between Confirmed, Deaths, Recovered, and Active cases.
- Summary Cards — Display global totals for confirmed, deaths, recovered, and active cases.
- Top 10 Countries Bar Chart — Compare countries with the highest number of cases.
- Scatter Plot — Explore the relationship between recovered and death cases.
- Responsive Layout — Automatically adapts to different screen sizes.
- Smooth UI — Styled summary cards and hover effects using custom CSS.

Tech Stack
----------
- Python 3.9+
- Pandas — Data manipulation and cleaning
- Plotly — Interactive visualization and mapping
- Dash — Web application framework for Python
- PyCountry — ISO-3 country code mapping for accurate geolocation

Dataset
-------
The dataset used is: `country_wise_latest.csv`

Columns include:
- Country/Region
- Confirmed
- Deaths
- Recovered
- Active
- Death Rate
- Recovery Rate

Installation & Setup
--------------------
1. Clone this repository
   git clone https://github.com/<your-username>/covid19-trend-dashboard.git
   cd covid19-trend-dashboard

2. Create a virtual environment (optional but recommended)
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows

3. Install dependencies
   pip install -r requirements.txt

   If you don’t have one yet, create it with:
   pip install dash plotly pandas pycountry
   pip freeze > requirements.txt

4. Run the dashboard
   python Covid19.py

5. Open your browser
   http://127.0.0.1:8050/

Project Structure
-----------------
covid19-trend-dashboard/
│
├── Covid19.py               # Main dashboard app
├── country_wise_latest.csv  # Dataset
├── assets/
│   └── style.css            # Custom CSS for cards and layout
└── README.txt               # Project documentation

Future Enhancements
-------------------
- Add daily trend time series per country
- Integrate real-time API (Johns Hopkins / WHO)
- Add vaccination data visualization
- Dark mode and mobile-first design
- Deploy via Render, Vercel, or Heroku

Author
------
Triston Marta
Data Science and Statistics
