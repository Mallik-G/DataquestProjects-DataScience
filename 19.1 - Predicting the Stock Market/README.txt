### Documented process for this project and steps taken to build model - written in markdown language ###

# Predicting the Stock Market
This project will focus on taking historical daily records of prices of the S&P500 index from 1950 to 2015 and trying to forecast future prices based on this information. THe dataset is the file 'sphist.csv' in the project folder. Note that this information is only for the S&P500 index.

## Introducton
Like mentioned above, we can try to take historical pricing data for an index in the stock market and try to see if we can "predict" prices moving forward. Predict is in quotations obviously because we are using the trained part of the model to predict the test part, not actual future prices, although we can certainly do that as well. For this model, training will be on the years 1950-2012 and then the model will be tested on its predictions for the years 2013-2015. We'll see how it does!

Some information on the columns for reference: 
* Date -- The date of the record.
* Open -- The opening price of the day (when trading starts).
* High -- The highest trade price during the day.
* Low -- The lowest trade price during the day.
* Close -- The closing price for the day (when trading is finished).
* Volume -- The number of shares traded.
* Adj Close -- The daily closing price, adjusted retroactively.

## Reading in the Data 
First we need to read in some data. This whole process is documented in the predict.py script. Essentially, we are trying to do the following:
* Read in the data first for a basic df
* Convert the date column to use to_datetime function
* Import datetime library and get the datetime functions
* Sort the df by date in ascending order

While this obviously does not predict anything, it is a good start in reading in data and doing some basic cleanup work. Work can be verified through this step by isolating the code and running just this portion in the cmd.

## Generating Indicators
Stock datasets are different from others, such as housing prices or classifications. Each row is not independent, as they are sequential from one day to another. Because of this, we must be very careful not to inject 'future' knowledge when training - this will not bode well for predictions when it comes time for the real world (this is how many algorithmic traders lose money). 

Using the time series nature of the data, we can generate indicators to make our model more accurate. By creating a new column that contains the average of every 10 rows, for example, we combine information as well as enhancing accuracy. When we do this, it is important not to take the current row into account. The point here is price prediction, and in the real world we will not know the current price upfront when trying to predict something.

Here are some ways we can generate indicators:
* The average price from the past 5 days.
*The average price for the past 30 days.
*The average price for the past 250 days.
*The ratio between the average price for the past 5 days, and the average price for the past 250 days.
*The standard deviation of the price over the past 5 days.
*The standard deviation of the price over the past 250 days.
*The ratio between the standard deviation for the past 5 days, and the standard deviation for the past 250 days.

We are going to assume here that "days" means trading days, so the 5 days before the current one, and "price" means the price in the 'Close' column at the end of that day. Always be careful not to include the current price in these indicators! We are predicting the next day price, so our indicators are designed to predict the current price from the previous prices. We can start our yearly computations with the first date available + 1 year, which is 1951-01-03.

We will loop through each day in the dataset to get these averages. For example, to find the average past 5 day price for 1951-01-03, we would loop from 1950-12-26 to 1951-01-02, and compute those averages. Note that the loop ends the day before as mentioned, and also more than 5 calandar days are in the loop because we have to account for holidays too (trading days are not calandar days). Then, for 1951-01-04, we would loop again from 1950-12-27 to 1951-01-03, and so on.

This process will keep repeating until we have all the averages. Below is an example layout of what the first 10 days would look like, with indexes. 

        Date	    Close	    day_5
16339	1951-01-03	20.690001	20.360000
16338	1951-01-04	20.870001	20.514000
16337	1951-01-05	20.870001	20.628000
16336	1951-01-08	21.000000	20.726001
16335	1951-01-09	21.120001	20.840001
16334	1951-01-10	20.850000	20.910001
16333	1951-01-11	21.190001	20.942001
16332	1951-01-12	21.110001	21.006001
16331	1951-01-15	21.299999	21.054001
16330	1951-01-16	21.459999	21.114000

This process will be continued to be documented in the predict.py file, so again isolating the code will run this portion by itself. We will be computing 3 indicators from our suggestion list: averages of 5, 30, and 250 days (250 trading days is about a year). This will be accomplished by looping with the iterrows method and rolling function in pandas, and the shift method will be used to account for not using the current data for that day.
    
## Splitting the Data 
Now that we have our new indicator columns, we can get rid of 'unimportant' data. Our 'day_250' column for example has NaN for the entire first year, as expected. Judging by the fact that we have over 60 years worth of data, we can drop the first year of 1950. More accurately, it is not until 1951-01-03 that all three new columns are filled up. We can adjust the df now to only keep the rows past these dates for good analysis.

Once this is done, it is time to split our data up to prepare for testing. As stated before, we will use the remaining clean data up until 2013-01-01 for training, and dates after that for testing. Once again, all of this will be documented in the predict.py file.

## Making Predictions 
Now we can establish an error metric, train the model, and make predictions! We will be using mean absolute error (or MAE) because this metric shows how 'close' you were to the price in intutitive terms. In contrast, mean squared error (or MSE) is more commonly used, but for this case it makes it harder to intutitively tell how far off you were from the true price because it squares the error. Generally MAE is okay in linear type problems.

We will now create an instance of a linear regression model and train it using ONLY our three new columns that we made. We leave out all the original columns because they all contain knowledge of the future that we do not want the model to have in order to be realistic. The 'Close' column will be the target column and the column that we will make predictions for on the test df.

Finally, we will see how far off we were using these metrics with the MAE. This first iteration of the model will be documeted in predict.py.

MAE found: 16.1486719012233.
    
## Improving Error
The MAE found can be interpreted as this: on average, the price that is predicted is more or less $16.15 off from the actual price of that day. On one hand, if you consider the fact that the S&P500 prices range around $1500 starting in 2013, this means the error is within 1%! On the other hand, the index itself rarely deviates 1% whichever direction on any given day, so it seems like the error itself is already the full range of possibilities, or at least almost so. 
    
Because of this, day trading seems to be out of the equation, and long term trading is also kind of moot because the stock market trends up long term anyway.
    
This makes our get rich quick (sarcasm) scheme a bit unlikely, but after all, no one expects to get rich quick with just a random average model of 3 basic indicators. We can try to reduce this erorr a little bit by adding a couple more features that are a little more complex. Here are some examples:
*The average volume over the past five days.
*The average volume over the past year.
*The ratio between the average volume for the past five days, and the average volume for the past year.
*The standard deviation of the average volume over the past five days.
*The standard deviation of the average volume over the past year.
*The ratio between the standard deviation of the average volume for the past five days, and the standard deviation of the average volume for the past year.
*The year component of the date.
*The ratio between the lowest price in the past year and the current price.
*The ratio between the highest price in the past year and the current price.
*The year component of the date.
*The month component of the date.
*The day of week.
*The day component of the date.
*The number of holidays in the prior month.

Obviously addinng all of these will result in overfitting and we definitely want to avoid that, so we can choose what we think is best. For this project, we will add what we think will be useful for day trading; some 5 day averages. I.e. the average volume over the past 5 days, the average high, low, and open prices, and we will also add the year component of the date as well as day of the week, as this could pose interesting results. This will be marked in the predict.py file, and documented accordingly.

Note: the day of week columns will be indicated by integers: 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday. Exchange closed on weekends. This was thought be simple enough to not rename the columns ans save space.

MAE found: 13.314816276920169
    
## Further Analysis / Next Steps 
As we can see, the MAE was reduced a little bit more, naturally from the more in-depth indicators that we provided. As is such the nature of ML, the indicators can always be improved, but we also need to be careful not to improve them too much, or we will overfit. On the algorithmic side of things, there are also a few things that need to be mentioned as well. Working on these few things may seem like little iterable changes in our code, but the differences can mean everything when dealing with projects like these.

## Multiple Models
Our model right now trains based on dates from 1951-2013, and then tries to predict prices from 2013-2015. This is a good exercise, but in order to actually predict day to day prices, we need to include each passing day as new information and only predict a day ahead, as this will more accurately capture what we want in a price prediction model. For example, if it was 2013-01-02 right now:
*We would train a model using information from 1951-01-03 to 2013-01-02 (not inclusive), and try to predict just the price at 2013-01-02.
*Then the next day, we train a separate model using information from 1951-01-03 to 2013-01-03, including the new information yesterdat, and try to predict just the price at 2013-01-03. 
*Rinse and repeat!

This type of modeling is actually more intuitive when we think about what we want to predict, even if it seems more comlex. If we are actually trying to do this day to day, using past daily information in each new model makes the 'ultimate' model more accurate day by day.

## Improved Algorithm 
Using different types of algorithms can also be a way to improve model results. There are a multitide of different types of algorithms, so while trying each one is just a waste of time, we can use ones that we think will work best and go from there. For example, a random forest may be of use here.

A random forest is another fairly fast and simple tool, and can be read about here: https://towardsdatascience.com/the-random-forest-algorithm-d457d499ffcd.
        
To quote, "To say it in simple words: Random forest builds multiple decision trees and merges them together to get a more accurate and stable prediction."

Fortunately for us, implementing this (thanks to the power of Python libraries) is just a matter of a few minutes of getting the right modules and function syntax. Because of this, we can actually try out multiple algorithms in the span of a work day!

## Different Data 
Although the premise of the analysis will be the same (not much changes) when adding different data, the interesting part comes from just deciding which data is considered valuable and which data is just noise. For example, there are tons of datasets to incorporate into this project, such as daily weather in NYC, or twitter activity pertaining to different stocks on any given day. While the former is probaly just correlation and pure noise, the latter may be interesting to see. 

Social media data is only going to become more and more prevalent in future models, so adding in the dataset to see how error is affected may be worthwhile. The good news is, as mentioned before, not much more work will be required. We simply just read in the new dataset, adjust some columns and features, and voila. No new analysis will really need to be implemented.

## Automation
This is where the fun begins. Like our "Fandango Movie Ratings" project (data analysis folder on github), we can set up an automated scraping script to get the latest data when the market closes each day and make our multiple models scenario a lot more simple by automation. We simply set the script to run at the same time each day, and this prevents the user from having to manually get a new dataset each and every day as new information is presented. A quick fix that saves loads of time!

## Higher Resolution
We are currently making daily predictions. But why stop here? We can always make hourly, minute-ly, or even predictions by the second. We just need to obtain more data that has informatino pertaining to these scopes. The more we scope in, however, the more the data becomes just pure noise, fair warning. 

For example, predicting the price by second is probably not reccommended because at that point the prices are probably inevitbaly effected by randomness more than anything. 

Again, like our other improvement, the good news is once we obtain this higher-scoped data, the process will more or less be the same. For the purpose of price predictions, however, day-by-day is already pretty scoped in and besides hourly predictions, this is probably the most in-depth we can go before being subjected to pure randomness. This is all subject to opinion though, and it is just a matter of both experience and trial and error. All in the beauty of ML!

## Conclusion
In this project, what really should be highlighed is the efficiency of the code itself. This README ended up being 3x as long as the predict.py file! This is the beauty of efficient alogithms in Python, and something we will continue to work on moving forward. 

As for the model itself, using our features and linear regression, we were able to get price predictions within +/- $13 of the actual price on the average day. While this is not too bad, it certainly is not a means for a money making machine. Continuing to work this down using more efficient features and algorithms is the ultimate goal. This not only requires ML knowledge, but industry knowledge as well. Knowing which features to pick, which one is more useful than another, how to incorporate datasets in a way that makes sense, etc. are all things that only get better with experience in a domain. 

In terms of a linear regression model, however, we completed our goal! This model did exactly what we expected it to, and while predicting stock market prices was a bit of a longshot, we can use these same principles in the project to gain much more useful and practical predictions in other areas of life. 