#!/usr/bin/env python
import psutil, time, json

stats = psutil.cpu_percent(percpu=True)
mem = psutil.virtual_memory()
disk = psutil.disk_usage('/')
avg=psutil.getloadavg()

