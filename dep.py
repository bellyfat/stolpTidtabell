# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
import json
import gc
import tornado.web
import pickle
import gzip


# names:a
weekdayname = {}
weekdayname[0] = 'mo'
weekdayname[1] = 'tu'
weekdayname[2] = 'we'
weekdayname[3] = 'th'
weekdayname[4] = 'fr'
weekdayname[5] = 'sa'
weekdayname[6] = 'su'

def save(object, filename, bin = 1):
	"""Saves a compressed object to disk
	"""
	file = gzip.GzipFile(filename, 'wb')
	file.write(pickle.dumps(object, bin))
	file.close()


def load(filename):
	"""Loads a compressed object from disk
	"""
	file = gzip.GzipFile(filename, 'rb')
	buffer = ""
	while 1:
		data = file.read()
		if data == "":
			break
		buffer += data
	object = pickle.loads(buffer)
	file.close()
	return object

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
    save(data, 'stop/'+stop+'.dat') # python will convert \n to os.linesep
'''

class tripinfo:
  rID = ''
  sID = ''
  headSign = ''
  headSignS = ''

# Get trip info data:
trips = open('../sweden/trips.txt', 'r')
tripdata = {}
for trip in trips:
    trip = trip.strip()
    parts = trip.split(',')
    tripid = parts[2]
    tripdata[tripid] = tripinfo()
    tripdata[tripid].rID = parts[0]
    tripdata[tripid].sID = parts[1]
    tripdata[tripid].headSign = parts[3]
    tripdata[tripid].headSignS = parts[4]
trips.close()

class routeinfo:
   op = ''
   rNameS = ''
   rNameL = ''
   vtype = ''

# Get rout data
routes = open('../sweden/routes.txt', 'r')
routesdata = {}
for route in routes:
    route = route.strip()
    parts = route.split(',')
    routeid = parts[0]
    routesdata[routeid] = routeinfo()
    routesdata[routeid].op = parts[1]
    routesdata[routeid].rNameS = parts[2]
    routesdata[routeid].rNameL = parts[3]
    routesdata[routeid].vtype = parts[5]
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

class getdep(tornado.web.RequestHandler):
  
    @tornado.web.asynchronous
    def get(self, var):
	global tripdata
	global routesdata
	global datesdata
	global weekdayname

	
	# Get time same before and after:
	yesterdaysec = datetime.datetime.fromtimestamp(time.time()-86400)
	todaysec = datetime.datetime.fromtimestamp(time.time())
	tomorrowsec = datetime.datetime.fromtimestamp(time.time()+86400)
	
	# Weekday:
	yesterday = weekdayname[yesterdaysec.weekday()]
	today = weekdayname[todaysec.weekday()]
	tomorrow = weekdayname[tomorrowsec.weekday()]
	
	# Get date of today
	dateyesterday = yesterdaysec.strftime("%Y%m%d")
	datetoday = todaysec.strftime("%Y%m%d")
	datetomorrow = tomorrowsec.strftime("%Y%m%d")
	realdatetoday = todaysec.strftime("%Y-%m-%d")
	
	depsbystop = {}
        try:
	  depsbystop[var] = load('stop/'+var+'.dat')
	except:
	  self.write({"Error":"stop not found"})
	  self.finish()
	  return

	foroutput = []
	for dep in depsbystop[var]:
	    trip = tripdata[dep['tID']]
	    route = routesdata[trip.rID]
	    timeparts = dep['depTime'].split(':')
	    sectrip = int(timeparts[0])*3600+int(timeparts[1])*60+int(timeparts[2])
	    
	    if sectrip > 86400:
	      usedate = dateyesterday
	      useday = yesterday
	      dep['depTime'] = datetime.datetime.fromtimestamp(sectrip-86400).strftime("%H:%M:%S")
	      
	    else:
	      usedate = datetoday
	      useday = today
	    
	    try:
	      date = datesdata[trip.sID+usedate]
	    except:
	      date = ''
	
	    try:
	      weekday = daysdata[trip.sID]
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
		if weekday[0][useday] == 1:
		  noshow = 0
		
	    if noshow == 0:
	      outtrip = {}
	      outtrip['direction'] = trip.headSign
	      outtrip['no'] = trip.headSignS
	      outtrip['datetime'] = realdatetoday + ' ' + dep['depTime']
	      outtrip['type'] = routesdata[trip.rID].vtype
	      outtrip['route'] = route.rNameS
	      outtrip['routetext'] = route.rNameL
	      outtrip['carrier'] = carrierdata[route.op]
	      if todaysec < datetime.datetime.strptime(outtrip['datetime'],"%Y-%m-%d %H:%M:%S"):
		foroutput.append(outtrip)
	      
	depsbystop = {}
	self.write({"trips":foroutput})
	self.finish()
