# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import json
import gc

# names:a
weekdayname = {}
weekdayname[0] = 'mo'
weekdayname[1] = 'tu'
weekdayname[2] = 'we'
weekdayname[3] = 'th'
weekdayname[4] = 'fr'
weekdayname[5] = 'sa'
weekdayname[6] = 'su'

# info about today:
today = weekdayname[datetime.today().weekday()]
datetoday = time.strftime("%Y%m%d")

# Get carrier:
carriers = open('../sweden/agency.txt', 'r')
carrierdata = {}
for carrier in carriers:
    carrier = carrier.strip()
    parts = carrier.split(',')
    carrierdata[parts[0]] = parts[1]
carriers.close()

'''
# Get times:
deps = open('../sweden/stop_times.txt', 'r')
depsbystop = {}
for dep in deps:
    depdata = {}
    dep = dep.strip()
    parts = dep.split(',')
    stop = parts[3]
    try:
      depsbystop[stop]
    except:
      depsbystop[stop] = []
      
    depdata['tID'] = parts[0]
    depdata['arrTime'] = parts[1]
    depdata['depTime'] = parts[2]
    depdata['seq'] = parts[4]
    depsbystop[stop].append(depdata);
deps.close()

for (stop, data) in depsbystop.items():
    f = open('stop/'+stop+'.json','w')
    f.write(json.dumps(data)) # python will convert \n to os.linesep
    f.close()
'''

depsbystop = {}

# Get trip info data:
trips = open('../sweden/trips.txt', 'r')
tripdata = {}
for trip in trips:
    trip = trip.strip()
    parts = trip.split(',')
    tripid = parts[2]
    tripdata[tripid] = {}
    tripdata[tripid]['rID'] = parts[0]
    tripdata[tripid]['sID'] = parts[1]
    tripdata[tripid]['headSign'] = parts[3]
    tripdata[tripid]['headSignS'] = parts[4]
trips.close()

# Get rout data
routes = open('../sweden/routes.txt', 'r')
routesdata = {}
for route in routes:
    route = route.strip()
    parts = route.split(',')
    routeid = parts[0]
    routesdata[routeid] = {}
    routesdata[routeid]['op'] = parts[1]
    routesdata[routeid]['rNameS'] = parts[2]
    routesdata[routeid]['rNameL'] = parts[3]
    routesdata[routeid]['type'] = parts[5]
routes.close()

# Get specific date data.
dates = open('../sweden/calendar_dates.txt', 'r')
datesdata = {}
for date in dates:
    date = date.strip()
    parts = date.split(',')
    dateid = parts[0]+parts[1]
    datesdata[dateid] = parts[2]
dates.close()

# Get weekley data.
days = open('../sweden/calendar.txt', 'r')
daysdata = {}
for day in days:
    day = day.strip()
    parts = day.split(',')
    dayid = parts[0]
    try:
      daysdata[dayid]
    except:
      daysdata[dayid] = []
    data = {}
    data['mo'] = parts[1]
    data['tu'] = parts[2]
    data['we'] = parts[3]
    data['th'] = parts[4]
    data['fr'] = parts[5]
    data['sa'] = parts[6]
    data['su'] = parts[7]
    data['rangestart'] = parts[8]
    data['rangeend'] = parts[9]
    daysdata[dayid].append(data)
days.close()

while 1==1:
    var = raw_input("Stopid: ")
    dt = datetime.now()
    start = dt.microsecond
    depsbystop[var] = json.loads(open('stop/'+var+'.json').read())

    foroutput = []
    for dep in depsbystop[var]:
	trip = tripdata[dep['tID']]
	route = routesdata[trip['rID']]
	try:
	  date = datesdata[trip['sID']+datetoday]
	except:
	  date = ''
	
	try:
	  weekday = daysdata[trip['sID']]
	except:
	  weekday = ''
	
	noshow = 1
	if date == '' and  weekday == '':
	  noshow = 1
	else:
	  if date == '2':
	    noshow = 1
	  elif date == '1':
	    noshow = 0
	  elif weekday != '':
	    if weekday[0][today] == 1:
	      noshow = 0
	      
	if noshow == 0:
	   outtrip = {}
	   outtrip['direction'] = trip['headSign']
	   outtrip['no'] = trip['headSignS']
	   outtrip['datetime'] = dep['depTime']
	   outtrip['type'] = routesdata[trip['rID']]['type']
	   outtrip['route'] = route['rNameS']
	   outtrip['routetext'] = route['rNameL']
	   outtrip['carrier'] = carrierdata[route['op']]
	   foroutput.append(outtrip)
    
    depsbystop = {}
    print  json.dumps(foroutput)  
    gc.collect()
    dt = datetime.now()
    print dt.microsecond-start
