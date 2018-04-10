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

# UULat = 42.086942806500474
# UULon = -75.96704414865724

UULat = 42.08687988
UULon = -75.96715875

# UUendLat = 42.08698128
# UUendLon = -75.96582985
UUendLat = 42.08687988
UUendLon = -75.96715875

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
	test = ['PM ALPHA', '7:00 PM - 9:00 PM', 'Gaddi Eshun', '2017/09/12', 4]
	bus = test[-1]# 6
	date = test[3]# '2017/09/11'
	schedule = [ '7:00 PM - 7:25 PM'+',OAK', '7:25 PM - 8:10 PM'+',WSOUT', '8:10 PM - 8:55 PM'+',WSIN']

	# bus = 6
	# date = '2017/9/13'
	# schedule = [ '12:00 PM - 2:30 PM,CS7','12:00 PM - 2:30 PM,CS7']
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

		# get timestamp_start and timestamp_end
		if dic.has_key(PHONE_ID[bus]):
			buslist = dic[PHONE_ID[bus]]
			starflag = 0
			endflag = 0
			newstartStamp = timestamp_start
			newendStamp = timestamp_end
			print timestamp_to_date(timestamp_start)
			print timestamp_to_date(timestamp_end)
			for i in range(0,len(buslist),30):
				y = int(buslist[i][2])/1000
				if y >= timestamp_start and y < timestamp_end:
					lastone = buslist[i]
					startdistance = get_distance(UULat,UULon,float(buslist[i][3]),float(buslist[i][4]))
					if starflag == 0:
						if startdistance > 350 :
							timestamp_start = timestamp_start + 60
							print 'add 60s'
					if startdistance < 300 and starflag == 0:
						starflag = 1
						newstartStamp = y
						print 'reset-start'
						print timestamp_to_date(newstartStamp)

				elif y >= timestamp_end and endflag == 0:
					new = get_distance(UUendLat,UUendLon,float(buslist[i][3]),float(buslist[i][4]))
					if new > 350:
						timestamp_end = timestamp_end + 60
					if new < 300:
						newendStamp = y
						print 'reset-end'
						print timestamp_to_date(newendStamp)
						endflag = 1
		# "test"+str(count)+".csv"
		with open(route+".csv","w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(["lat","lng","comment"])

			if dic.has_key(PHONE_ID[bus]):
				buslist = dic[PHONE_ID[bus]]
				mark = 0
				print 'newnewnewnewnew'
				print timestamp_to_date(newstartStamp)
				print timestamp_to_date(newendStamp)
				for i in range(0,len(buslist),30):
					y = int(buslist[i][2])/1000
					x = timestamp_to_date(y)
					if y >= newstartStamp and y <= newendStamp:
						temp.append(buslist[i])
						row = [(float(buslist[i][3]),float(buslist[i][4]),mark)]
						mark += 1
						writer.writerows(row)
						flag = 1

				if flag == 0:
					print 'no data during this time slot!'
				if flag == 1:
					print 'result'
					print timestamp_to_date(int(temp[0][2])/1000)
					print timestamp_to_date(int(temp[-1][2])/1000)
					print get_distance(UULat,UULon,float(temp[0][3]),float(temp[0][4]))
					print get_distance(UUendLat,UUendLon,float(temp[-1][3]),float(temp[-1][4]))
				print 'data write to '+route+".csv"+'\n'
			else:
				print 'This bus has no data in GPS file!'









