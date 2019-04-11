# code for predictions
# python from command line 
if __name__ == "__main__":
    # import libraries
    import pandas as pd
    import numpy as np
    from datetime import datetime
    
    # read in the dataset
    data = pd.read_csv('sphist.csv')
    
    # convert dates
    data['Date'] = pd.to_datetime(data['Date'])
    
    # sort according to Date
    data.sort_values(by=['Date'], axis=0, ascending=True, inplace=True)
    
    # compute averages for previous 5, 30, 200 days, and set new columns
    # edit for improving errors: added 5 day averages for volume, high, low, open
    for index, row in data.iterrows():
        data['day_5_price'] = data['Close'].rolling(window=5).mean().shift(1)
        data['day_30_price'] = data['Close'].rolling(window=30).mean().shift(1)
        data['day_250_price'] = data['Close'].rolling(window=250).mean().shift(1)
        
        data['day_5_vol'] = data['Volume'].rolling(window=5).mean().shift(1)
        data['day_5_open'] = data['Open'].rolling(window=5).mean().shift(1)
        data['day_5_high'] = data['High'].rolling(window=5).mean().shift(1)
        data['day_5_low'] = data['Low'].rolling(window=5).mean().shift(1)
        
    # edit for improving errors: added year, day of week components (dummy vars)
    data['Year'] = data['Date'].apply(lambda x: x.year)
    data['day_of_week'] = data['Date'].apply(lambda x: x.weekday())
    dow_df = pd.get_dummies(data['day_of_week'])
    data = pd.concat([data, dow_df], axis=1)
    data = data.drop(['day_of_week'], axis=1)
    
    # remove any rows that have a NaN in new columns (before 1951-01-03)
    data = data[data["Date"] > datetime(year=1951, month=1, day=2)]
    
    # remove any rows with a NaN in general
    data = data.dropna(axis=0)
    
    # split dataset into train and test dfs
    train = data[data["Date"] < datetime(year=2013, month=1, day=1)]
    test = data[data["Date"] >= datetime(year=2013, month=1, day=1)]
    
    # get ML functions
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    
    # declare features
    # edit for improving errors: added rest of features after first three
    features = ['day_5_price', 'day_30_price', 'day_250_price', 'day_5_vol', 'day_5_open', 'day_5_high', 'day_5_low', 'Year', 0, 1, 2, 3, 4]
    
    # model declaration and training
    model = LinearRegression()
    model.fit(train[features], train[['Close']])
    predictions = model.predict(test[features])
    
    # get errors
    mae = mean_absolute_error(test[['Close']], predictions)
    
    # see results!
    print(test.tail(10))
    print(mae)