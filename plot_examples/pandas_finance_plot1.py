import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web

DAX = web.DataReader(name='^GDAXI', data_source='yahoo', start='2000-1-1')

DAX['Close'].plot(figsize=(8, 5))


DAX['Return'] = np.log(DAX['Close'] / DAX['Close'].shift(1))

DAX[['Close', 'Return']].plot(subplots=True, style='b', figsize=(8, 5))

plt.show()


