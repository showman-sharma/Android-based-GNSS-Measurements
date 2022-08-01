import pandas as pd
import numpy as np
from math import radians
from math import pi
from sklearn.metrics.pairwise import haversine_distances as havd
import matplotlib.pyplot as plt

cases =  ['inside','balcony','outside']
i = 0

for case in cases:
	print('## CASE: '+case)

	#Read log files
	with open(case+'.txt') as f:
		lines = f.readlines()
	statusLines = []
	fixLines = []
	for line in lines:
	    if line[:6] == 'Status' and line[7]!='U':
	        statusLines.append(line)
	    elif line[:7] == 'Fix,GPS':
	        fixLines.append(line)	

	#Extract Status Data
	statusData = [((line[7:-2].split(','))) for line in statusLines]
	statusdf = pd.DataFrame(statusData, columns = ['UnixTimeMillis','SignalCount','SignalIndex','ConstellationType','Svid','CarrierFrequencyHz','Cn0DbHz','AzimuthDegrees','ElevationDegrees','UsedInFix','HasAlmanacData','HasEphemerisData'])#,',BasebandCn0DbHz '])        
	statusdf[['UnixTimeMillis','SignalCount','SignalIndex','ConstellationType','Svid','UsedInFix','HasAlmanacData','HasEphemerisData']] = statusdf[['UnixTimeMillis','SignalCount','SignalIndex','ConstellationType','Svid','UsedInFix','HasAlmanacData','HasEphemerisData']].astype('int64')
	statusdf[['Cn0DbHz', 'AzimuthDegrees', 'ElevationDegrees']] = statusdf[['Cn0DbHz', 'AzimuthDegrees', 'ElevationDegrees']].astype(float) 

	#Extract Fix Data
	fixData = [((line[8:-2].split(','))) for line in fixLines]
	fixdf = pd.DataFrame(fixData, columns = ['LatitudeDegrees','LongitudeDegrees','AltitudeMeters','SpeedMps','AccuracyMeters','BearingDegrees','UnixTimeMillis','SpeedAccuracyMps','BearingAccuracyDegrees','elapsedRealtimeNanos'])
	fixdf = fixdf.astype(float)

	#Task 2
	# Location coordinates
	loc_lat = np.radians(np.array(fixdf['LatitudeDegrees']))
	loc_lon = np.radians(np.array(fixdf['LongitudeDegrees']))
	locs = [[loc_lat[i],loc_lon[i]] for i in range(len(loc_lon))]
	mean_loc = [np.mean(loc_lat), np.mean(loc_lon)]
	print('mean coordinates of '+ case+' = ',[mean_loc[0]*180/pi,mean_loc[1]*180/pi])
	errors = [havd([loc,mean_loc])[0][1]* 6371000 for loc in locs]
	N = len(errors)
	# getting data of the histogram
	count, bins_count = np.histogram(errors, bins=N)
	  
	# finding the PDF of the histogram using count values
	pdf = count / sum(count)
	  
	# using numpy np.cumsum to calculate the CDF
	# We can also find using the PDF values by looping and adding
	cdf = np.cumsum(pdf)
	  
	# plotting PDF and CDF
	plt.figure(i, figsize = (10,10));
	i += 1;
	plt.plot(bins_count[1:], pdf, color="red", label="PDF");
	plt.plot(bins_count[1:], cdf, label="CDF");
	plt.xlabel('error of distance in meters');
	plt.ylabel('probability');
	plt.title(case)
	plt.legend();
	
	#print variance and mean of errors in meters
	print('variance of the error ('+case+ ') = {} meters '.format(np.var(errors)))
	print('mean of the error ('+case+ ') = {} meters '.format(np.mean(errors)))


	#task 3
	#Extract Satellite data used in fix

	useddf = statusdf[np.logical_and(statusdf['UsedInFix']==1 ,statusdf['ConstellationType']==1)]
	
	fixtostatusMap = {} #a dictionary of status line dataframes corresponding to each fix line
	statuses = []
	for line in lines:
	    if line[:6] == 'Status' and line[7]!='U':# and line[-1] == '1':
	        statuses.append((line[7:-2].split(',')))
	    elif line[:7] == 'Fix,GPS':
	        
	        sdf = pd.DataFrame(statuses, columns = ['UnixTimeMillis','SignalCount','SignalIndex','ConstellationType','Svid','CarrierFrequencyHz','Cn0DbHz','AzimuthDegrees','ElevationDegrees','UsedInFix','HasAlmanacData','HasEphemerisData'])#,',BasebandCn0DbHz '])
	        fixtostatusMap[line] = sdf[sdf['UsedInFix']=='1']
	        statuses = []	

	#counting individual satellites used in each fix        
	countSats = [len(fixtostatusMap[fix]['Svid'].unique()) for fix in fixtostatusMap]
	
	# a.
	medCountSats = (np.median(countSats))
	print('median of # of satellites used per fix ('+case+ ') = ', medCountSats)

	#b.
	print('correlation between # satellites and error = ',np.corrcoef(countSats, errors)[0][1])
	plt.figure(i, figsize = (10,10));
	i += 1;
	plt.scatter(countSats, errors, alpha =0.1);
	plt.xlabel('number of satellites used in fix',size = 15);
	plt.ylabel('error in meters',size = 15);
	plt.title(case)

	#c.
	SNRs = [fixtostatusMap[fix]['Cn0DbHz'].astype(float).mean() for fix in fixtostatusMap]
	goodSNR = [i for i in range(len(SNRs)) if str(SNRs[i])!='nan']
	print('correlation between SNR and error = ',np.corrcoef(np.array(SNRs)[goodSNR], np.array(errors)[goodSNR])[0][1])

	plt.figure(i, figsize = (10,10));
	i += 1;
	plt.scatter(SNRs, errors, alpha = 0.1);
	plt.xlabel('Average SNR',size = 15);
	plt.ylabel('error in meters',size = 15);
	plt.title(case)	


	#4
	#a.
	print('\n\nTABLE OF SATELLITES USED ON FIX ('+case+ ')')
	satdf = useddf[['Svid','Cn0DbHz', 'AzimuthDegrees', 'ElevationDegrees']].groupby(['Svid']).mean()
	print(satdf)

	#b.
	fig = plt.figure(i,figsize=(10,10))
	i += 1
	ax = fig.add_subplot(projection='polar')
	ax.plot(satdf['AzimuthDegrees']*np.pi/180 , satdf['Cn0DbHz'], 'ro')
	ax.grid(True)
	#steps to align the plots according to map
	ax.set_theta_zero_location("N")
	ax.set_theta_direction(-1)
	ax.set_title('Average Azimuth Angle vs SNR ('+case+')', va='bottom')

	#c
	fig = plt.figure(i,figsize=(10,10))
	i += 1
	ax = fig.add_subplot(projection='polar')
	c = ax.scatter(satdf['ElevationDegrees']*np.pi/180 , satdf['Cn0DbHz'], c=satdf['ElevationDegrees'], s=100, cmap='hsv', alpha=0.75)

	ax.set_thetamin(0)
	ax.set_thetamax(90)
	plt.title('Average Elevation Angle vs SNR ('+case+')')




	print('_____________________________________')
plt.show()	