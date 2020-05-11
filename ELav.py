# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 09:15:26 2020

Otsu binarization as roi mask for averaging. 

@author: Jonas R. Winsvold
"""
import cv2
import skimage.io as io
import numpy as np
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
# def ELavOtsu(img_PATH):
#     img = io.imread(img_PATH)
#    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     th,roi = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #io.imshow(roi)
#     roi = cv2.multiply(roi,(1/255)) #(roi*(1/255)).astype(int)
#     img_ROI = cv2.multiply(img,roi)
#    # io.imshow(img_ROI)
#   #  np.amax(img_ROI)
#  #   np.amax(img)
# #    np.amax(roi)
#     ELav = np.average(img_ROI[np.nonzero(img_ROI)])
#   #  img_ROI=img_ROI.astype(float)
#  #   img_ROI[img==0] = int(np.nan)
# #    ELav = np.nanmean(img_ROI|)
#     return th,ELav

def ELavOtsu(calibration_img_PATH):
    img = io.imread(calibration_img_PATH)
    #img = rgb2gray(img)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Backgound exl.
    th,roi = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #n_th = th/255
    
    #roi = cv2.multiply(roi,(1/255)) #(roi*(1/255)).astype(int)
    # plt.figure()
    # io.imshow(roi)
    # plt.title('Cal ROI')
    #img_ROI = cv2.multiply(img,roi)
    #io.imshow(img_ROI)
    bin_roi = cv2.multiply(roi,(1/255)) #(roi*(1/255)).astype(int)
    #io.imshow(roi)
    img_ROI = cv2.multiply(img,bin_roi)   
    
    th2,roi2 = cv2.threshold(img_ROI[img_ROI!=0],th,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return th,roi

def getELav(folder_with_data,calibration_img_PATH):
    
    files = os.listdir(folder_with_data)

    moduleIDs = [file.split('_')[0] for file in files]
    # moduleIDs = np.unique(np.array(moduleIDs))  # finding unique entries, SE12897374
    # ELavs = pd.DataFrame([ELavOtsu(folder_with_data + file) for file in files],index=moduleIDs)
   
    th,roi = ELavOtsu(calibration_img_PATH)
    n_roi = cv2.multiply(roi,(1/255)).astype(float) #(roi*(1/255)).astype(int)
    # plt.figure()
    # io.imshow(roi)
    n_roi[n_roi == 0] = np.nan
    #io.imshow(roi)

    ELav = {}
    for moduleID in moduleIDs:
        #pick out all filenames 
        files_matching_moduleID = [filename for filename in files if moduleID in filename]
        I_EL = pd.DataFrame()
        img_av= []
        I = []
        for file in files_matching_moduleID:
                img = io.imread(folder_with_data + file)
                img_ROI = cv2.multiply(img.astype(float),n_roi)
                # img_ROI = np.ma.array(img_ROI,mask=np.nan)
                img_ROI = np.ma.masked_invalid(img_ROI)
                plt.figure()
                io.imshow(img_ROI)
                plt.title(file)
                exp = re.search('200506_(.*)_',file).group(1)
                av = (np.average(img_ROI))/(float(exp))
                img_av.append(av)
                I.append(float(re.search('_'+exp+'_(.*).xIbg',file).group(1).replace(',','.')))
        I_EL['I'] = I
        I_EL['ELav'] = img_av
        ELav[moduleID] = I_EL
        
    #         for file in os.chdir(folder_with_data):
    #     module = file.split('IxIbg_Output\\')[1].split('-')[0]
    return ELav
    
if __name__ == "__main__":
    # img_PATH = "C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas\\6018xx-191015-test-tif\\601861-191015_191015_1_9,00000_xIbg.tiff" #I_Input\\9\\601861-191015_191015_1_9,000000.tiff" 
    # folder_with_data = "C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\Til Jonas\\6018xx-191015-test-tif\\IxIbg_Output_0,9\\" #I_Input\\9\\"

    folder_with_data = "C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\2020.05.06\\xIbg\\" #
    calibration_img_PATH = "C:\\Users\\io318\\OneDrive - Norwegian University of Life Sciences\\skole\\Master IFE BIPV\\EL-bilder\\2020.05.06\\xIbg\\601871_200506_1_9,0.xIbg.tiff" #
    
    ELavs = getELav(folder_with_data,calibration_img_PATH)

    # n = '601871_200506_1_9,0.xIbg.tiff'
    # e = re.search('200506_(.*)_',n).group(1)
    # i = float(re.search('_'+e+'_(.*).xIbg',n).group(1).replace(',','.'))
