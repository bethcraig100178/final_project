
#################################################################################

                    #Proof of Concept Script
                    
#Nested loops with behaviours nested inside day ie run through all behaviours for Day 1 first, then all behaviours for Day 2 etc

#################################################################################


                            #Functions
                            
 #################################################################################
@profile
def convert_time(time): # converts string of hh:mm:ss to time in seconds
    
    time_hour = int(time[0:2])
    time_minute = int(time[3:5])
    time_seconds = int(time[6:8])
    time_seconds = (60*60*time_hour) + (60*time_minute) + time_seconds
    return time_seconds
    
@profile    
def create_lists(alldata):# create start, finish, behaviour and day_no lists
    start = []
    finish = []
    for line in alldata:
        data = line.split(',')
        #print type(list_behaviours[x]), type(data[3]), type(list_day_no[d]), type(data[0])
        if data[3] == list_behaviours[x] and int(data[0]) == list_day_no[d]:
            start_time_seconds = convert_time(data[4]) #convert the start and finish times of each recorded behavior from hh:mm:ss to seconds
            finish_time_seconds = convert_time(data[5])
            #generate a list for each attribute
            start.append(start_time_seconds)
            finish.append(finish_time_seconds)
            #print len(start), len(finish)
    return start, finish
    
@profile   
def yes_no_every_second(start, finish): #creates a yes/no for every second of the day between 5am (18000) and 8pm (72000) and a corresponding entry for behaviour and day_no
    i = 18000  # ie starts at 5am
    yes_list = []
    while i <= 72000: # ends the time span at 8pm and prevents traceback error for behaviours that are not recorded in a given day
        for s in range(0, len(start)): # len(start) is the number of instances of the behaviour recorded that day
            if  i == int(start[s]) or i == int(finish[s]): # this deals with the start and finish time of a behaviour instance
                yes_list.append("yes")
                #print 'yes', i
            elif i > int(start[s]) and i < int(finish[s]): #deals with seconds in between a start and finish time
                yes_list.append("yes")
                #print 'yes', i
            elif s-1 >= 0 and i > int(finish[s-1]) and i < int(start[s]):
                yes_list.append("no")
                #print 'no', i
            elif s == (len(start) -1) and i > int(finish[s]):
                yes_list.append("no")
                #print 'no', i
            elif s == 0 and i < int(start[s]):
                yes_list.append("no")
                #print 'no', i
                
        i = i + 1
    print len(yes_list)
    return yes_list
    
@profile  
def convert_TSB_percent(yes_list):#segregates into 15 minute intervals (every 900 seconds) and creates a zero entry for 15 min intervals with none of the behaviour in question
    log_yes = {}
    i = 0
    j = 0
    while i < 54001 and i < len(yes_list):
        #print 'i', i
        #print 'j', j
        #print yes_list[i]
        if i <= j + 900:
            if yes_list[i] == 'yes':
                log_yes[(j+18000)] = log_yes.get((j+18000), 0) + 1 #dictionary yes entry is created or increased by 1 
            elif yes_list[i] == 'no':
                log_yes[(j+18000)] = log_yes.get((j+18000), 0) + 0 #dictionary yes entry is created or increased by 0 so it is always zer0
            i = i+1
        else:
            j = j + 900
    log_yes = dict(map(lambda (k,v): (k, (v*100)/900.0), log_yes.iteritems())) # change the number of seconds spent at the behaviour in question to a percetnage of the 900 second interval 
    return log_yes

###################################################################################
                        #Step 1 Set-Up
        #Import Packages, Read in Master Data, set up files and empty lists etc

#################################################################################

#Import Packages
import csv

#Read in Data
file = 'master_data_for_python_test.csv'
alldata = [line.strip() for line in open(file, 'r')]

#create csv file to write to and add headers
file = 'master_data_after_python_test.csv'
with open(file, 'ab') as file:
    fieldnames = ['Day_No', 'Behaviour', 'Time', '%TSB'] # %TSB = % Time Spent (at a) Behaviour
    writer = csv.writer(file)
    writer.writerow(fieldnames)
    

#create list of study day number and pre-defined list of behaviours
list_day_no = [1,2, 3]
list_behaviours = ['SW', 'FO']


#################################################################################

                #Step 2 Loop through days and behaviours

#################################################################################   


d = 0 #loop through days variable to increment at the end of each day
while d < len(list_day_no):
    print 'day', list_day_no[d]
    x = 0 #loop through the list of behaviours (list_behaviours)(note behaviour is nested within days)
    while x < len(list_behaviours): # ends the loop when it has gone through every behaviour
        print 'behaviour', list_behaviours[x]
        start, finish = create_lists(alldata)#for the behaviour in question on the day in question (i) convert times into seconds and (ii) generate lists of start, finish times, behaviour and day number
        yes_list = yes_no_every_second(start, finish)#this section generates a list of yes/no for every second between 5am and 8pm 
        log_yes = convert_TSB_percent(yes_list) #convert to %TSB in 15 minute intervals
        file = 'master_data_after_python_test.csv'
        with open(file, 'ab') as file:
            writer = csv.writer(file)
            for key, value in sorted(log_yes.items()):
                writer.writerow([list_day_no[d], list_behaviours[x], key, value])
        file.close 
        x = x + 1 # increment behaviour by 1
    d = d+1 # increment day by 1
    
print 'got to the end'
print 'updated'    
   
   