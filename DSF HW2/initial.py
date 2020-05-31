import pandas as pd
import logging
import csv
import time
pd.set_option('display.width', 3000)
pd.set_option("display.max_columns", 15)

logging.info('Reading files..')
path = 'ieee-fraud-detection\\'
#txs =  pd.read_csv(path+'test_transaction.csv')
lim_txs = pd.read_csv(path+'test_transaction_sliced.csv')
ids = pd.read_csv(path+'test_identity.csv') #,index_col=0

#Filter to limit the number of columns/data
#filtered = txs[['TransactionID','TransactionDT','TransactionAmt','ProductCD','card1','card2','card3','card4','card5','card6','addr1','addr2','dist1','dist2']]
#f = open('ieee-fraud-detection\\test_transaction_sliced.csv','w+')
#filtered.to_csv(f,line_terminator='\n')

st = 0
en = 1
'''
for i in range(0,lim_txs.size) :
    print(lim_txs.loc[0,card1])
    st,en = st+1,en+1
    time.sleep(3)
    if i > 50 :
        break
'''

set_1000 = lim_txs.iloc[0:1000,:]

set_1000.hist()

