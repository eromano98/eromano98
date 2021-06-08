# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 11:02:48 2021

@author: eduar
"""
"""
Backtest strategy 
"""
import bt
import pandas as pd

tickers = 'aapl,msft,v,nvda,ma,pypl,intc,adbe,crm,avgo,csco,acn,txn,qcom,orcl,amat,ibm,now,intu,mu,amd,fis,lrcx,adp,fisv'
start = '01-01-2015'
end = '31-12-2018'




portfolio = bt.get(tickers, start = start, end = end )

# We will need the risk-free rate to get correct Sharpe Ratios 
riskfree =  bt.get('^IRX', start=start)
# Convert risk free from % to decimal

riskfree_rate = float(riskfree.mean()) / 100
# Print out the risk free rate to make sure it looks good
print(riskfree_rate)

#we start to built our first strategy where we run monthly and the weight assigned to the stocks is equal
Strat1 = bt.Strategy('Benchmark', [bt.algos.RunMonthly(),
                                     bt.algos.SelectAll(),
                                     bt.algos.WeighEqually(),
                                     bt.algos.Rebalance()])

# we run our backtest to test our strategy
test = bt.Backtest(Strat1, portfolio)

# create a second strategy named Second_Strat
# we RunWeekly and Weight using Inverse Volatility in this strategy 
# This means the strategy will make more trades and put more weight on less Volatile asset
Strat2 = bt.Strategy('Inverse Vol', [bt.algos.RunWeekly(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighInvVol(),
                        bt.algos.Rebalance()])


Strat3 = bt.Strategy('Mean Var',  [bt.algos.RunEveryNPeriods(30, offset=30),
                                       bt.algos.SelectAll(),
                                       bt.algos.WeighMeanVar(lookback=pd.DateOffset(months=3),bounds=(0.015,0.15), rf=riskfree_rate),
                                       bt.algos.Rebalance()])

# Test Second_Strat and name it test2
test2 = bt.Backtest(Strat2, portfolio)
test3 = bt.Backtest(Strat3, portfolio)



# To see the results side-by-side, we must tell the bt.run to use both tests
# All res2 commands will produce output comparing s1 and s2 because we have test and test2
results_both = bt.run(test, test2,test3)
results_both.set_riskfree_rate(riskfree_rate)

# res_First_Strat only has test in it, so you will only see Second_Strat from it
res_Strat1 = bt.run(test)

# res_Second_Strat only has test2 in it, so you will only see Second_Strat from it
res_Strat2 = bt.run(test2)
res_Strat3 = bt.run(test3)

# res2 plots here include both s1 and s2 info
results_both.plot()


results_both.display()

# Plot weights from the first strategy to illustrate the different weighting schemes
res_Strat1.plot_security_weights()
res_Strat3.plot_security_weights()
res_Strat3.plot_security_weights()
# For some reason, I cannot plot weights or histograms for both at the same time
results_both.plot_security_weights()
#----------------------------------------
start1 = '2019-01-01'
end1 = '2020-01-01'
data = bt.get(tickers, start = start1, end = end1)

test = bt.Backtest(Strat1, data)
test2 = bt.Backtest(Strat2, data)
test3 = bt.Backtest(Strat3, data)



# To see the results side-by-side, we must tell the bt.run to use both tests
# All res2 commands will produce output comparing s1 and s2 because we have test and test2
results_both = bt.run(test, test2,test3)
results_both.set_riskfree_rate(riskfree_rate)

# res_First_Strat only has test in it, so you will only see Second_Strat from it
res_Strat1 = bt.run(test)

# res_Second_Strat only has test2 in it, so you will only see Second_Strat from it
res_Strat2 = bt.run(test2)
res_Strat3 = bt.run(test3)

# res2 plots here include both s1 and s2 info
results_both.plot()


results_both.display()

# Plot weights from the first strategy to illustrate the different weighting schemes
res_Strat1.plot_security_weights()
res_Strat2.plot_security_weights()
res_Strat3.plot_security_weights()
# For some reason, I cannot plot weights or histograms for both at the same time
results_both.plot_security_weights()

