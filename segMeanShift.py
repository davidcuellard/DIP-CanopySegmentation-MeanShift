"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 2: Segmentación Meanshift

@author: David Felipe Cuellar Diaz
"""

#https://github.com/log0/build-your-own-meanshift/blob/master/Meanshift%20Image%20Segmentation.ipynb

import cv2
import numpy as np
from sklearn.cluster import MeanShift

class segmentacion:

    def __init__(self,image="image.jpg",folder="",minc=2,maxc=2,scalefactor=1,resize=False):        
        self.image=image
        self.folder=folder
        self.minc=minc
        self.maxc=maxc
        self.scalefactor=scalefactor
        self.resize=resize
    
    def meanShift(self):
        
        	# carga la imagen
        imagein = cv2.imread(self.image)

        # cambia el tamaño de la imagen si es necesario
        if self.resize == True:
            height, width = imagein.shape[:2]
            imagein = cv2.resize(imagein,(int(self.scalefactor*width), int(self.scalefactor*height)), interpolation = cv2.INTER_NEAREST)
        
        # crea una copia de la imagen
        imagecopy=imagein.copy()
        
        # convierte la imagen en un arreglo
        imagein = np.array(imagein)
        
        # Convierte la imagen a tres capas
        X = np.reshape(imagein, [-1, 3])
        
        #Ancho de banda
        bandwidth=self.minc
        
        while bandwidth <= self.maxc:

            print(bandwidth)
            
            # realiza meanshift con el ancho de banda indicado
            ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=1)
            ms.fit(X)
        
            labels = ms.labels_
	       
            cluster_centers = ms.cluster_centers_
            # convierte cada centro de cluster a una imagen de 3 canales con 8 bits
            cluster_centers= cluster_centers.astype(np.uint8)
            labels_unique = np.unique(labels)
            n_clusters_ = len(labels_unique)

            # imprime el número de clusters
            print("Clusters : %d" % n_clusters_)        

            # Combina cada cluster con el label de cada píxel
            result= cluster_centers [labels.flatten()]
            img_meanshift=result.reshape((imagein.shape))  

            cv2.imwrite(self.folder + "imagecopy.bmp",imagecopy) 
            cv2.imwrite(self.folder + str(bandwidth) + "/output" + str(bandwidth) + "_" + str(n_clusters_) + ".bmp",img_meanshift)
 
            # Convierte el resultado kmeans en escala de grises
            gray= cv2.cvtColor(img_meanshift, cv2.COLOR_BGR2GRAY)
         
            # aplica umbralización threshold para crear la máscara
            ret,mask = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            resultmask = cv2.bitwise_and(imagein, imagein, mask=mask)

            # Guarda las imágenes
            cv2.imwrite(self.folder + str(bandwidth) + "/mask.bmp",mask)
            cv2.imwrite(self.folder + str(bandwidth) + "/result.bmp",resultmask)

            # Invierte la máscara y se la aplica a la imagen de entrada
            ret2,mask2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            resultmask2 = cv2.bitwise_and(imagein, imagein, mask=mask2)
            
            # Guarda las imagenes
            cv2.imwrite(self.folder + str(bandwidth) + "/mask2.bmp",mask2)
            cv2.imwrite(self.folder + str(bandwidth) + "/result2.bmp",resultmask2)

            # duplica el ancho de banda para una siguiente iteración		
            bandwidth=bandwidth*2
            
        cv2.destroyAllWindows()