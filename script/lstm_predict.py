#--coding:utf-8--
'''
lstm 预测
'''
import sys
sys.path.append("..")
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.utils import Sequence
from pandas import concat, DataFrame
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from script.logger import logger
from script.mysql_util import PooL
import numpy as np

def loadData():
    import pandas as pd

    try:
        conn = PooL.connection()
        sql = "select * from stock_data;"
        df = pd.read_sql(sql,conn,index_col='id')
        conn.close()

    except:
        logger.error("load data from mysql failure",exc_info = 1)
    return df

## 数据转换
def transformData(df):
    try:

        df = df.drop(df.columns[[0,1,2,3]],axis=1)
        values = df.values  ## 获取有效数据部分
        ## 数据归一化
        '''
        只有当数据中出现标签类数据的时候，才需要做一下的转换操作
          # # integer encode direction
        # encoder = LabelEncoder()
        # values[:, 2] = encoder.fit_transform(values[:, 2])
        '''
        # ensure all data is float
        values = values.astype('float32')

        # normalize features
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(values)
        # frame as supervised learning
        dataFrame = DataFrame(scaled)
        names = []
        # frame as supervised learning
        df1 = dataFrame.shift(1)  ## 向下移动一行
        names.extend([ 'var_%d' %(i) for i in range(len(df1.columns.values))])
        df2 = dataFrame.shift(-1)  ## 向上移动一行
        names.extend(['var_%d' % (i + len(df1.columns.values)) for i in range(len(df2.columns.values))])
        agg = concat([df1, df2], axis=1)
        agg.columns = names  ## 这一个步骤不能省，否则在删除列的时候，会出现问题
        agg.dropna(inplace=True)
        agg.drop(agg.columns[[29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]], axis=1,inplace=True)
        return agg
    except:
        logger.error('transformData error',exc_info = 1)

def predict(dataframe):
    import matplotlib.pyplot as pyplot
    import math
    from matplotlib.font_manager import FontProperties
    font_set = FontProperties(fname=r"../resources/font/simsun.ttc", size=12) ## r/R : 非转义的原始字符串

    values = dataframe.values
    n_train_size = math.ceil(values.shape[0]*0.7)

    train_x,train_y = values[:n_train_size,:-1],values[:n_train_size,-1]
    test_x,test_y = values[n_train_size:,:-1],values[n_train_size:,-1]
    ## 生成lstm 需要的数据结构  行数，时间间隔，列数
    train_x = train_x.reshape((train_x.shape[0],1,train_x.shape[1]))
    test_x = test_x.reshape((test_x.shape[0],1,test_x.shape[1]))

    ## 训练模型
    model = Sequential()
    model.add(LSTM(50,input_shape=(train_x.shape[1], train_x.shape[2]),dropout=0.3))
    model.add(Dense(1))
    '''
    可选的评价函数：
         mse = MSE = mean_squared_error
         mae = MAE = mean_absolute_error
         mape = MAPE = mean_absolute_percentage_error
         msle = MSLE = mean_squared_logarithmic_error
         kld = KLD = kullback_leibler_divergence
         cosine = cosine_proximity
    '''
    model.compile(loss='mse', optimizer='adam') ## 还可以采用adam

    history = model.fit(train_x,train_y,epochs=50, batch_size=30,validation_data=(test_x, test_y), verbose=2,shuffle=False)
   # plot history
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.title(u"股票预测拟合结果（时间步长：1s,优化函数：adam）",fontproperties=font_set)
    pyplot.legend()

    pyplot.show()

if __name__ == '__main__':

   df = loadData()
   # df.set_index(0)
   print(df.values)
   df = transformData(df)
   predict(df)

