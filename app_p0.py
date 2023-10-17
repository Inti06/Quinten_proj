import streamlit as st
import pandas as pd
import plotly.graph_objects as go


class Streamlit_Page0:
    def __init__(self):
        # Initialize the Streamlit app and class attributes
        self.data = pd.read_csv("data_test.csv", header=0) # dataset
        self.selected_quarter = None # quarter selection for prediction
        self.selected_nb_companies = None
        self.month = None # month associated with the prediction quarter
        self.year = None # year associated with the prediction quarter
        self.df_portfolio = pd.DataFrame()

    def update_data(self):
        # Define the selectboxes accordingly to the data
        id_quarters = 'Q'+ str((self.data['quarter']//3) + 1) + str(self.data['year'])
        self.data['id_quarters'] = id_quarters
        self.selected_quarter = st.selectbox('Select Quarter', self.data['id_quarters'].unique())
        self.selected_nb_companies = st.selectbox('Select Portfolio Size', list(range(1, 30)))
        self.month = self.data[self.data['id_quarters']==self.selected_quarter]['quarter'].values[0]
        self.year = self.data[self.data['id_quarters']==self.selected_quarter]['year'].values[0]
        
        # compute the stock price evolution
        prev_month = self.month - 3
        # anomalies in month : 
        if prev_month == 0 : prev_month = 1
        if prev_month == -2 : prev_month = 9
        prev_year = self.year if prev_month > 0 else self.year - 1
        
        self.data = self.data[(self.data['month'].isin([prev_month, self.month])) 
                              & (self.data['month'].isin([prev_year, self.year]))
                              ]
        # we only keep assets with a stock price in prev_month and pred_month, 
        # and compute their values and evolutions
        self.df_portfolio['symbol'] = self.data['symbol'].unique()
        prev_stock_prices, pred_stock_prices, var_stock_prices = [], [], []
        for symbol in self.df_portfolio['symbol'] :
            prev_stock_price = self.data[(self.data['month']==prev_month) 
                                         & (self.data['symbol']==symbol)
                                         ]['close'].values[0]
            pred_stock_price = self.data[(self.data['month']==self.month) 
                                         & (self.data['symbol']==symbol)
                                         ]['close'].values[0]
            var_stock_price = (pred_stock_price - prev_stock_price) / prev_stock_price
            
            prev_stock_prices.append(prev_stock_price)
            pred_stock_prices.append(pred_stock_price)
            var_stock_prices.append(var_stock_price)
            
        self.df_portfolio['prev_stock_price'] = prev_stock_prices
        self.df_portfolio['prev_stock_price'] = prev_stock_prices
        self.df_portfolio['var_stock_price'] = var_stock_prices
        
        self.df_portfolio.sort_values(by='var_stock_price', 
                                      ascending=False, 
                                      ignore_index=True, 
                                      inplace=True
                                      )
        self.df_portfolio = self.df_portfolio.head(self.selected_nb_companies)
        self.df_portfolio['rank'] = self.df_portfolio.index + 1
        
        tot_var = self.df_portfolio['var_stock_price'].sum()
        self.df_portfolio['weight'] = self.df_portfolio['var_stock_price'] / tot_var


    def page_portfolio(self):
        if self.selected_nb_companies:
            st.dataframe(
                self.df_portfolio[['rank', 'symbol', 'prev_stock_price', 'var_stock_price']], 
                column_config = {
                    # adapt display here
                },
                hide_index=True, 
                use_container_width=True,
            )
            
            fig = go.Figure(data=[go.Pie(labels=self.df_portfolio['symbol'], 
                                         values=self.df_portfolio['weight'], 
                                         hole=0.6)]
                            )
            fig.update_layout(annotations=[dict(
                text='Portfolio',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
                )])
            
            st.plotly_chart(fig)


if __name__ == "__main__":
    # Run the Streamlit app with the Page 0 for plume detection
    Streamlit_Page0()