# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 13:09:56 2020

@author: Atish
"""

import geopandas as gpd
import pandas as pd
import pysal as ps
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pysal.explore.esda.moran import Moran
from pysal.viz.splot.esda import plot_moran
from pysal.lib.weights import Queen 
from pysal.viz.splot.esda import moran_scatterplot
from splot.esda import lisa_cluster
from esda.moran import Moran_Local
import seaborn as sns
import geoplot

def load_data()
    X = pd.read_csv("F:/codes.csv", names =  ['code' , 'definition' , 'fine' , 'fine2'] )
    Y = pd.read_csv('F:/2014.csv' )
    Y['Violation Precinct'].value_counts
    y1 = Y.iloc[:1000,:]
    y1['Violation Precinct'].value_counts()
    imd_shp2 = 'F:/nypp.shp'
    imd2 = gpd.read_file(imd_shp2)
    whole_data = pd.merge(X, y1, left_on='code', right_on='Violation Code')

def top10():
    print(Y["Plate ID" ].value_counts()[:10])
    print(Y["Registration State" ].value_counts()[:10])
    print(Y["Vehicle Make" ].value_counts()[:10])
    print(Y["Violation Location" ].value_counts()[:10])
    print(Y["Violation Code" ].value_counts()[:10])
    print(Y["Issue Date" ].value_counts()[:10])

def cleaning():
    X['fine'] = X['fine'].replace('Manhattan\xa0 96th St. & below' ,0)
    X['code'] = X['code'].replace('CODE' ,0)
    X['code'] = X['code'].astype(int)
    Y['Violation Precinct']=Y['Violation Precinct'].astype(int)
    
def get_data_plot():
    whole_data = pd.merge(X, Y, left_on='code', right_on='Violation Code')
    whole_data['fine'] = whole_data['fine'].astype(int)
    finetotal = whole_data.groupby('Violation Precinct')['fine'].sum()
    nycplot = pd.merge(imd2, finetotal, left_on='Precinct', right_on='Violation Precinct')
 
def plot_chrolopleth():
    fig, ax = plt.subplots(1, figsize=(11,8.5))
    ax.axis('off')
    ax.set_title('Fine collected ', fontsize=28)
    nycplot.plot(ax=ax, column=nycplot['fine'], scheme='quantiles', legend=True ,cmap='OrRd')
    
    
    precinct_actually_exists = list(imd2['Precinct'])
    precinct_from_data = list(Y['Violation Precinct'].astype(int).unique())
    prob_precincts = {element for element in precinct_from_data if element not in precinct_actually_exists}
    
def morans_plot_fine_and_precinct():
    w = Queen.from_dataframe(imd2)
    mi = Moran( nycplot['fine'], w)
    fig ,ax = moran_scatterplot(mi)
'''
def chloropleth_date:
    y1.groupby('Issue Date' )
    
'''
