#Akshay Jajoo
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from numpy import cumsum
import os
import csv
from itertools import izip
from collections import Counter
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
