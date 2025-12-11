# Belmont North Property Market Dashboard  
### Data Analysis & Interactive Streamlit Application

This project was completed as part of a data analysis interview task. It demonstrates the ability to:

- integrate external API data  
- clean and transform complex time-series datasets  
- build insightful visualizations  
- deliver an interactive dashboard using Streamlit  
- communicate findings clearly for non-technical audiences  

---

## 1. Project Overview  

The goal of this project is to analyse long-term property trends for **Belmont North, NSW**, using market data extracted from the Microburbs API Sandbox. The analysis focuses on:

- Median sell price trends  
- Indexed price growth vs regional benchmarks  
- Houses vs units performance  
- Rolling 12-month growth cycles  
- Key investment insights for property buyers  

The final deliverable is an **interactive Streamlit dashboard** that showcases data, insights, and visualizations in a way that is immediately useful to residential property investors.

---

## 2. Features of the Dashboard  

The Streamlit app is organised into three main analytical components:

### Tab 1 – Long-term Price Trends  
- Median sell price trend for Belmont North  
- Indexed growth comparison vs CR and SA3 benchmarks  
- Automatic calculation of CAGR and total growth  

### Tab 2 – Houses vs Units  
- Median price comparison over time  
- Structural divergence between houses and units  
- Investor insights on capital growth and affordability  

### Tab 3 – Rolling 12-Month Growth  
- Momentum analysis using rolling annual price changes  
- Suburb vs SA3 volatility comparison  
- Leading indicators of market cycles  

Each chart includes accompanying **insights text** that explains the meaning of the trend in plain English.

---

## 3. Tech Stack  

- **Python 3.10+**  
- **Pandas** for data cleaning & transformation  
- **Matplotlib / Seaborn** for visualisations  
- **Streamlit** for the interactive dashboard  
- **Requests** for API calls  
