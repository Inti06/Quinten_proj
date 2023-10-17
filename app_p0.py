import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


class Streamlit_Page0:
    def __init__(self):
        ## Initialize the Streamlit app and class attributes
        # hide top orange bar
        hide_decoration_bar_style = '<style> header {visibility: hidden;}</style>'
        st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
        self.data = pd.read_csv("data/data_test.csv", header=0) # dataset
        self.data['year'] = self.data['year'].astype(int)
        self.data['quarter'] = self.data['quarter'].astype(int)
        self.selected_quarter = None # quarter selection for prediction
        self.selected_nb_companies = None
        self.month = None # month associated with the prediction quarter
        self.year = None # year associated with the prediction quarter
        self.df_portfolio = pd.DataFrame()

    def update_data(self):
        # Define the selectboxes accordingly to the data
        self.data['id_quarters'] = 'Q' + (self.data['quarter']//3 + 1).astype(str)+ ' ' + (self.data['year']).astype(str)
        col1, col2 = st.columns(2)
        self.selected_quarter = col1.selectbox('Select Quarter for prediction', 
                                               np.flip(self.data['id_quarters'].unique()), 
                                               index=0)
        self.selected_nb_companies = col2.selectbox('Select Portfolio Size', 
                                                    list(range(2, 30)), 
                                                    index=6)
        quarter = int(self.selected_quarter[1])
        self.month = {1: 1, 2: 3, 3: 6, 4: 9}.get(quarter)
        self.year = int(self.selected_quarter[3:7])
        # compute the stock price evolution
        prev_month = {9: 6, 6: 3, 3: 1, 1: 9}.get(self.month)
        prev_year = self.year-1 if prev_month == 9 else self.year
        prev_id_quarter = f'Q{str(prev_month // 3 + 1)} {str(prev_year)}'

        self.data = self.data[(self.data['id_quarters']==self.selected_quarter) 
                              | (self.data['id_quarters']==prev_id_quarter)
                              ]

        # we only keep assets with a stock price in prev_month and pred_month, 
        # and compute their values and evolutions
        symbols, prev_stock_prices, pred_stock_prices, var_stock_prices = [], [], [], []
        for symbol in self.data['symbol'].unique() :
            prev_stock_price = self.data[(self.data['id_quarters']==prev_id_quarter) 
                                         & (self.data['symbol']==symbol)
                                         ]['stockPrice']
            pred_stock_price = self.data[(self.data['id_quarters']==self.selected_quarter) 
                                         & (self.data['symbol']==symbol)
                                         ]['stockPrice']
            if not prev_stock_price.empty and not pred_stock_price.empty :
                symbols.append(symbol)
                prev_stock_price = prev_stock_price.values[0]
                pred_stock_price = pred_stock_price.values[0]
                var_stock_price = (pred_stock_price - prev_stock_price) / prev_stock_price
                prev_stock_prices.append(prev_stock_price)
                pred_stock_prices.append(pred_stock_price)
                var_stock_prices.append(var_stock_price)
        self.df_portfolio['symbol'] = symbols
        self.df_portfolio['prev_stock_price'] = prev_stock_prices
        self.df_portfolio['pred_stock_price'] = pred_stock_prices
        self.df_portfolio['var_stock_price'] = var_stock_prices

        self.df_portfolio.sort_values(by='var_stock_price', 
                                      ascending=False, 
                                      ignore_index=True, 
                                      inplace=True
                                      )
        self.df_portfolio = self.df_portfolio.head(self.selected_nb_companies)
        self.df_portfolio['rank'] = self.df_portfolio.index + 1

        weights = []
        limit = limit = {1: 1, 2: .75, 3: .67, 4: .5}.get(len(self.df_portfolio), 0.35)
        tot_var = self.df_portfolio['var_stock_price'].sum()
        for i in range(len(self.df_portfolio)):
            weight = min(
                limit, 
                (1-sum(weights))*self.df_portfolio.loc[i]['var_stock_price'] / tot_var
                )
            weights.append(weight)
        self.df_portfolio['weight'] = weights


    def page_portfolio(self):
        self.update_data()
        
        #if self.selected_nb_companies:
        df = self.df_portfolio.copy()
        df['percentage'] = 100*df['var_stock_price']
        df['percentage'] = df['percentage'].map(lambda x : f'{x :.1f} %')
        st.dataframe(
            df[['rank', 'symbol', 'prev_stock_price', 'percentage']], 
            column_config = {
                'rank' : 'RANK', 
                'symbol': 'ASSET', 
                'prev_stock_price' : 'STOCK PRICE',
                'percentage' : 'EXPECTED RETURN'
            },
            hide_index=True, 
            use_container_width=True,
        )
        
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
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
        
        weighted_return = 100*(self.df_portfolio['var_stock_price']*self.df_portfolio['weight']).sum()
        
        col1.plotly_chart(fig)
        # spacer
        for _ in range(5):
            col3.markdown('#')
            col4.markdown('#')
        col3.metric("Number of assets", str(self.selected_nb_companies))
        col4.metric("Weighted return", f'{weighted_return :.1f} %')



if __name__ == "__main__":
    # Run the Streamlit app with the Page 0 for plume detection
    Streamlit_Page0()