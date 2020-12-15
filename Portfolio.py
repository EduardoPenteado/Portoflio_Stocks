#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from IPython import display
from time import sleep
from plotly.subplots import make_subplots

class Portfolio:
    
    def __init__(self, stocks, total):
        self.total = total
        self.soma = []
        self.analise = []
        self.rdolar, self.rbit, self.ribov = [], [], []
        for stock in stocks:
            self.df = yf.download(stock[0]+'.SA',start=stock[2],end=datetime.today(),actions = True)
            self.df['Date'] = self.df.index
            aporte = self.total*stock[1]
            self.ibov = yf.download('^BVSP',start=stock[2], end=datetime.today())
            self.bit = yf.download('BTC-USD',start=stock[2], end=datetime.today())
            self.real = yf.download('BRL=X',start=stock[2],end=datetime.today())
            self.main(stock, aporte)  
        self.Total_Portfolio()
        
    def Close_graph(self, fig):
        # The close graph
        fig.append_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['Close'],
                        name='Close'),
                    row=1, col=1)
        return fig
        
    def Cumulative_graph(self, fig):
        # The Cumulative variation
        fig.add_trace(go.Scatter(
                        x=[self.df['Date'][0],self.df['Date'][-1]], y=[1, 1], 
                        showlegend=False,line=dict(color='black',dash='dash')),
                    row=1, col=2)
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['Close']/self.df['Close'][0],
                        name='Cumulative',fill='tonexty'),
                    row=1, col=2)
        return fig
    
    def Volume_graph(self, fig):
        # The variaotion of the volume
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['Volume'],
                        name='Volume',fill='tonexty'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(
                        x=[self.df['Date'][0], self.df['Date'][-1]],
                        y=[self.df['Volume'].mean(), self.df['Volume'].mean()],
                        line=dict(color='black',dash='dash'),showlegend=False),
                    row=2, col=1)
        return fig
    
    def Daily_graph(self, fig):
        # A Variation in day trade
        fig.add_trace(go.Histogram
                    (x=self.df['Close'].pct_change(1),
                    name="Daily Return",
                    histnorm='',
                    opacity=0.75),
                row=3, col=1)
        return fig
    
    def Median(self, fig):
        # The median 5 and 20 days graphs
        self.df['MA5'] = self.df['Close'].rolling(5).mean()
        self.df['MA20'] = self.df['Close'].rolling(20).mean()
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['Close'],
                        showlegend=False, line=dict(color='blue')),
                    row=4, col=1)
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['MA5'],
                        name='MA5'),
                    row=4, col=1)
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['MA20'],
                        name='MA20'),
                    row=4, col=1)
        return fig
    
    def High_graph(self, fig):
        # The High variation in the period
        fig.add_trace(go.Scatter
              (x=self.df['Date'],
               y=self.df['High'],
               name="High",
               line=dict(color="#33CFA5")),
            row=5, col=1)
        fig.add_trace(go.Scatter
               (x=[self.df['Date'][0], self.df['Date'][-1]],
               y=[self.df['High'].mean(), self.df['High'].mean()],
               name="High Average",
               line=dict(color="#33CFA5", dash="dash")),
            row=5, col=1)
        
        maximo = self.df['High'].max()
        minimo = self.df['High'].min()
        for i in range(0,len(self.df)):
            if self.df['High'][i] == maximo:
                max_index = self.df['Date'][i]
            elif self.df['High'][i] == minimo:
                min_index = self.df['Date'][i]
                
        # Anotations
        fig.add_annotation(x=max_index, y=maximo, text='Max: '+str(round(maximo,2)), row=5,col=1)
        fig.add_annotation(x=min_index, y=minimo,text='Low: '+str(round(minimo,2)),row=5,col=1)
        
        return fig
    
    def Low_graph(self,fig):
        # The low variation in the period
        fig.add_trace(go.Scatter
              (x=self.df['Date'],
               y=self.df['Low'],
               name="High",
               line=dict(color="#F06A6A")),
            row=5, col=2)
        fig.add_trace(go.Scatter
               (x=[self.df['Date'][0], self.df['Date'][-1]],
               y=[self.df['Low'].mean(), self.df['Low'].mean()],
               name='Low Average',
               line=dict(color="#F06A6A", dash="dash")),
            row=5, col=2)
        
        maximo = self.df['Low'].max()
        minimo = self.df['Low'].min()
        for i in range(0,len(self.df)):
            if self.df['Low'][i] == maximo:
                max_index = self.df['Date'][i]
            elif self.df['Low'][i] == minimo:
                min_index = self.df['Date'][i]
                
        # Anotations
        fig.add_annotation(x=max_index, y=maximo, text='Max: '+str(round(maximo,2)), row=5,col=2)
        fig.add_annotation(x=min_index, y=minimo,text='Low: '+str(round(minimo,2)),row=5,col=2)
        
        return fig
    
    def Dividends(self, fig):
        # Dividends payied during the period in table form
        self.df = self.df[self.df['Dividends'] != 0]
        fig.add_trace(go.Table(
                        header=dict(
                            values=["Date", "Dividends"],
                            font=dict(size=20),
                            align="center"
                        ),
                        cells=dict(
                            values=[self.df.index.strftime('%d'+'/'+'%m'+'/'+'%Y'),self.df['Dividends']],
                            align = "center")),row=3, col=2)
        return fig
    
    def Ibov(self, fig):
        #Ibov comparising plot
        fig.add_trace(go.Scatter(
                        x=[self.df['Date'][0],self.df['Date'][-1]], y=[1, 1], 
                        showlegend=False,line=dict(color='black',dash='dash')),
                    row=6, col=1)
        fig.add_trace(go.Scatter(
                        x=self.df['Date'], y=self.df['Close']/self.df['Close'][0],
                        showlegend=False, name='Cumulative',line=dict(color='blue')),
                    row=6, col=1)
        fig.add_trace(go.Scatter(
                        x=self.ibov.index, y=self.ibov['Close']/self.ibov['Close'][0],
                        name='Cumulative Ibov'),
                    row=6, col=1)
        return fig
    
    def Graphs(self, stock):
        #Making Subplot
        fig = make_subplots(
            rows=6, cols=2,
            specs=[[{}, {}],
                  [{"colspan": 2}, None],
                  [{}, {"type": "table"}],
                  [{"colspan":2}, None],
                  [{},{}],
                  [{"colspan":2}, None]])
        
        #Plotting functions
        self.Close_graph(fig)
        self.Cumulative_graph(fig)
        self.Volume_graph(fig)
        self.Daily_graph(fig)
        self.Median(fig)
        self.High_graph(fig)
        self.Low_graph(fig)
        self.Ibov(fig)
        self.Dividends(fig)
        
        #config graph
        fig.update_layout(height=1200, hovermode='x', title_text=stock[0])
        config = dict({'scrollZoom': True, 'responsive': False})
        fig.show(config=config)
    
    def Returns(self, stock, aporte):
        # Median price in the day of bought and sold. Calculate by the median of Close, High and Low.
        median_price = (self.df['Close'][0]+self.df['High'][0]+self.df['Low'][0])/3
        median_final = (self.df['Close'][-1]+self.df['High'][-1]+self.df['Low'][-1])/3
        dividends = self.df[self.df['Dividends'] != 0]['Dividends'].values
        soma_div = round(sum(dividends)*aporte/self.df['Close'][0],2)
        print('\033[1m'+stock[0]+'\033[0m')
        print('-'*25)
        print('Aporte Inicial: '+str(round(aporte)))
        #print('Aporte Final: '+str(round(aporte*median_final,2)))
        print('Dividendos ('+str(sum(dividends))+') | Total Pago: '+str(soma_div))
        ganho = self.df['Close'][-1]/self.df['Close'][0] - 1
        if ganho > 0:
            print('Variação positiva de \033[92m'+str(round(100*ganho,2))+' %\033[0m')
            print('Ganho de \033[92m'+str(round(ganho*aporte, 2))+'\033[0m')
            print('Com div: \033[92m'+str(round(ganho*aporte+soma_div, 2))+'\033[0m')
            print('Total: \033[92m'+str(round(aporte+ganho*aporte+soma_div, 2))+'\033[0m')
        else:
            print('Variação negativa de \033[91m'+str(round(ganho*100,2))+' %\033[0m')
            print('Perda de \033[91m'+str(round(ganho*aporte, 2))+'\033[0m')
            print('Com div: \033[91m'+str(round(ganho*aporte+soma_div, 2))+'\033[0m')
            print('Total: \033[91m'+str(round(aporte+ganho*aporte+soma_div, 2))+'\033[0m')
        self.Other_Returns(aporte)
        print('-'*25)
        self.soma.append(round(aporte+ganho*aporte+soma_div,2))
        self.analise.append((stock[0],aporte,round(aporte+ganho*aporte+soma_div,2),round(100*ganho,2)))
    
    def Other_Returns(self, aporte):
        # Return the variation of ibovespa, bitcoin and dólar in the period.
        var_ibov = self.ibov['Close'][-1]/self.ibov['Close'][0] - 1
        var_bit = self.bit['Close'][-1]/self.bit['Close'][0] - 1
        var_real = self.real['Close'][-1]/self.real['Close'][0] - 1
        self.ribov.append(aporte+var_ibov*aporte)
        self.rbit.append(aporte+var_bit*aporte)
        self.rdolar.append(aporte+var_real*aporte)
        print('Variação IBOV: '+str(round(100*var_ibov,2))+' %')
        print('Variação BITCOIN: '+str(round(100*var_bit,2))+' %')
        print('Variação REAL/DÓLAR: '+str(round(100*var_real,2))+' %')
    
    def Total_Portfolio(self):
        # Print the total return of the investment
        print('\033[1mANÁLISE DO INVESTIMENTO\033[0m')
        print('-'*30)
        print('Ações')
        for stock in self.analise:
            print(str(stock[0])+' - '+str(stock[1])+' - '+str(stock[2])+' ('+str(stock[3])+' %)')
        print('-'*30)
        print('Outros Investimentos')
        print('Ibovespa: '+str(round(sum(self.ribov),2))+' ('+str(round(100*((sum(self.ribov)/self.total)-1),2))+' %)')
        print('Bitcoin: '+str(round(sum(self.rbit),2))+' ('+str(round(100*((sum(self.rbit)/self.total)-1),2))+' %)')
        print('Real/Dólar: '+str(round(sum(self.rdolar),2))+' ('+str(round(100*((sum(self.rdolar)/self.total)-1),2))+' %)')
        print('-'*30)
        print('Aporte inicial do investimento: '+str(self.total))
        print('Montante final: '+str(round(sum(self.soma),2)))
        print('Ganho/Perda de: '+str(round(sum(self.soma)-self.total,2)))
        print('Retorno do Investimento: '+str(round(100*((sum(self.soma)/self.total)-1),2))+' %')
        print('-'*30)
        self.Indicators()
        
    def Indicators(self):
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type':'domain'}, {'type':'domain'}]],
            subplot_titles=['Investimento Inicial',"Investimento Final"])
        labels, value_in, value_fi = [], [], []
        for stock in self.analise:
            labels.append(stock[0])
            value_in.append(stock[1])
            value_fi.append(stock[2])
        fig.add_trace(go.Pie(labels=labels, values=value_in, textinfo='label+percent'),
              row=1, col=1)
        fig.add_trace(go.Pie(labels=labels, values=value_fi, textinfo='label+percent'),
              row=1, col=2)
        fig.show()
        
    def main(self, stock, aporte):
        self.Returns(stock, aporte)
        self.Graphs(stock)

# This function will receive the inputs of the stocks, percentage and bought date.
def Input(stocks, per_total):
    
    def Check_Stock():
        # Check if the user inserted a valid stock.
        while True:
            stock = str(input('Insert a valid stock: ')).upper()
            check = yf.download(stock+'.SA', start=datetime.today())
            if len(check) == 0:
                print('Invalid Stock')
                pass
            else:
                break
        return stock
    
    def Date():
        # Check if the user inserted a valid date.
        while True:
            date = str(input('Insert the period of purchase with format(yyyy-mm-dd): '))
            if len(date) != 10:
                print('Invalid date.')
            elif date[5:7] > str(12):
                print("Invalid month")
                print("Please, check if you don't have exchanged month with day")
            elif date.count('-') != 2:
                print('Invalid date')
            else:
                break
                
        return date
    
    def Percentage(per_total):
        # Check if the user inserted a valid percentage.
        while True:
            percentage = float(input('Insert the percentage of the stock in your wallet: '))
            if percentage > 1 or percentage < 0:
                print('Invalid value.')
                print('Please insert a valid percentage!')
            else:
                if per_total + percentage > 1 :
                    print('Invalid value, total wallet more than 100 %')
                    print('Please insert a valid percentage!')
                else:
                    break
        return percentage
    
    print('Now, you need to insert the stock, the percentage of it in your wallet on the format 0.25 (25%), and the bought date\n')
    # If per_total == 1 then 100 % of your wallet is inputed, so the program will run it.
    while per_total < 1:
        print('The program will run when the percentage of your wallet achieve 1.00 (100%)')
        print('Percentage of your wallet now: '+str(per_total))
        stock = Check_Stock()
        date = Date()
        percentage = Percentage(per_total)
        per_total += percentage
        print(stock+' '+date+' '+str(percentage)+' as been added.')
        sleep(3)
        display.clear_output(wait=True)
        stocks.append((stock, percentage, date))
    
    return stocks

# Input to the total invested.
total = int(input('Insert the total amount invested: '))
stocks, per_total = [], 0
# Add the stocks inputs in a list to run in the class Portfolio.
stocks = Input(stocks, per_total)

#Stock, percentage, Date
# If you want to optimize the code and don't be asking more for inputs, comment the input and discomment the line of code above and edit it.
#stocks = [('MGLU3',0.25,'2020-01-01'),('PETR4',0.25,'2020-01-01'),('AZUL4',0.25,'2020-01-01'),('ITSA4',0.25,'2020-01-01')]
port = Portfolio(stocks, total)

