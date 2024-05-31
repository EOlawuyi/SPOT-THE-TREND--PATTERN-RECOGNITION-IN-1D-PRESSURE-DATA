from PIL import Image as im
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import numpy as np
import imageio.v3 as iio
import ipympl
import matplotlib.pyplot as plt
import skimage as ski
import skimage.feature
import pandas as pd
import scipy.stats as stats
from scipy.stats import entropy
from skimage import feature, measure
from skimage.measure import label, regionprops, regionprops_table
import pyarrow.parquet as pa
import string
from openpyxl import load_workbook
from openpyxl import Workbook
import openpyxl
import csv
import cv2
import json

#This is the code that belongs to Olorogun Engineer Enoch O. Ejofodomi in his Collaboration with Shell Onward.
#This code also belongs to Engineer Francis Olawuyi in his collaboration with Shell Onward.
#The code also belongs to the following people
#1. GODSWILL OFUALAGBA C.E.O. SWILLAS ENERGY LIMITED.
#2. DR. MICHAEL OLAWUYI
#3. DR. DAMILOLA SUNDAY OLAWUYI
#4. ENGINEER DEBORAH OLAWUYI
#5. ENGINEER JOSHUA OLAWUYI
#6. ENGINEER JOSEPH OLAWUYI
#7. ENGINEER ONOME EJOFODOMI
#8. ENGINEER EFEJERA EJOFODOMI
#9. ENGINEER FRANCIS OLAWUYI
#10. DR. MATTHEW OLAWUYI
#11. ENGINEER ENOCH O. EJOFODOMI
#12. OCHAMUKE EJOFODOMI
#13. ENGINEER ONOME OMIYI
#14. MS. KOME ODU
#15. MR. KAYODE ADEDIPE
#16. MR. OMAFUME EJOFODOMI
#17. MR. NICHOLAS MONYENYE
#18. ENGINEER AYO ADEGITE
#19. ENGINEER ESOSA EHANIRE
#20. Ms. NANAYE INOKOBA
#21. Ms. YINKA OLAREWAJU-ALO
#22. Ms. ERKINAY ABLIZ
#23. Ms. FAEZEH RAZOUYAN
#24. MRS. TEVUKE EJOFODOMI
#25. MR.ONORIODE AGGREH
#26. MS. NDIDI IKEMEFUNA
#27. MS. ENAJITE AGGREH
#28. DR. ESTHER OLAWUYI
#29  MS. ISI OMIYI
#30. DR. JASON ZARA
#31. DR. VESNA ZDERIC
#32. DR. AHMED JENDOUBI
#33. DR. MOHAMMED CHOUIKHA
#34. MS. SHANI ROSS

# MAY 31, 2024.

mainwindow = tk.Tk()
mainwindow.geometry("1400x700")

#Load 362 Images
Imagefile = ["bzjeg.csv", "cuetl.csv",  "edvhp.csv", "apgjp.csv",
             "ceeng.csv", "dgqzb.csv", "frlos.csv", "bafgr.csv",
             "cnvsw.csv", "dkiqe.csv", "oylrn.csv", ]


print(Imagefile)       

#Array to Hold String Variable for file
StringFile = "{"

for l in range(0,11):
   #Read in test CSV file
   datacsv = pd.read_csv(Imagefile[l])
            
   #Geg Shape of Data in File
   datacsv.shape

   #Print Data
   print(datacsv)
   
   #Get Shape of CSV Data
   [a,b] =  datacsv.shape
   datacsv.values[0,0]

   #Extract Pressure Data from File
   #string = "freeCodeCamp"
   #print(string[0:5])

   #Variables
   count = 0
   counta = ""
   countb = ""
   finalcount = ""
   numvar = np.zeros((a,1))
   assigneddatalength = a - 100
   pdata = datacsv.values[:,0]
   slength = len(pdata)
   print(pdata)

   #Get Pressure Data 
   #for j in range(0,a):
   for j in range(0,assigneddatalength):
      count = 0
      counta = str(pdata[j])
      sublength = len(counta)
      for k in range(0, sublength):
         if(counta[k:k+1] == '\t'):
            count = count + 1
            if (count == 2):
               countb = counta[k+1:sublength]
               if(countb != ''):
                  numvar[j] = float(countb)

                  
   #Pressure Data Algorithm
   #Variables
   value1 = numvar[0]
   value2 = numvar[1]

   addcount = 0
   minuscount = 0
   function1 = np.zeros((1576700,1))
   function2 = np.zeros((1576700,1))
   #Variables to store the start value of each flowing or producing cycle
   startproducing = np.zeros((100,1))
   startproducinga = 0
   endproducing = np.zeros((100,1))
   endproducinga = 0
   startshutin = np.zeros((100,1))
   startshutina = 0
   endshutin = np.zeros((100,1))
   endshutina = 0
   jcountplus = 0
   jcountminus = 0
           
   for j in range(2,1576700):
      if((value2-value1) > 0):
         #Zero out the negative count because you are starting to deal with Positive Pressures
         jcountplus = j
         minuscount = 0
         #Pressure Data in the Well is increasing
         addcount = addcount+1
         if(addcount == 3000):
            #if the increase has run the course for 50 values
            #identify it as a Start Location for a Producing Well
            # and store the Variable value for it.
            startproducinga = startproducinga + 1
            startproducing[startproducinga] = j
            print("J value Plus:")
            print(j)
         if(addcount > 3000):
            #Store the End Value of the Producing Well until it stops,
            # thereby getting the last accurate point.
            endproducing[startproducinga] = j


      if((value2-value1) < 0):
         #Zero out the positive count because you are starting to deal with Negative Pressures
         addcount = 0
         jcountminus = j
         #Pressure Data in the Well is decreasing
         minuscount = minuscount+1 
         if(minuscount == 3000):
            #if the decrease has run the course for 50 values
            #identify it as a Start Location for a Shutin Well
            # and store the Variable value for it.
            startshutina = startshutina + 1
            startshutin[startshutina]= j
            print("J value Minus:")
            print(j)

         if(minuscount > 3000):
            #Store the End Value of the Shutin Well until it stops,
            # thereby getting the last accurate point.
            endshutin[startshutina] = j


      value1 = value2
      value2 = numvar[j]
    
   print("Addcount")
   print(addcount)
   print("Minuscount")
   print(minuscount)
   print("StartProducing :")
   print(startproducing)
   print("EndProducing:")
   print(endproducing)
   print("StartShutin :")
   print(startshutin)
   print("EndShutin:")
   print(endshutin)


   # Remove 3000 from the Start Producing  and Start Shutin Values such
   # to get the correct Start Positions for Positve and Negative Pressures
   countproducing1 = 0
   countstartin1 = 0
   for k in range(0,39):
      if(startproducing[k] != 0):
         startproducing[k] = startproducing[k] - 3000
         countproducing1 = countproducing1 + 1
      if(startshutin[k] != 0):
         startshutin[k] = startshutin[k] - 3000
         countstartin1 = countstartin1 + 1


   print("SECOND LAYER")
   print("StartProducing :")
   print(startproducing)
   print("EndProducing:")
   print(endproducing)
   print("StartShutin :")
   print(startshutin)
   print("EndShutin:")
   print(endshutin)

   print(countproducing1)
   print(countstartin1)

   StringFile = StringFile + "'" + "test_labels/" + Imagefile[l] + "': ["
   for k in range(1,countproducing1+1):
      StringFile = StringFile + str(startproducing[k]) + "," + str(endproducing[k]) + ", "
      
   for k in range(1,countstartin1+1):
      StringFile = StringFile + str(startshutin[k]) + "," + str(endshutin[k]) + ", "
    
   StringFile = StringFile + "], "


# Remember to remove 3000 from the Start Producing  and Start Shutin Values such
# as the following:
# startproducing = startproducing-3000
# startshutin = startshutin-3000


   #countb = counta[6:sublength]
   #print(counta)
   #print(countb)
   #numvar[j] = float(countb)
   #print("final numvar")
   #print(numvar)

   #print("Completed")



# SAMPLE SUBMISSION
#{'test_labels/bzjeg.csv': [[17169, 26422], [109319, 109370], [211460, 211501], [321419, 333529], [423736, 434317], [527942, 538429],
#[1, 2000], [3000, 5000], [6000, 8000], [9000, 11000], [12000, 14000], [15000, 16000], [16100, 16500], [1510000, 1530000],
#[1540000, 1590000]], 'test_labels/cuetl.csv': [[1, 2000], [3000, 5000], [6000, 8000], [9000, 11000], [12000, 14000], [16000, 18000],
#[19000, 21000], [23000, 29000], [32000, 37000], [38000, 39000], [404859, 404978], [471368, 471460], [537876, 538010], [604362, 604423],
#[670880, 671032], [737335, 737551], [803858, 803902], [862250, 862351], [1540000, 1550000], [1555000, 1560000]],
#'test_labels/edvhp.csv': [[100, 500], [800, 900], [1100, 3000], [3200, 6000], [7000, 11000], [53556, 104893], [134925, 197511], [239938, 282281], [373975, 432351], [452588, 494652], [564908, 594802], [1560000, 1562000], [1563000, 1565000], [1570000, 1572000], [1573000, 1574000]], 'test_labels/apgjp.csv': [[1000, 2000], [3000, 5000], [6000, 8000], [11000, 20000], [21000, 29000], [30000, 33000], [37000, 43000], [838957, 896943], [1010188, 1044815], [1121129, 1121330], [1311813, 1364753], [1489639, 1528663]], 'test_labels/ceeng.csv': [[100, 500], [600, 800], [850, 900], [1100, 1500], [2000, 2500], [3000, 3500], [3600, 3900], [4000, 4100], [475535, 475619], [534419, 534583], [593407, 593436], [652293, 652416], [711175, 711353], [770129, 770239], [829002, 829066], [887928, 888069], [901592, 901739], [1510000, 1520000], [1530000, 1540000], [1545000, 1550000], [1555000, 1560000], [1565000, 1568000], [1568100, 1569200]], 'test_labels/dgqzb.csv': [[100, 500], [600, 800], [1100, 1200], [2100, 2500], [3000, 3500], [4100, 5400], [6100, 7500], [1133651, 1142696], [1231962, 1242156], [1341943, 1352299], [1445286, 1455709], [1548331, 1557553]], 'test_labels/frlos.csv': [[1000, 2000], [3000, 7000], [10000, 20000], [21000, 22000], [31000, 35000], [1202823, 1233114], [1276071, 1296932], [1346695, 1363925], [1433847, 1456422], [1499841, 1524398]], 'test_labels/bafgr.csv': [[10000, 20000], [21000, 25000], [38423, 67012], [1250607, 1277466], [1317316, 1346067], [1392547, 1414300], [1468221, 1501534]], 'test_labels/cnvsw.csv': [[1000, 10000], [11000, 19000], [21067, 29024], [113505, 122362], [202292, 212057], [294745, 305376]], 'test_labels/dkiqe.csv': [[30869, 58273], [93265, 123408], [1541131, 1563685], [1565000, 1568999]], 'test_labels/oylrn.csv': [[1000, 12600], [14000, 19000], [48423, 88805], [153289, 196222], [1261902, 1262065], [1457350, 1494841]]}


print("Numvar:")
print(numvar)     

   
StringFile = StringFile + "}"

print("String File: ")
print(StringFile)     
   
