import types
import pandas as pd
import numpy as np
import datetime
import operator
import os
import csv
import time
import datetime
from math import radians, cos, sin, asin, sqrt, fabs

SHUTTLE_NUM = ["763","747","762","748","787","788","528","526","[Deleted: ID 389]"]
SHUTTLE_INDEX = [0,1,2,3,4,5,6,7]
PHONE_ID = ["02597a5b9e75cf6c", "02596c2b9e85bf69", "025c411f85bad2ac","0249cc55455bc6ad",
            "023d6dfce95b3997","01ef64e4dec54025","024a0c2d305eb3cc","025391f6de955621"]
NUM_OF_SHUTTLE = 8

UULat = 42.086942806500474
UULon = -75.96704414865724
def hav(theta):
	s = sin(theta / 2)
	return s * s
def get_distance(lat0, lng0, lat1, lng1):
	r = 6371
	lat0 = radians(lat0)
	lat1 = radians(lat1)
	lng0 = radians(lng0)
	lng1 = radians(lng1)

	dlng = fabs(lng0 - lng1)
	dlat = fabs(lat0 - lat1)
	h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
	distance = 2 * r * asin(sqrt(h)) * 1000
	return distance     # return meter

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


if __name__=="__main__":
	# virtialRouteTable = []
	dic = {}
	with open('Gps.csv','rU') as csvfile:
	        csvreader1 = csv.reader(csvfile)
	        for row in csvreader1:
	            str1 = ''
	            if '\xef\xbb\xbf' in row[0]:
	                str1 = row[0].replace('\xef\xbb\xbf','')
	                row[0] = str1
	                dic.setdefault(row[1], []).append(row)
	                # virtialRouteTable.append(row)
	            else:
	            	dic.setdefault(row[1], []).append(row)
	                # virtialRouteTable.append(row)
	"""
	['6704101', '024a09d94ab01756', '1505667614326', '42.10743427', '-75.98704116', '0', '0', '0']
	   0                 1                  2                3              4         
	 GPS file
	"""
	"""
	['Eve CHI', '10:00 PM - 12:30 AM', 'Administrator', '2017/09/12', 7] result from driverlist
	"""
	bus = 4
	date = '2017/9/25'
	schedule = ['10:01 AM - 11:00 AM,CS7']
	fo = open("foo.txt", "w")
	for slot in schedule:
		detail = slot.split(',')
		route = detail[1]
		times = detail[0].split('-')
		start = date + ' ' + convert_ap_pm(date, times[0])
		end = date + ' ' + convert_ap_pm(date, times[1])
		timestamp_start = date_to_timestamp(start)
		timestamp_end = date_to_timestamp(end)
		temp = []
		flag = 0
		for gps_point in dic[PHONE_ID[bus]]:

			x = timestamp_to_date(int(gps_point[2])/1000)
			y = int(gps_point[2])/1000
			#print x
			if y >= timestamp_start and y <= timestamp_end:
				temp.append(gps_point)

				fo.write(gps_point[3])
				fo.write(',')
				fo.write(gps_point[4])
				fo.write('\n')

				flag = 1
		if flag == 0:
			print 'no data during this time slot!'
		fo.close
		if flag == 1:
			print timestamp_to_date(int(temp[0][2])/1000)
			print timestamp_to_date(int(temp[-1][2])/1000)
			print get_distance(UULat,UULon,float(temp[0][3]),float(temp[0][4]))











