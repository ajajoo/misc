#Akshay Jajoo
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from numpy import cumsum
import os
import csv
from itertools import izip
import re
from collections import Counter
import heapq
import math
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches

def plotVectors(graphType, x=[], y=[], xlabel="", ylabel="", fileName="AJgraph", color=[], xTickLabels = [], yTickLabels = [],xLim=[], yLim=[],xMinorTickLabels = [], yMinorTickLabels = [], xMinorTickLabelsLocator = [], yMinorTickLabelsLocator = [], png=False, pdf=False,figHeight = 0, figWidth = 0, xlabelFontSize = 20, ylabelFontSize = 20,xTickLabelFontSize = 18, yTickLabelFontSize = 18, legends=[]): 
# plots a graph of graphType. All the parameter names are self explanatory
# if want to plot cdf of anything pass it as x and pass y as empty vector or any thing, it wont effect but do not skip it
	fig,ax = plt.subplots()
	if figHeight != 0:
		fig.set_figheight(figHeight)
	if figWidth != 0:
		fig.set_figwidth(figWidth)
	if len(color) == 0:
		color = ['b' for i in range(len(x))]
	graphType.lower()
	if graphType == "scatter":
		ax.scatter(x,y,color=color)
	elif graphType == "bar":
		ax.bar(x,y)
	elif graphType == "":
		ax.plot(x,y)
	elif graphType == "cdf":
		cdfx = np.array(x)
		cdfx.sort()
		cdfy = [float((i+1))/float(len(cdfx)) for i in range(len(cdfx))]
		ax.plot(cdfx,cdfy)
		if ylabel == "":
			ylabel = "CDF"
	if(xLim != []):
		ax.set_xlim(xLim)
	if(yLim != []):
		ax.set_ylim(yLim)
	if(xTickLabels != []):
		ax.set_xticklabels(xTickLabels)
	if(yTickLabels != []):
		ax.set_yticklabels(yTickLabels)
	for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(xTickLabelFontSize)
	for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(yTickLabelFontSize)
	if xlabel != "":
		plt.xlabel(xlabel,fontsize = xlabelFontSize)
	if ylabel != "":
		plt.ylabel(ylabel, fontsize = ylabelFontSize)	
	if(xMinorTickLabels != []):
		if(xMinorTickLabelsLocator != []):
			ax.xaxis.set_minor_locator(ticker.FixedLocator(xMinorTickLabelsLocator))
		ax.xaxis.set_minor_formatter(ticker.FixedFormatter(xMinorTickLabels))
	if(yMinorTickLabels != []):
		if(yMinorTickLabelsLocator != []):
			ax.yaxis.set_minor_locator(ticker.FixedLocator(yMinorTickLabelsLocator))
		ax.yaxis.set_minor_formatter(ticker.FixedFormatter(yMinorTickLabels))
	for tick in ax.xaxis.get_minor_ticks():
                tick.label.set_fontsize(18)
	for tick in ax.yaxis.get_minor_ticks():
                tick.label.set_fontsize(18)
	plt.gcf().subplots_adjust(bottom=0.17)
	if legends !={}:
		patchesSym = []
		patchesText = []
		for i in range(0,len(legends),2):
			patchesSym.append(mpatches.Circle((0, 0), 1, fc=legends[i],ec="none"))
			patchesText.append(legends[i+1])
		plt.legend(patchesSym,patchesText,prop={'size':6},loc="upper left")
	if pdf:
		pp = PdfPages(fileName+'.pdf')
		pp.savefig(fig)
		pp.close()
	if png:
		plt.savefig(fileName)

def writeToCSV(listOfColumns,columnNames,outputFile,mode='wb'):
	with open(outputFile+'.csv',mode) as fi:
		writer = csv.writer(fi)
		writer.writerow(columnNames)
		for i in range(len(listOfColumns[0])):
			temp = []
			for j in range(len(listOfColumns)):
				temp.append(listOfColumns[j][i])
			writer.writerow(temp)
		#writer.writerows(izip(listOfColumns))

def getFileFirstName(fullName):
	extentionIndex = -4
	for i in range(1,len(fullName)):
		if fullName[-1*i] == '.':
			return fullName[0:-1*i]

class TraceObject(object):
# maintains trace info a dictionary keyed by their Job name. Make 1 object for 1 execution. This takes input file in format coflow-benchmark trace.
	def __init__(self,inputFile):
		self.baseAddress = os.getcwd()#'/home/ajajoo/Desktop/Research/coflow/coflowsim-master/results/'
		self.data = {}
		with open(self.baseAddress+'/'+inputFile,'r') as f:
			lines = f.readline()
			for line in f:	
				line = line.replace(':',' ');
				nos = line.split() 
				jName = "JOB-"+str(nos[0])
				self.data[jName] = {};
				self.data[jName]["arrivalTime"] = float(nos[1])	
				self.data[jName]["numMappers"] = float(nos[2])	
				index = int(self.data[jName]["numMappers"]) + 3
				self.data[jName]["mapperPortList"] = nos[3:index]	
				self.data[jName]["numReducers"] = float(nos[index])
				index +=1 
				self.data[jName]["reducerPortList"] = nos[index:][0:][::2]
				self.data[jName]["reducerTotalData"] = nos[index:][1:][::2]
				for x in range(len(self.data[jName]["reducerTotalData"])):
					self.data[jName]["reducerTotalData"][x] = float(self.data[jName]["reducerTotalData"][x])*1024*1024
				self.data[jName]["length"] = max(self.data[jName]["reducerTotalData"])/len(self.data[jName]["mapperPortList"])
				self.data[jName]["size"] = sum(self.data[jName]["reducerTotalData"])	
	def __getitem__(self,key):
		return self.data[key]
	def getArrayByKey(self,key):
		toReturn = {};
		for x in self.data:
			toReturn[x] = self.data[x][key];
		return toReturn;

class ResultObject(object):
# maintains results in a dictionary keyed by their Job name. Make 1 object for 1 execution.
	def __init__(self,inputFile):
		self.baseAddress = os.getcwd()#'/home/ajajoo/Desktop/Research/coflow/coflowsim-master/results/'
		self.data = {}
		with open(self.baseAddress+'/'+inputFile,'r') as f:
			lines = f.readlines()
			self.totalCCT = float(lines[-1].split()[0])
			for line in lines:
				line = line.split()
				if line[0][0:4] != "JOB-":
					continue
				else:
					self.data[line[0]] = {};
				self.data[line[0]]["simulatedstarttime"] = float(line[1]);	
				self.data[line[0]]["simulatedfinishtime"] = float(line[2]);	
				self.data[line[0]]["nummappers"] = float(line[3]);	
				self.data[line[0]]["numreducers"] = float(line[4]);	
				self.data[line[0]]["totalshufflebytes"] = float(line[5]);	
				self.data[line[0]]["maxshufflebytes"] = float(line[6]);	
				self.data[line[0]]["simulationDuration"] = float(line[7]);	
				self.data[line[0]]["deadline"] = float(line[8]);	
				self.data[line[0]]["simulatedshuffleindividualsums"] = float(line[9]);
	def __getitem__(self,key):
		return self.data[key]
	def getData(self,editable=False):
		if editable:
			return self.data
		else:
			return self.data.copy()
	def getArrayByKey(self,key):
		toReturn = {}
		for job in self.data.keys():
			toReturn[job] = float(self.data[job][key])
		return toReturn
	def normalizeWithOtherResults(self, otherObject, comparisonKey):
	# normalizes self relative to other
		results = {}
		otherData = otherObject.getData()
		if len(self.data.keys())!=len(otherData.keys()):
			return results
		for key in self.data.keys():
			results[key] = self.data[key][comparisonKey]/otherData[key][comparisonKey]
		del otherData
		return results
	def getEndQueueForCoflow(self,coflowName):
		qMin = 1024*1024*10
		E = 10
		q = math.log(self.data[coflowName]["totalshufflebytes"]/qMin,E)
		return 0 if q <= 0 else int(q) + 1
	def getEndQueueForAllCoflows(self):
		toReturn = {}
		for coflow in self.data:
			toReturn[coflow] = self.getEndQueueForCoflow(coflow)
		return toReturn
