import types
import pandas as pd
import numpy as np
import datetime
# import DriverSchedule as ds
import operator

import os
import csv
import time
import datetime
from math import radians, cos, sin, asin, sqrt, fabs

WHICH_DRIVER = 1
VIRTUAL = 'virtualSchedule(1).csv'
DRIVER = 'Virtual-file.csv'
# select the Driver you want

SHUTTLE_NUM = ["763","747","762","748","787","788","528","526","[Deleted: ID 389]"]
SHUTTLE_INDEX = [0,1,2,3,4,5,6,7]
PHONE_ID = ["02597a5b9e75cf6c", "02596c2b9e85bf69", "025c411f85bad2ac","0249cc55455bc6ad",
            "023d6dfce95b3997","01ef64e4dec54025","024a0c2d305eb3cc","025391f6de955621","025391f6de950000"]
NUM_OF_SHUTTLE = 8

def get_result(sorted_list):
    new_dic = {}
    exist_dic = {}
    # new_dic: dictionary that has everything
    # exist_dic : dictionary that only has bus[0,1,2,3,4,5,6,7]
    for number in range(len(sorted_list)):
        name = sorted_list[number][0]
        driver_slots = sorted_list[number][1]#NO.ith hardest driver schedule
        new_dic[name] = []
        exist_dic[name] = []
        #sort driver_slots according to time
        sorted_driver_slots = sorted(driver_slots, key=lambda item: date_to_timestamp(item[3] +' ' +convert_ap_pm(item[3], item[1].split('-')[0])))
        #=====================
        for slot in sorted_driver_slots:
        # ['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/18']
            date = slot[3]
            time_split= slot[1].split('-')
            route1 = slot[0].upper()

            if route1.find('PARTIAL'):
                route = route1.split(' PARTIAL')[0]

            start = date + ' ' + convert_ap_pm(date, time_split[0])
            end = date + ' ' + convert_ap_pm(date, time_split[1])

            timestamp_start = date_to_timestamp(start)
            timestamp_end = date_to_timestamp(end)
            flag1 = 0
            for key in route_dic.keys():
                #if route.find(key) != -1 and key != 'L': #route match [['2017/9/5 7:23','763'], ['2017/9/5 7:23','763'] ,['2017/9/5 7:23','763']]
                if route.find(key) != -1 and key != 'L' and len(key) + route.index(key) == len(route):
                    #print key
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
                        for i in range(len(candidate)):#from all smaller ones find the biggest one index as flag_index.
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
                            #print '!!!!!!!!!there is a break point!!!!!!!!!!!!!!'
                            slot[1] =  slot[1] + breakpoint[0][0]

                            if len(candidate[flag_index][1]) < 5:
                                bus_index = SHUTTLE_NUM.index(candidate[flag_index][1])
                            else:
                                bus_index = 8
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
            #print slot
            new_dic[name].append(slot)
            if slot[-1] in SHUTTLE_INDEX:
                exist_dic[name].append(slot)
            #print '------------->'

    return new_dic, exist_dic

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


virtialRouteTable = []
route_dic = {}
with open(VIRTUAL,'rU') as csvfile:
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


#===================================================================

#driver dictionary part
#=======================
virtualTable = []
dic_driver = {}
with open(DRIVER,'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            str1 = ''
            if '\xef\xbb\xbf' in row[0]:
                str1 = row[0].replace('\xef\xbb\xbf','')
                row[0] = str1
                virtualTable.append(row)
            else:
                virtualTable.append(row)

for i in range(1,len(virtualTable)):
#['Jorge Fernando Flores', '2017/09/11', 'Monday', 'Sunrise Pre-trip ALPHA', '6:30 AM-7:00 AM', '0.5', 'details', '']
    if virtualTable[i][7] == '':
        temp =[]
        newtime = virtualTable[i][4].replace('-',' - ')
        temp.extend([virtualTable[i][3], newtime ,virtualTable[i][0],virtualTable[i][1]])
        # print temp[2]
        # print temp
        x = temp[2].replace(' ','')
        if x.isalpha():
            dic_driver.setdefault(temp[2], []).append(temp)
    elif virtualTable[i][7].find('Unapproved') == -1:
        if virtualTable[i][7].find(':') != -1:
            new = virtualTable[i][7].split(': ')
            newDriver = new[1].replace('.','')
            temp =[]
            newtime = virtualTable[i][4].replace('-',' - ')
            temp.extend([virtualTable[i][3], newtime ,newDriver,virtualTable[i][1]])
            # print temp[2]
            # print temp
            x = temp[2].replace(' ','')
            if x.isalpha():
                dic_driver.setdefault(temp[2], []).append(temp)
"""
('Jorge Fernando Flores', [['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/18'], ['Sunrise Pre-trip ALPHA', '6:30 AM - 7:00 AM', 'Jorge Fernando Flores', '2017/9/20']])
"""
sorted_list1 = sorted(dic_driver.items(), key=lambda item: len(item[1]), reverse=True)

"""
result: dictionary that has everything
exist_result : dictionary that only has bus [0,1,2,3,4,5,6,7]
"""
result,exist_result= get_result(sorted_list1)

sorted_result = sorted(exist_result.items(), key=lambda item: len(item[1]), reverse=True)
# print driver ID ,driver name, and bus set
print '======================='
for i in range(len(sorted_result)):
    print '--',i,'--'
    bus = []
    for x in sorted_result[i][1]:
        bus.append(x[-1])
        if isinstance(x[-2],int):
            bus.append(x[-2])
    print len(bus),"times",bus
    print "set:",list(set(bus))
    print sorted_result[i][0]
    print '-------------->' 
print '======================='

# print chosen driver's slots
for x in sorted_result[WHICH_DRIVER][1]:
    print x
    print '-------------->'


#===========

