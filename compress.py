# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Get times:
deps = open('../sweden/stop_times.txt', 'r')
depsbystop = {}
first = 1
for dep in deps:
    if first == 1:
      first = 0
      continue
    depdata = {}
    dep = dep.strip()
    parts = dep.split(',')
    stop = parts[3]
    dep = parts[1].split(":")
    depint = int(dep[0])*3600+int(dep[1])*60+int(dep[2])
    arr = parts[2].split(":")
    arrint = int(arr[0])*3600+int(arr[1])*60+int(arr[2])
    
    with open("stop/"+stop+".csv", "a") as myfile:
        dep = str(depint)
        arr = str(arrint)
        if parts[6]=="1":
            dep = "-"
        if parts[7]=="1":
            arr = "-"
        myfile.write(parts[0]+","+dep+","+arr+"\n")
 

 
deps.close()
    
