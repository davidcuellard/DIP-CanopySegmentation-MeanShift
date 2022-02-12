"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 2: Metodos de segmentación - TEST

@author: David Felipe Cuellar Diaz
"""

import os
import segMeanShift

directory = os.getcwd()

folderin = directory + "/"

tipo=["GRE","NIR","RGB"]

form=[".TIF",".JPG"]

imagein=["","IMG_170805_165709_0138_"]
	
image= folderin + imagein[1] + tipo[2] + form[1]
folder = folderin + "/results/"

skm=segMeanShift.segmentacion(image=image,folder=folder,minc=2,maxc=2,scalefactor=1/2,resize=True)

skm.meanShift()


