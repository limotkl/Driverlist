import types
import pandas as pd
import numpy as np
import datetime
import DriverSchedule as ds
import os
import csv
import time
import datetime
from math import radians, cos, sin, asin, sqrt, fabs

# select the Driver you want
DRIVER_ID = 0

  

virtialRouteTable = []
route_dic = {}

with open('virtualScheduleSEP.csv','rU') as csvfile:
        csvreader1 = csv.reader(csvfile)
        for row in csvreader1:
            str1 = ''
            if '\xef\xbb\xbf' in row[0]:
                str1 = row[0].replace('\xef\xbb\xbf','')
                row[0] = str1
                virtialRouteTable.append(row)
            else:
                virtialRouteTable.append(row)

#build dictionary
for i in range(1,len(virtialRouteTable)):
    if virtialRouteTable[i][4].find("Details:") != -1:
        a = virtialRouteTable[i][4].split("Details: ")
        if len(a) > 1:
            temp = [virtialRouteTable[i][0],virtialRouteTable[i][2]]#add time and BUS number e.g['2017/9/5 7:23','763']
            x = a[1].upper()
            route_dic.setdefault(x, []).append(temp)



#print route_dic['ALPHA']
#===================================================================

SHUTTLE_NUM = ["763","747","762","748","787","788","528","526","[Deleted: ID 389]"]
PHONE_ID = ["02597a5b9e75cf6c", "02596c2b9e85bf69", "025c411f85bad2ac","0249cc55455bc6ad",
            "023d6dfce95b3997","01ef64e4dec54025","024a0c2d305eb3cc","025391f6de955621","025391f6de950000"]
NUM_OF_SHUTTLE = 9

# def date_to_timestamp( date):  # convert Y/M/D H:M to x xxx xxx xxx . xxx
#     return time.mktime(time.strptime(date, "%Y/%m/%d %H:%M"))

# def timestamp_to_date(timestamp):  # convert x xxx xxx xxx . xxx to Y/M/D H:M 10 digit
#     return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)) 

def date_to_timestamp(date):  # convert Y/M/D H:M to x xxx xxx xxx . xxx
    time_array = time.strptime(date, "%Y/%m/%d %H:%M")
    timestamp = time.mktime(time_array)
    return timestamp

def timestamp_to_date(timestamp):  # convert x xxx xxx xxx . xxx to Y/M/D H:M
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y/%-m/%-d %-H:%-M", time_local)  # %-m %-d if it's 07/06, will return 7/6
    return dt

def convert_ap_pm(date, time):
    """
    :param date: eg: 2017/7/7
    :param time: eg: 1pm
    :return:     eg: 13:00
    """
    temp = date + ' ' + time
    # print temp
    res = pd.to_datetime(temp).strftime('%-H:%-M')
    return res

#driver dictionary part
#=======================
virtualTable = []
dic_driver = {}
with open('Schedule0918-0924(csv).csv','rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            str1 = ''
            if '\xef\xbb\xbf' in row[0]:
                str1 = row[0].replace('\xef\xbb\xbf','')
                row[0] = str1
                virtualTable.append(row)
            else:
                virtualTable.append(row)

# build dictionary
for i in range(1,len(virtualTable)):#len(virtualTable)
    for x in range(len(virtualTable[i])):
        if virtualTable[i][x] != '': #skip empty slot
            temp =virtualTable[i][x].split(',')#temp = ['Rosh Hashanah Alpha', '8:15 AM - 11:30 AM', 'Reece Pyankaroo']
            temp.append(virtualTable[0][x]) #add date temp =['Rosh Hashanah Alpha', '8:15 AM - 11:30 AM', 'Reece Pyankaroo', '2017/9/21']
            dic_driver.setdefault(temp[2], []).append(temp)

sorted_list = sorted(dic_driver.items(), key=lambda item: len(item[1]), reverse=True)
#=======================


#########   change driver here   #################

print '======================='
for i in range(len(sorted_list)):
    print i
    print sorted_list[i][0]
print '======================='

"""
('Jorge Fernando Flores', [['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/18'], ['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/20']])
"""
name = sorted_list[DRIVER_ID][0]
driver_slots = sorted_list[DRIVER_ID][1]#NO.ith hardest driver schedule


for slot in driver_slots:
# ['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/18']
    date = slot[3]
    time_split= slot[1].split('-')
    route = slot[0].upper()

    start = date + ' ' + convert_ap_pm(date, time_split[0])
    end = date + ' ' + convert_ap_pm(date, time_split[1])

    timestamp_start = date_to_timestamp(start)
    timestamp_end = date_to_timestamp(end)

    
    flag1 = 0
    for key in route_dic.keys():
        # print key
        if route.find(key) != -1 and key != 'L': #route match [['2017/9/5 7:23','763'], ['2017/9/5 7:23','763'] ,['2017/9/5 7:23','763']]
            flag1 =1
            candidate = []
            breakpoint = []
            for items in route_dic[key]:
                if date_to_timestamp(items[0]) < timestamp_start:
                    candidate.append(items)
                if timestamp_start < date_to_timestamp(items[0]) < timestamp_end:
                    breakpoint.append(items)

            if len(candidate) > 0:
                flag = date_to_timestamp(candidate[0][0])
                flag_index = 0
                for i in range(len(candidate)):
                    if date_to_timestamp(candidate[i][0]) > flag:
                        flag = date_to_timestamp(candidate[i][0])
                        flag_index = i
                if len(breakpoint) == 0:
                    if len(candidate[flag_index][1]) < 5:
                        bus_index = SHUTTLE_NUM.index(candidate[flag_index][1])
                    else:
                        bus_index = 8
                    slot.append(bus_index)
                    break
                else:#assume there is only one breakpoint
                    print '!!!!!!!!!there is a break point!!!!!!!!!!!!!!'
                    slot[1] =  slot[1] + breakpoint[0][0]

                    if len(candidate[flag_index][1]) < 5:
                        bus_index = SHUTTLE_NUM.index(candidate[flag_index][1])
                    else:
                        bus_index = 8

                    #bus_index = SHUTTLE_NUM.index(candidate[flag_index][1])
                    slot.append(bus_index)

                    if len(breakpoint[0][1]) < 5:
                        break_index = SHUTTLE_NUM.index(breakpoint[0][1])
                    else:
                        break_index = 8
                    slot.append(break_index)
                    break
            else:
                slot.append('no bus found')
                break


    if flag1 == 0:
        slot.append("route not found")

    print slot
    print '------------->'

            #print route_dic['Epsilon'],,,['2017/9/5 7:23','763']



