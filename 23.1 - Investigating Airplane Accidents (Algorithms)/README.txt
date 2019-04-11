# Investigating Airplane Accidents

This document will document the process of our project of investigating airplane accidents toures, and will be written in markdown language.

## Introduction
Accidents are an unfortunate fact of air travel. Although flying is statistically safer than driving, minor and major flying accidents occur daily. In this project, we will work with a data set of airplane accident statistics to analyze patterns and look for any common threads.

For the dataset, we have 77282 aviation accidents that have occured in the US, and the respective data associated with each one in AviationData.txt. This file comes from the NTSB and can be found here: https://catalog.data.gov/dataset/aviation-data-and-documentation-from-the-ntsb-accident-database-system-05748/resource/4b1e95fe-91a7-4112-85fa-424d2672a906
        
The file is not in CSV format but has a '|' delimiter. Some relevant columns in the dataset are:
* Event Id - The unique id for the incident
* Investigation Type - The type of investigation the NTSB conducted
* Event Date - The date of the accident
* Location - Where the accident occurred
* Country - The country where the accident occurred
* Latitude - The latitude where the accident occurred
* Longitude - The longitude where the accident occurred
* Injury Severity - The severity of any injuries
* Aircraft Damage - The extent of the damage to the aircraft
* Aircraft Category - The type of aircraft
* Make - The make of the aircraft
* Model - The model of the aircraft
* Number of Engines - The number of engines on the plane
* Air Carrier - The carrier operating the aircraft
* Total Fatal Injuries - The number of fatal injuries
* Total Serious Injuries - The number of serious injuries
* Total Minor Injuries - The number of minor injuries
* Total Uninjured - The number of people who did not sustain injuries
* Broad Phase of Flight - The phase of flight during which the accident occurred

At this point, we have read the file into a list to practice data structures, and have gone through some cleanup including splitting the data into a list of lists and a little bit of example analysis. The process is documented in the read.py file.

After doing some preliminary research, we saw that finding 'LAX94LA336' in our list was possible, but it is not good for a couple of reasons. First, it is not very efficient to do exponential search for this particular situation (or any situation really). We will improve upon it later. Next, it is important to point out that if this value were present 2+ times on the same row, the row would be appended twice and we would have redundant data. While we could break out of the inner loop to prevent this, it still poses the linear search problem, which we will look at next.

## Linear and Log Time Algorithms
One of the main problems that our search algorithm posed in the code above was that it took exponential time. That is because it had to loop through each row first, and then each column inside that row. 

There are ways to make our algorithm run on Big O of n time or log(n) time, or in other words, linear or log times. This will be much faster than an exponential search and will be documented in the file read.py.

As we can see in our code (and example if we slowed down the process enough or added a timer to the search), the log time search will take significantly less time searching for a code as our data grows, and the exponential time search will ultiamately become unbearable if we were working with a dataset such as any flights from the past year, accident or not.

The tradeoffs for these such algorithms reside mainly in complexity vs. efficiency. The more complex an algorithm is, the more efficient. While the exponential algorithm was very easy to understand and write, it will take a lot longer. The log algorithm took a bit more intuition even though its code was short, because it was not that easy to implement. Although you will be thanking yourself later because it will take much faster to run.

Generally, with smaller datasets, it is ok to use simpler algorithms because your code will return fast anyway. As your dataset grows, however, it is a good idea to graduate to complex alogrithms to save yourself the headache.

## Hash Tables
It is important to note that our last algorithm of log time implemented was called a hash table. Hash tables are important to understand and are one of the most useful algorithms out there to save time.

With enough knowledge, it can be implemented in just 3 lines of code as seen in read.py! More information on hash tables can be read here: https://en.wikipedia.org/wiki/Hash_table.
        
For the rest of the project, we will use whichever algorithm we deem is most efficient (probably the simplest one since the dataset is not that large).
        
## Accidents by US State
Now that we have a good algorithm, we can do some analysis! 

For now, let us count how many accidents occurred in each U.S. state, then determine which state had the most accidents overall. Again, this will be documented in the read.py file.

As we see in our code, the accidents were easily fit into a dictionary, and we could extract the most accidents also relatively easily, which was CA. This makes sense considering how big the state is and how much aviation traffic it would get. 

## Fatalities and Injuries by Month
Finally, since we do not really want to make this an analysis heavy project (this was for data structures - a bunch of analysis projects can be seen in other projects in the github), let us just end by calculating the fatalities and injuries by month.

We can make a couple of functions that display accidents and injuries by month, and then compare them. This will again be documented in the read.py file.

The months with the most accidents are in the dead of summer and come at the beginning of our dataset. Next we will see if these months are also the ones that had the most injuries.

Interestingly, the 3 worst months for injuries are not the same as the 3 worst months for accidents! This can probably be atrributed to most minor dings and scratches where people are not harmed being recorded as accidents.

There are many more questions to explore with this data. It would be interesting to see the number of injuries or accidents in a time series chart to see if there is any trend. A histogram showing the frequency of injuries and accidents in each month of the year would show if there is any reason to suspect season effects, although as stated before, this can be done in a separate analysis project.

## Further Analysis / Next Steps
There are a few things we can try out before we conclude the project, including some mapping and a bit more analysis just to fully see what the dataset has to offer. Although we will not go too in depth, we can explain basis of what each part provides.

## Basemap
Matplotlib offers a pretty neat basemap library that we can use to actually see and map out each accident. Unfortunately, our dataset seems to be missing Latitude and Longitude values, but the source code would more or less look a little bit like this:
    
1. draw the map background
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=-119,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

2. scatter city data, with color reflecting population and size reflecting area
m.scatter(lon, lat, latlon=True,
          c=np.log10(population), s=area,
          cmap='Reds', alpha=0.5)

3. create colorbar and legend
plt.colorbar(label=r'$\log_{10}({\rm population})$')
plt.clim(3, 7)

4. make legend with dummy points
for a in [100, 300, 500]:
    plt.scatter([], [], c='k', alpha=0.5, s=a,
                label=str(a) + ' km$^2$')
plt.legend(scatterpoints=1, frameon=False,
           labelspacing=1, loc='lower left');

5. done!
plt.show()

Remember, this is after all the necessary modules are imported and lats and longs are extracted. The process is simple enough as we can see, and we have already implemented a basemap in a previous project before.

## Counts of Different Measures
Just like with our monthly data, we can instead count accidents by different things such as air carrier, make and model, or weather conditions to see what our ratings can be. It is important to note that we do not have the number of successful flights as well, so it is probably not safe to rate the highest number of accidents as the most dangerous carrier, since it will probably be the biggest company or most frequent weather condition by pure correlation.

In terms of implementation, we will save the headache of analysis because as we have learned, pandas and dataframes do a much better job of all of this than going through primitive things such as lists in Python. Knowing how to do these things is still important though, which is why we did it for the dates. If we wanted to see things such as carrier or make and model, all we need to do is change the appropriate column that we are pulling from and change the dict of dates to a dict of different carriers. That template can basically get us a count of anything!

Because of the headache but also redundancy, we leave it up to trust to recognize that with a few simple word changes, we can get the counts of most accidents by just about anything in the data with the functions that we have already provided in read.py.

## Conclusion
Although this project was quite short in relation to others in the github, we saw that we could implement different algorithms with different data structures relatively easily in Python. This is one of the advantages of the language, and why it is so good for data science. 

Most of this stuff works behind the scenes and we can get away with not know algorithms for a long time, but in order to work with really big datasets, it is important to understand the differences between things such as linear, exponential, log, nlog, etc. searches to make our projects more efficient. That is what this project was all about!

Our processes in other projects, especially machine learning ones, will implement an efficient algorithm by default, but if we are ever stuck in a primitive environment where we need to know how basic data structures and algorithms work, it is important to not be sitti
