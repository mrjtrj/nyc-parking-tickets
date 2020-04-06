# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:48:12 2020

Violation Codes and their meaning: https://data.cityofnewyork.us/widgets/ncbg-6agr

Old labels for pie chart
labs = {"Angle Parking":[59,60],
                    "Double Parking":[46,47],
                    "Expired Meter":[34,37,42,43],
                    "No reciept":[38,69],
                    "No Parking":[20,21,23,24,27],
                    "No Standing":[10,11,12,13,14,15,16,17,18,19,20,22,25,26,30,31,64,81,89],
                    "Obstructing path":[9,98],
                    "Overtime":[6,28,32,39,65],
                    "Plate Issues":[74,75,82],
                    "Others":[29,62,48,57,5,4,50,66,56,55,49,1,7,33,40,8,83,71,72,52,58,86,
                              41,80,78,63,68,2,99,77,54,67,36,44,84,96,70,73,93,53,35,51,85,45,87,88,79,3,97,91,90,76,92,61]}
            
@author: TUSHAR
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
from matplotlib import cm, colors

year = list(range(2015, 2021))
def group_data(dataframe, groupby):
    dataframe = dataframe.groupby(by=dataframe[groupby],as_index=False).count() 
    return dataframe[[groupby,'Summons Number']]

def preprocessing(filepath):
    '''
    Reads the csv files, and then converts Issue date to date and month
    '''
    dataframe = pd.read_csv(filepath) ## Using Pandas
    dataframe['date'] = pd.to_datetime(dataframe['Issue Date']) ## Convert date to datetime
    dataframe['month'] = dataframe['date'].dt.month ## Extract month from Issue Date
    return dataframe

def BarPlot_2Var(ax, data, column, groupby, year, b_colors, labels):
    '''
    Bar plots for 2 variables
    '''
    ## Grouped data for bar plot
    NY_month_data = group_data(data[data[column]==var], groupby)    # NY data for all months
    NotNY_month_data = group_data(data[data[column]!=var], groupby) # other cities data for all months   
        
    ## plotting the graph
    ax.bar(NY_month_data[groupby] , NY_month_data['Summons Number'], color = b_colors[0], width = 0.5) 
    ax.bar(NotNY_month_data[groupby], NotNY_month_data['Summons Number'], color = b_colors[1], width = 0.5)
    
    ax.set_xticks(NY_month_data[groupby], labels)
    
    ## Legend labels
    blue_patch=mpatches.Patch(color=b_colors[0],label='New York') 
    green_patch=mpatches.Patch(color=b_colors[1],label='Other Cities') ## Legend labels
    ax.legend(handles=[blue_patch,green_patch]) #providing the labels
    
    ax.set_xlabel(groupby)
    ax.set_ylabel('Number of tickets')
    ax.set_title('Parking tickets for the year '+str(year-1))
    return ax 

def PiePlot(ax, values, title, col):
    '''
    Pie chart
    '''
    if col in  list(values.columns):
        label, data = np.unique(values[col], return_counts=True)
        if col == 'Violation Code': 
            ## Defining the violation code merges as a dictionary
            labs = {"Misc":[35,41,90,91,94],
                    "No Parking":[20,21,23,24,27],
                    "No Standing":[3,4,5,6,8,10,11,12,13,14,15,16,17,18,19,22,25,26,30,31,40,44,54,57,58,63,64,77,78,81,89,92],
                    "Permit/Doc Issue":[1,2,29,70,71,72,73,76,80,83,87,88,93,97],
                    "Plate Issues":[74,75,82],
                    "Obstructing Path":[7,9,36,45,46,47,48,49,50,51,52,53,55,56,59,60,61,62,66,67,68,79,84,96,98],
                    "Overtime":[28,32,33,34,37,38,39,42,43,65,69,85,86]
                    }
            ## Count based on the grouping
            temp = defaultdict(list)
            for i in range(len(label)):
                for key, val in labs.items():
                    if label[i] in val:
                        if temp[key] == []:
                            temp[key] = 0
                        else:
                            temp[key] = temp[key]+data[i]

            ## Ordering data based on the dictionary 
            label, data  = list(), list()
            for key in labs.keys():
                label.append(key)
                data.append(temp[key])    
                
        ## Defining color for each category
        temp = defaultdict(list)
        for l,c in zip(labs,cm.tab20(range(len(labs)))):
            temp[l]=c

        centre_circle = plt.Circle((0,0),0.85,fc='white') ## radius to make it like a donut
        explode = np.full(len(label), 0.04) ## Gaps between the categories
        
        pat = ax.pie(list(map(lambda x: x*100/sum(data), data)), labels=label, autopct='%1.1f%%', startangle=90, pctdistance=0.6, explode = explode)
        if col == 'Violation Code':
            for pie_wedge in pat[0]:
                pie_wedge.set_edgecolor('white')
                pie_wedge.set_facecolor(temp[pie_wedge.get_label()]) # Assigning color code for each catergory
        
        ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title(title, pad=20)
        plt.gcf().gca().add_artist(centre_circle)
    return ax

def EDAplot(ax, parking_data, year, column, var, groupby, labels, plotype):
    if plotype=='bar_2v':
        ax = BarPlot_2Var(ax, parking_data, column=column,groupby=groupby, year=year, b_colors=['b', 'r'], labels=labels)
    
    elif plotype=='pie':
        ax = PiePlot(ax, parking_data, 'Parking ticket '+str(column)+' for the year '+str(year-1), column)
    return ax

def EDA(year, groupby, labels, pt, plotdim, col, var):
    fig = plt.figure(figsize=(30, 25))
    axs=plt.GridSpec(plotdim[0], plotdim[1], hspace=0.15, wspace=0.02)
    for i in range(len(year)):
        filepath = "G:\Downloads\Parking_Violations_Issued_-_Fiscal_Year_"+str(year[i])+".csv"
        parking_data = preprocessing(filepath)
        EDAplot(ax= fig.add_subplot(axs[i]), parking_data=parking_data, year=year[i], 
           column=col, var=var, groupby=groupby, labels=labels, plotype=pt)
    plt.savefig('EDA_'+str(col)+'_'+str(pt)+'.png',  bbox_inches='tight')
    
    
groupby = 'month'
labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']  
col='Registration State'
var='NY' 
EDA(year, groupby, labels, pt='bar_2v', plotdim=[3,2], col=col, var=var)  

groupby = ''
labels=[]  
col='Violation Code'
var='' 
EDA(year, groupby, labels, pt='pie', plotdim=[3,2], col=col, var=var)  
