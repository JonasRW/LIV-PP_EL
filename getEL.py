# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:35:04 2020

@author: Jonas Rydtun Winsvold

This script imports EL data from an .xlsx file. The script is based on data
extracted from the softeware dataArtist.
Prerequisites for this code is:
    - The average cell intensities of modules estimated in dataArtist are 
    copied to sparate sheets in the .xlsx file. 
    - The moduleID is placed in 
    cell [0,0] of eatch sheet. 
"""

import pandas as pd
import numpy as np
import xlrd




#%%---Function to import the EL data and generating an module average. 


def getEL(file_path):
    wb = xlrd.open_workbook(file_path)
    
    #Cells imported clockwise
    #ModuleIDs = [str(int(wb.sheet_by_name(sheet).cell_value(0,0))) for sheet in  wb.sheet_names()]
    #ModuleIDs = np.unique(np.array(ModuleIDs))  # finding unique entries with unique to arrange in increasing order.
    EL_intensities_xl = np.array([[int(wb.sheet_by_name(sheet).cell_value(0,0))\
                                       ,float(wb.sheet_by_name(sheet).cell_value(1,0))\
                          ,float(wb.sheet_by_name(sheet).cell_value(1,1))\
                              ,float(wb.sheet_by_name(sheet).cell_value(2,1))\
                                  ,float(wb.sheet_by_name(sheet).cell_value(2,0))] for sheet in  wb.sheet_names()])
    ModuleIDs = EL_intensities_xl[:,0].astype(int)
    EL_int_data = pd.DataFrame(EL_intensities_xl[:,1:],columns=['Cell NW','Cell NE','Cell SE','Cell SW'],index=ModuleIDs)

    EL_int_av = pd.DataFrame([np.average(EL_int_data.loc[module]) for module in ModuleIDs],index=ModuleIDs)
    return EL_int_data, EL_int_av

if __name__ == "__main__":
    file_path_EL = 'C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas\\6018xx-191015-test-tif\\6018xx-191015_Iav.xlsx'
    EL_int_data,EL_int_av = getEL(file_path_EL)