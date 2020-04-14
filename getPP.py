# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:17:18 2020

@author: Jonas R. Winsvold

This script is a modified version of the script "lightIV-analysis" by Gaute
Otnes. It mainly imports light-IV data from the Spire Solar Simulator and
stores the Isc and Voc parameters.

Prerequisites for the script to work are
    -that you have all the data you want to look at in the same folder, input
     this folder-path into "folder_with_data"
    -that the files you have there are csv-files, exported from the Spire
     software by "Save file as" and choosing csv. Preferably, only csv-files 
     that you want to look at should be present in the folder. If you take
     files from the folder where Spire saves files automatically, they will be
     .ivc. In this case, the only thing that needs to be changed is the "*.csv"
     to "*.ivc" where the files are found by glob.glob
    -that the files have filenames including unique identifiers for the
     different modules, e.g. a serial number. What comes directly before and
     after this serial number in the file name should be entered into the first
     and second ".split()" parentheses where the "moduleIDs" parameter
     is defined (fifth line after the "Import and organize data" header). If 
     there is nothing before the identifier in the file-name, enter the last
     part of the folder-path. See example below.
     
"""

import os
import pandas as pd
import glob
import numpy as np


#%%------------Function for importing the light_IV data
def getLIVdata(folder_with_data):

    os.chdir(folder_with_data)
    
    # --------------------------IMPORT AND ORGANIZE DATA------------------------
    lightIV_data = {}
    lightIV_parameters = {}
    
    files = glob.glob(os.getcwd() + '\\*.csv') # get all 
    moduleIDs = [file.split('Til Jonas\\')[1].split('-')[0] for file in files]
    moduleIDs = np.unique(np.array(moduleIDs))  # finding unique entries with unique to arrange in increasing order.
    
    for moduleID in moduleIDs:
        lightIV_data[moduleID] = {}
        lightIV_parameters[moduleID] = {}
        
        #pick out all filenames 
        files_matching_moduleID = [filename for filename in files if moduleID in filename]
        for file in files_matching_moduleID:
            
            # pick out irradiance
            IV_irradiance = pd.read_csv(file, skiprows=9, nrows=1)
            IV_irradiance = int(float(IV_irradiance.columns[1]))*10  # converting from mW/cm^2 to W/m^2
    
            
            #import IV-data into a temporary dataframe, and clean it up a bit
            temporary_df = pd.read_csv(file, skiprows=81)
            temporary_df.columns = [col.replace(" ", "") for col in temporary_df.columns] #removing whitespace, SE8270092
            temporary_df.columns = [col.replace(":", "") for col in temporary_df.columns] #removing colons
            IV_end_index = temporary_df.loc[temporary_df['Voltage'] == ' Ref Cell:    '].index[0]
            temporary_df = temporary_df[:IV_end_index].astype(float)  # remove everything but the IV-curve
            
            # assign IV-data to dictionary
            lightIV_data[moduleID][IV_irradiance] = temporary_df.copy()
    
            # import performance-parameters determined by the SolarSimulator-software
            temporary_df = pd.read_csv(file, skiprows=14, nrows=9).transpose()  # overwriting the temporary dataframe from above
            lightIV_parameters[moduleID][IV_irradiance] = dict(zip(temporary_df.iloc[0], temporary_df.iloc[1]))
    
        lightIV_parameters[moduleID] = pd.DataFrame(lightIV_parameters[moduleID]).transpose()
        lightIV_parameters[moduleID].columns = [col.replace(" ", "") for col in lightIV_parameters[moduleID].columns]  #removing whitespace, SE8270092
        lightIV_parameters[moduleID].columns = [col.replace(":", "") for col in lightIV_parameters[moduleID].columns]  #removing colons
        
    return moduleIDs,lightIV_data, lightIV_parameters



#%% -------------- Function for exctracting Isc and Voc

def getPP(IRRADIANCE,folder_with_data):
    
    moduleIDs, lightIV_data, lightIV_parameters = getLIVdata(folder_with_data)
   
    performance_parameter = ['Voc','Isc']

    parameter_values = [[lightIV_parameters[moduleID].loc[IRRADIANCE][performance_parameter[0]]\
                        ,lightIV_parameters[moduleID].loc[IRRADIANCE][performance_parameter[1]]] for moduleID in moduleIDs]
    parameter_values = pd.DataFrame(parameter_values,columns=performance_parameter,index=moduleIDs)
    return parameter_values

def getELPP(folder_with_data):
    os.chdir(folder_with_data)
    feedback_PP = {}
    #file ={}
    files = glob.glob(os.getcwd() + '\\*.txt') # get all 
    
    for filename in files:
        file = pd.read_csv(filename,delim_whitespace=True\
                                      ,skiprows=8,nrows=2,header=None,decimal=',')
        moduleIDs = filename.split('Til Jonas\\')[1].split('-')[0]
        feedback_PP[moduleIDs] = file[[3,4]].rename(columns={3:'I',4:'V'})
    moduleIDs = [file.split('Til Jonas\\')[1].split('-')[0] for file in files]
    moduleIDs = np.unique(np.array(moduleIDs))
    param = ['I','V']
    feedback_PP_high = [[feedback_PP[moduleID].loc[0][param[0]]\
                         ,feedback_PP[moduleID].loc[0][param[1]]] for moduleID in moduleIDs]
    feedback_PP_low = [[feedback_PP[moduleID].loc[1][param[0]]\
                     ,feedback_PP[moduleID].loc[1][param[1]]] for moduleID in moduleIDs]

    feedback_PP_high = pd.DataFrame(feedback_PP_high,columns=param,index=moduleIDs)
    feedback_PP_low = pd.DataFrame(feedback_PP_low,columns=param,index=moduleIDs)
    
    return feedback_PP,feedback_PP_high,feedback_PP_low
        
if __name__ == '__main__':
    folder_with_data = ('C:\\Users\\jonas\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas')
    moduleIDs,lightIV_data, lightIV_parameters = getLIVdata(folder_with_data)
    parameter_values = getPP(1000,folder_with_data)
    v,h,l = getELPP(folder_with_data)
    hi = h['I'].transpose()
    G = h['I']/parameter_values['Isc']
