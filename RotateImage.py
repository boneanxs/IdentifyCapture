
# coding: utf-8

# In[1]:


import os
# import transfer
from PIL import Image

def convertToBin(img,binLists):
    pix = img.load()
    for i in range(img.size[1]):
        temp = []
        for j in range(img.size[0]):
            #print(pix[i,j],end = ' ')
            if pix[j,i]>200:
                temp.append('0')
            else:
                temp.append('1')
        binLists.append(temp)
def getWidth(binLists,img):
    verVs = []
    for x in range(img.size[0]):
        lens = 0
        for y in range(img.size[1]):
            temp = binLists[y]
            if temp[x] == '1':
                lens += 1
        verVs.append(lens)
    begin = 0
    end = 0
    turn = 0
    for i in range(len(verVs)):
        item = verVs[i]
        if (item != 0) & (turn == 0):
            turn = 1
            begin = i
            continue
        if (item == 0) & (turn == 1):
            end = i
            turn = 0
    if end == 0:
        end = len(verVs)
    return end - begin
def transImg(im):
    #im = Image.open(path + '.png')
    im2 = im.convert('RGBA')
    minVal = 1000
    minImg = 0
    #print('Start rotate')
    for i in range(-45,45):
        binaryL = []
        rot = im2.rotate(i,expand = 1)
        fff = Image.new('RGBA', rot.size, (255,)*4)
        out = Image.composite(rot, fff, rot)
        out = out.convert(im.mode)
        convertToBin(out,binaryL)
        wid = getWidth(binaryL,out)
        if wid < minVal:
            minImg = out
            minVal = wid
    im.close()
    im2.close()
    return minImg
if __name__ == '__main__':
    pngList = [x.replace('.png','') for x in os.listdir() if x.endswith('.png')]
    for path in pngList:
        print('start file:' + path)
        transImg(path) 
    #     img.save('transed/' + path + '.png')
    print('succeed!')


# In[ ]:




