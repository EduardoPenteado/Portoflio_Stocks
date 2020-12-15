# Portoflio_Stocks

This code returns a series of graphs of the stocks on your portfolio, and returns the final investment of your portfolio. Also, It compares your investment with Dolar, Bitcoin and index Ibovespa.
The main libraries are Plotly, Pandas and YFinance.

# INSTRUCTIONS
1. You need to run it on a graphic interface, like Jupyter Notebook.
2. The code will ask for inputs, first, the total amount that you have invested. After, you need to provide the stock name, the bought date of the stock and the percentage of it in your portfolio of investment.
3. Follow the steps on the inputs, they have some tips and if you enter a wrong input, the code would recognize it and you will asked to insert a correct input.
4. The code will run when the percentage achieves 1, that is 100 % of your total amount have been inputed.
5. The graphs are interative, you can zooming then and double click to zoom out.
obs. If a stock is matchs 25 % of your total amount, on the percentage, you'll need to enter 0.25.
The returns could have a bit difference, because it doesn't consider the broker tax, or other taxes. Also, the median price in the bought day and the final day were calculated, which is the median of Close, High and Low price at the day.
