# code for investigating airplane accidents is documented in this file

# read in the data
# use "head AviationData.txt" and "tail AviationData.txt" on the cmd to preview some of data
# first make empty lists
aviation_list = []
aviation_data = []

# open file and with it...
with open('AviationData.txt', 'r') as file:
    # loop through each line, appending to aviation_data and splitting the text
    for line in file:
        aviation_data.append(line)
        text = line.split('|')
        words = []
        # loop through each word in the text split and after cleaning, append to words
        for word in text:
            word = word.strip()
            words.append(word)
        # finally append the words to aviation_list
        aviation_list.append(words)

# see the first rows of data by uncommenting
#print(aviation_data[1], "\n")        
#print(aviation_list[1], "\n")

# assign lax_code for example analysis
lax_code = []

# search for a specific code and append - exponential time (NOT GOOD - EXPLAINED IN README)
for row in aviation_list:
    for element in row:
        if element == "LAX94LA336":
            lax_code.append(row)

# see lax_code (exponential result)
print(lax_code)

# search for a specific code and appen - linear time (FAIR - EXPLAINED IN README)
lax_lines = [x for x in open("AviationData.txt", "r") if "LAX94LA336" in x]

# see lax_lines (linear result)
print(lax_lines)

# search for a specific code and append - log time HASH TABLE (GOOD - EXPLAINED IN CODE)
headers = aviation_data[0].split(" | ")
aviation_dict_list = [dict(zip(headers, row.split(" | "))) for row in aviation_data[1:]]
lax_dict = [row for row in aviation_dict_list if "LAX94LA336" in row.values()]

# see lax_dict (log result)
print(lax_dict)

# get default dict, a special dict to work with
# a defaultdict works exactly like a normal dict, but it is initialized with a function (“default factory”) that takes no arguments and provides the default value for a nonexistent key
# also get operator -  a set of efficient functions corresponding to the intrinsic operators of Python
import operator
from collections import defaultdict
state_accidents = defaultdict(int)

# search the dataset and get assign each accident to a state
for row in aviation_dict_list:
    if row['Country'] == 'United States' and ", " in row['Location']:
        state = row['Location'].split(", ")[1]
        state_accidents[state] += 1
        
# get the most state accidents as well as all of them in one dict
state_accidents = dict(state_accidents)
most_accident_state = max(state_accidents.items(), 
                          key=operator.itemgetter(1))[0]

# see accidents and state with most
print(state_accidents)
print(most_accident_state)

# get Counter to count hashable objects
from collections import Counter

# make function for worst months for accidents
def worst_month_accidents(data):
    # assign empty list and month dict
    months = []
    change_month = {"01":"January",
                    "02":"February",
                    "03":"March",
                    "04":"April",
                    "05":"May",
                    "06":"June",
                    "07":"July",
                    "08":"August",
                    "09":"September",
                    "10":"October",
                    "11":"November",
                    "12":"December"}
    
    # loop through data and assign
    for x in range(0, len(data)):
        month = data[x]['Event Date'][0:2]
        try:
            month = change_month[month]
        except KeyError:
            month = data[x]['Event Id'][4:6]
            month = change_month[month]
        if data[x]['Event Date'] != '':
            year = data[x]['Event Date'][-4:]
        else:
            year = data[x]['Event Id'][0:4]
        months.append(month + ' ' + year)
    
    # return the worst months (and the top 3)
    worst_months = Counter(months)
    return worst_months, worst_months.most_common(3)

# get the worst months as a tuple
month_count_accidents, worst_3_months_acc = worst_month_accidents(aviation_dict_list)

# display the top 3 worst months
print(worst_3_months_acc)

# make function for worst months for injuries
def worst_month_injuries(data):
    # make empty injuries dict and month dict
    injuries_by_month = {}
    change_month = {"01":"January",
                    "02":"February",
                    "03":"March",
                    "04":"April",
                    "05":"May",
                    "06":"June",
                    "07":"July",
                    "08":"August",
                    "09":"September",
                    "10":"October",
                    "11":"November",
                    "12":"December"}
    
    # loop through data and assign
    for x in range(0, len(data)):
        injuries = 0
        month = data[x]['Event Date'][0:2]
        try: 
            month = change_month[month]
        except KeyError:
            month = data[x]['Event Id'][4:6]
            month = change_month[month]
        if data[x]['Event Date'] != '':
            year = data[x]['Event Date'][-4:]
        else:
            year = data[x]['Event Id'][0:4]
        month = month + ' ' + year
        fatal = data[x]['Total Fatal Injuries']
        serious = data[x]['Total Serious Injuries']
        
        # skip the blanks        
        if fatal:
            injuries += int(fatal)
        if serious:
            injuries += int(serious)
        
        # get the injuries by month with Counter and return worst 3
        injuries_by_month[month] = injuries
        injuries_by_month = Counter(injuries_by_month)        
        
    return injuries_by_month, injuries_by_month.most_common(3)

# get the worst months as a tuple
month_count_injuries, worst_3_months_inj  = worst_month_injuries(aviation_dict_list)

# return the worst 3 months for injuries
print(worst_3_months_inj)
