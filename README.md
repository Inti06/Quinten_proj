# Stock Price Prediction Project

## Project Overview

Welcome to the Stock Price Prediction project repository. This project is dedicated to predicting quarterly stock price movements based on historical financial data. We use panel data from different stocks, including accounting measures such as earnings per share (EPS), price-to-book ratio, and more, to predict the quarterly stock prices for the next quarter. Additionally, we have developed an app that displays these predicted prices in a dashboard and automatically manages portfolio weights.

## Data Source

- Data: Historical quarterly fundamental data from 1995 for 585 Euronext stocks.
- Missing Data: The dataset contains a significant number of missing values, both in the feature variables and the dependent variable (stock price).

## Data Preprocessing

### Imputation

The challenge with abundant missing data led us to employ the following imputation strategy:

- Missing values were imputed by calculating the average of each column, grouped by the specific stock.
- Stocks with insufficient data to compute the column average were removed from the dataset.

### Data Trimming

To make the dataset more manageable and relevant, we decided to exclude data before the year 2010. This process resulted in a substantial reduction in dataset size, from approximately 200,000K rows to around 20,000K rows.

## Repository Structure

- `data/`: This directory contains the raw data (not provided) used in the project.
- `notebooks/`: The jupyter notebook is available in this directory for data exploration, preprocessing, and model development.
- `app/`: The code for the web application, which enables visualization of predicted stock prices in a dashboard and portfolio weight management, is stored here.
- `requirements.txt`: The list of Python packages and dependencies required to run this project is outlined in this file.
- `README.md`: This document serves as the main README for the project.

## Disclaimer

Please note that this project is intended for educational and demonstration purposes. Predicting stock prices is a complex task, and this project does not guarantee profitable investment decisions.


