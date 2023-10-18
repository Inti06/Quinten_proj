import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from app_p0 import Streamlit_Page0
#from app_p1 import Streamlit_Page1


st.set_page_config(
    page_title="Stocks prediction",  # Set the page title
    page_icon="📈",  # Set a custom page icon
    layout="wide",  # Use wide layout
    initial_sidebar_state="collapsed",  # Start with the sidebar collapsed
)

# Title
st.markdown(
    "<h1 style='text-align: center'>Stocks prediction</h1>", unsafe_allow_html=True
)

# Page selction
selected_page = st.sidebar.selectbox(
    "Go to Page",
    ["Portfolio", "Company"],
)

# Navigate to the selected page
if selected_page == "Portfolio":
    Streamlit_Page0().page_portfolio()

if selected_page == "Company":
     
    #import data
    data = pd.read_csv('/Users/etiennedufayet/Desktop/Cours/X4A/data_quinten/Quinten_proj/data/for_app.csv')

    #Create a list of all availables companies
    companies_list = data['symbol'].drop_duplicates().to_list()

    # Selection widget for companies
    company_input = st.selectbox("Company name", companies_list)



    ## Gather data from this company
    filtered_dataset = data[data['symbol']==company_input]
    filtered_dataset = filtered_dataset.sort_values(by='date')

    filtered_dataset['date'] = filtered_dataset['date'].apply(lambda x: x.split()[0] if ' ' in x else x)

    dates_without_last = filtered_dataset['date'].iloc[:-1]
    date_range = pd.to_datetime(dates_without_last)


    last_date = filtered_dataset['date'].iloc[-1]
    previous_date = filtered_dataset['date'].iloc[-2]
    dates_df = pd.DataFrame({'date': [previous_date, last_date]})
    predicted_date = pd.to_datetime(dates_df['date'])



    stock_prices_except_last = filtered_dataset['stockPrice'][:-1].to_numpy()

    stock_price_data = pd.Series(stock_prices_except_last, index=date_range)
    predicted_price = filtered_dataset['stockPrice'].iloc[-1]

    predicted_stock_price = pd.Series([stock_price_data[-1], predicted_price], index=predicted_date)
    merged_stock_prices = pd.DataFrame({'Past stock price': stock_price_data, 'Futur stock price':predicted_stock_price})

    grossprofit = filtered_dataset['grossProfitRatio'][:-1].to_numpy()
    gross_profit = pd.Series(grossprofit, index=date_range)

    ebitda = filtered_dataset['ebitdaratio'][:-1].to_numpy()
    ebitda_data = pd.Series(ebitda, index=date_range)

    NIR = filtered_dataset['netIncomeRatio'][:-1].to_numpy()
    NIR_data = pd.Series(NIR, index=date_range)

    LTD = filtered_dataset['netDebtToEBITDA'][:-1].to_numpy()
    LTD_data = pd.Series(LTD, index=date_range)


    st.title(f"{company_input}")

    ##### def a function
    def compute_stats(data, data_name, date_range, start_time): 
        data_evolution = pd.Series([data.iloc[-(start_time+1)], data.iloc[-1]], index=[date_range.iloc[-(start_time+1)], date_range.iloc[-1]])

        if start_time>1: 
            data_list = [data.iloc[-(start_time+1)]]
            index_list = [date_range.iloc[-(start_time+1)]]
            for i in np.arange(1, start_time+1): 
                data_list.append(data.iloc[-(start_time+1)]+i*(data.iloc[-1]-data.iloc[-(start_time+1)])/(start_time+1))
                index_list.append(date_range.iloc[-(start_time+1-i)])
            
            data_evolution = pd.Series(data_list, index = index_list) 

        
        merged_data = pd.DataFrame({data_name: data, data_name+" evolution": data_evolution})
        date_str = date_range.iloc[-(start_time+1)].strftime("%B %Y")
        today_data_value = data[-1]
        start_time_data_value = data.iloc[-(start_time+1)]

        data_delta = today_data_value - start_time_data_value
        growth_percentage = (today_data_value - start_time_data_value)/start_time_data_value*100

        return(merged_data, data_delta, growth_percentage, date_str)


    ##### Stock price container
    st.write(f"Explore financial KPI of {company_input}.")
    today_date = date_range.iloc[-1].strftime("%B %Y")
    st.write(today_date)


    col1, col2 = st.columns([3, 2])
    col1.subheader("Past stock price")
    col1.line_chart(
    merged_stock_prices, x=None, y=["Past stock price", "Futur stock price"], color=["#FF0000", "#0000FF"]  
    )
    date_str = predicted_date.iloc[-1].strftime("%B %Y")
    col2.subheader('Futur stock price')

    stock_delta = np.round(predicted_stock_price.iloc[-1] - predicted_stock_price.iloc[-2], 2)

    col2.metric(label= f"{date_str}", value=f"${predicted_price:,.2f}", delta=stock_delta)

    ######### TABS

    tab1, tab2, tab3, tab4 = st.tabs(["Gross profit", "EBITDA", "Net income ratio", "Long term debt"])

    #### TAB 1
    tab1.subheader("Gross profit evolution")

    col1, col2 = tab1.columns([3, 2])

    col2.subheader("Evolution")


    key1 = "slider1" 
    start_time_1 = col2.slider(
        "Number of quarters ",
        1, 
        len(gross_profit),
        value=1,
        key=key1
        )


    merged_gross_profit, gross_profit_delta, growth_percentage_1, date_str_1 = compute_stats(gross_profit, "Gross profit", date_range, start_time_1)

    col1.line_chart(
    merged_gross_profit, x=None, y=["Gross profit", "Gross profit evolution"], color=["#FF0000", "#0000FF"]
    )
    col2.metric(label= f"Between today and {date_str_1}", value=f"{growth_percentage_1:,.2f}%", delta= f"{np.round(gross_profit_delta, 2)}", delta_color='off')




    ### TAB 2
    tab2.subheader("EBITDA")

    col3, col4 = tab2.columns([3, 2])

    col4.subheader("Evolution")

    key2 = "slider2"
    start_time_2 = col4.slider(
        "Number of quarters ",
        1, 
        len(ebitda_data),
        value=1,
        key=key2
        )

    merged_ebitda, ebitda_delta, growth_percentage_2, date_str_2 = compute_stats(ebitda_data, "EBITDA", date_range, start_time_2)

    col3.line_chart(
    merged_ebitda, x=None, y=["EBITDA", "EBITDA evolution"], color=["#FF0000", "#0000FF"]
    )
    col4.metric(label= f"Between today and {date_str_2}", value=f"{growth_percentage_2:,.2f}%", delta= f"${np.round(ebitda_delta, 2)}", delta_color='off')

    tab4.subheader("Long term debt")


    ### TAB 3
    tab3.subheader("Net income ratio")

    col5, col6 = tab3.columns([3, 2])

    col6.subheader("Evolution")

    key3 = "slider3"
    start_time_3 = col6.slider(
        "Number of quarters ",
        1, 
        len(NIR_data),
        value=1,
        key=key3
        )

    merged_NIR, NIR_delta, growth_percentage_3, date_str_3 = compute_stats(NIR_data, "Net Income Ratio", date_range, start_time_3)

    col5.line_chart(
    merged_NIR, x=None, y=["Net Income Ratio", "Net Income Ratio evolution"], color=["#FF0000", "#0000FF"]
    )
    col6.metric(label= f"Between today and {date_str_3}", value=f"{growth_percentage_3:,.2f}%", delta= f"${np.round(NIR_delta, 2)}", delta_color='off')


    ### TAB 4
    col7, col8 = tab4.columns([3, 2])

    col8.subheader("Evolution")

    key4 = "slider4"
    start_time_4 = col8.slider(
        "Number of quarters ",
        1, 
        len(LTD_data),
        value=1,
        key=key4
        )

    merged_LTD, LTD_delta, growth_percentage_4, date_str_4 = compute_stats(LTD_data, "Long term debt", date_range, start_time_4)

    col7.line_chart(
    merged_LTD, x=None, y=["Long term debt", "Long term debt evolution"], color=["#FF0000", "#0000FF"]
    )
    col8.metric(label= f"Entre aujourd'hui et {date_str_4}", value=f"{growth_percentage_4:,.2f}%", delta= f"${np.round(LTD_delta, 2)}", delta_color='off')

