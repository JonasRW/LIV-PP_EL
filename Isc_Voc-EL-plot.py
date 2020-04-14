# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:04:18 2020

@author: Jonas Rydtun Winsvold

This script utilizes the "getIsc" and "getEL" modules to import Isc and
intensity averages of modules. In order to plot them togehter for corrolation
comparison, the data is normalized. 
"""

from getPP import getPP,getELPP
from getEL import getEL
import matplotlib.pyplot as plt
import numpy as np
file_path_EL = 'C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas\\6018xx-191015-test-tif\\6018xx-191015_Iav.xlsx'
folder_with_data = ('C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas')

#%%------------Importing data with "getPP" and "getEL"
PP = getPP(1000,folder_with_data)
EL_int_data, EL_int_av = getEL(file_path_EL)

#%% Separating and normalizing Isc and El data
Isc = PP['Isc']
Isc_norm = Isc/np.amax(Isc)

Voc = PP['Voc']
Voc_n = Voc/np.amax(Voc)

EL_int_norm = EL_int_av/np.amax((EL_int_av))

#%% Plotting together
fig = plt.figure()
ax1 = fig.add_subplot(111)

modules = np.array(EL_int_av.index).astype(str)
ax1.scatter(modules, Isc_norm,label='Isc')
ax1.scatter(modules, EL_int_norm,label='Average EL')
plt.legend();
plt.ylabel('Normalized values of I and phi', fontsize=12)
#plt.xticks(np.array(EL_int_av.index).astype(str))
ax1.tick_params(direction='out',  labelsize=10, rotation=45)


#%% Plotting EL and Voc together
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(modules, Voc_n,label='Voc')
ax1.scatter(modules, EL_int_norm,label='Average EL')
plt.legend();
plt.ylabel('Normalized values of V and phi', fontsize=12)
#plt.xticks(list(EL_int_av.index))
ax1.tick_params(direction='out',  labelsize=10, rotation=45)

#%% Plotting Estimated irradiated intensity with measured EL intensity 
 
PP,PP_H,PP_L = getELPP(folder_with_data)

G_EL = PP_H['I']
G_EL = G_EL/Isc
G_EL_n = G_EL/np.amax(G_EL)
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(modules, G_EL,label='Estiamted G_EL')
ax1.scatter(modules, EL_int_norm,label='Average EL')
plt.legend();
plt.ylabel('Values of G_EL/1000 and normalized phi', fontsize=12)
#plt.xticks(list(EL_int_av.index))
ax1.tick_params(direction='out',  labelsize=10, rotation=45)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(modules, G_EL_n,label='Estiamted G_EL normalized')
ax1.scatter(modules, EL_int_norm,label='Average EL')
plt.legend();
plt.ylabel('Normalized values of G_EL and phi', fontsize=12)
#plt.xticks(list(EL_int_av.index))
ax1.tick_params(direction='out',  labelsize=10, rotation=45)



#%% Plotting Isc, G_EL and EL

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(modules, Isc_norm,label='Isc normalized')
ax1.scatter(modules, G_EL_n,label='Estiamted G_EL normalized')
ax1.scatter(modules, EL_int_norm,label='Average EL normalized')
plt.legend();
plt.ylabel('Normalized values of G_EL and phi', fontsize=12)
#plt.xticks(list(EL_int_av.index))
ax1.tick_params(direction='out',  labelsize=10, rotation=45)

#%% RMSE

#rmse=0
#rmse += [(EL_int_norm.loc(i)-G_EL_n[i])^2 for i in modules]
#i = modules[0]
#EL_int_norm.loc[i]