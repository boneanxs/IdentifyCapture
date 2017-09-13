
# coding: utf-8

# In[7]:


from PIL import Image
import numpy as np
import os
import SeperateImage
import RotateImage
import ImgToList
from sklearn.externals import joblib

def identify(img):
    cpl = joblib.load('prediction.pkl')
    binLists = SeperateImage.toBinList(img)
    cutLists = SeperateImage.cropImg(img)
    predicted = []
    # print(cutLists)
    if cutLists != 0:
        for item in cutLists:
            item = RotateImage.transImg(item)
            binList = ImgToList.imgToBinList(item)
            nx, ny = binList.shape
            nsamples = 1
            shapedList = binList.reshape((nsamples,nx*ny))
            predicted.append(''.join(cpl.predict(shapedList)))
        return ''.join(predicted)
    else:
        return 'error'
if __name__ == '__main__':
    pngList = [i for i in os.listdir() if i.endswith('.png')]
    for item in pngList:
        img = Image.open(item)
        name = identify(img)
        os.rename(item,name + '.png')
    print('finished')


# In[ ]:




