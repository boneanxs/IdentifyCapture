
# coding: utf-8

# In[3]:


from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
import os
def toBinList(im):
    pix = im.load()
    binLists = []
    for i in range(im.size[1]):
        temp = []
        for j in range(im.size[0]):
            #print(pix[i,j],end = ' ')
            if pix[j,i]>200:
                temp.append('0')
            else:
                temp.append('1')
        binLists.append(temp)
    return binLists
def cropImg(im):
    imgry = im.convert('L')#图像加强，二值化
    sharpness =ImageEnhance.Contrast(imgry)#对比度增强
    im = sharpness.enhance(2.0)
    binLists = toBinList(im)
    verVs = []
    for x in range(im.size[0]):
        lens = 0
        for y in range(im.size[1]):
            temp = binLists[y]
            if temp[x] == '1':
                lens += 1
        verVs.append(lens)
    cutList = []
    turn = 0
    begin = 0
    for i in range(len(verVs) - 1):
        item = verVs[i]
        if (item != 0) & (turn == 0):
            turn = 1
            begin = i
            cutList.append(begin)
            continue
        if (item == 0) & (turn == 1):
            turn = 0
    #         maxV = 100
    #         cutList.append(curCut)
            cutList.append(i)
            continue
        if item == 0:
            continue
    meanVal = 0
    total = 0
    if len(cutList) == 7:
        cutList.append(im.size[0])
    try:
        for i in range(0,len(cutList),2):
            total += cutList[i+1] - cutList[i]
    except Exception as error:
        return 0
    meanVal = total / 4
    maxV = 100
    curCut = 0
    #判断是否是有粘连
    for i in range(0,len(cutList),2):
        if cutList[i+1] - cutList[i] - 3 * meanVal >= -7:
            #print("The Fuck, we can't crack captureVal")
            continue
        if cutList[i+1] - cutList[i] - 2 * meanVal >= -7:
            tempMean = (cutList[i+1] - cutList[i]) / 2
            begin = cutList[i]
            for i in range(cutList[i],cutList[i+1]):
                item = verVs[i]
                if item == 0:
                    continue
                if (item <= verVs[i-1]) & (item <= verVs[i+1]):
                    if abs(i-begin - tempMean) < maxV:
                        maxV = abs(i-begin - tempMean)
                        curCut = i
            cutList.append(curCut)
            cutList.append(curCut)
            maxV = 1000
    #裁切图片
    cutList.sort()
    if len(cutList) < 8:
        return 0
    index = 1
    afterCut = list()
    for i in range(0,len(cutList),2):
        temp = im.crop((cutList[i],0,cutList[i+1],im.size[1]))
        afterCut.append(temp)
    return afterCut
if __name__ == '__main__':
    txtFiles = [x.replace('.png','') for x in os.listdir() if x.endswith('.png')]
    for item in txtFiles:
        print(item)
        cropImg(item)
    print('succeed')


# In[ ]:




