
# coding: utf-8

# In[6]:


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
def convertToBin(img,binLists,points):
    pix = img.load()
    for i in range(img.size[1]):
        temp = []
        for j in range(img.size[0]):
            #print(pix[i,j],end = ' ')
            if pix[j,i]>200:
                temp.append('0')
            else:
                temp.append('1')
                points.append((j,i))
        binLists.append(temp)
   # print('convertToBin finished')
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
def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]
def SlopeToArc(a,b):
    k = 0
    if (a[0] - b[0]) == 0:
        return math.pi / 2
    else:
        k = (a[1] - b[1]) / (a[0] - b[0])
    return -math.atan(k)
def drawHull(points,points2):
    plt.figure()
    plt.plot(points[0][0],points[0][1],'bo')
    plt.plot([i[0] for i in points],[i[1] for i in points],'r-')
    plt.plot([i[0] for i in points],[i[1] for i in points],'ro')
    plt.plot([i[0] for i in points2],[i[1] for i in points2],'bo')
    plt.show()
def getRotatePoint(point,origin,k):
    x = point[0] - origin[0]
    y = point[1] - origin[1]
    rX = math.cos(k) * x + math.sin(k) * y + origin[0]
    rY = math.cos(k) * y - math.sin(k) * x + origin[1]
    return (rX,rY)
def MBR(points):
#     print('x = ' + str(temp1), 'y = ' + str(temp2))
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0
    S = 1000
    topLeft = tuple()
    topRight = tuple()
    botLeft = tuple()
    botRight = tuple()
    for i in range(len(points)):
        if i != (len(points) - 1):
            k = SlopeToArc(points[i + 1],points[i])
        else:
            k = SlopeToArc(points[i],points[0])
        temp = [points[i]]
        for j in range(len(points)):
            x = points[j][0] - points[i][0]
            y = points[j][1] - points[i][1]
            temp1 = x * math.cos(k) - y * math.sin(k) + points[i][0]
            temp2 = y * math.cos(k) + x * math.sin(k) + points[i][1]
            temp.append((temp1,temp2))
        xAscend = sorted(temp,key = lambda d:d[0])
        yAscend = sorted(temp,key = lambda d:d[1])
        xMin = xAscend[0][0]
        xMax = xAscend[-1][0]
        yMin = yAscend[0][1]
        yMax = yAscend[-1][1]
        tempS = (yMax - yMin) * (xMax - xMin)
        #print(tempS)
        if tempS < S:
            S = tempS
            topLeft = getRotatePoint((xMin,yMax),points[i],k)
            topRight = getRotatePoint((xMax,yMax),points[i],k)
            botLeft = getRotatePoint((xMin,yMin),points[i],k)
            botRight = getRotatePoint((xMax,yMin),points[i],k)
#         plt.figure()
    # plt.plot([i[0] for i in points],[i[1] for i in points],'b-')
    # plt.plot(topLeft[0],topLeft[1],'go')
    # plt.plot(topRight[0],topRight[1],'go')
    # plt.plot(botLeft[0],botLeft[1],'go')
    # plt.plot(botRight[0],botRight[1],'go')
    sortList = [topLeft,topRight,botLeft,botRight]
    xAscend = sorted(points,key = lambda d:d[0])
    yAscend = sorted(points,key = lambda d:d[1])
    # plt.plot([i[0] for i in sortList],[i[1] for i in sortList],'g-')
    # plt.show()
    sortList = [xAscend[0][0],xAscend[-1][0],yAscend[0][1],yAscend[-1][1]]

    return sortList

#     if sortList[0][0] == sortList[1][0]:
#         return 0
#     return math.pi / 4 - math.atan((sortList[1][1] - sortList[0][1]) / (sortList[1][0] - sortList[0][0]))
def transImg(im):
    #im = Image.open(path)
    # im2 = im.convert('RGBA')
    binaryL = []
    points = []
    convertToBin(im,binaryL,points)
    solution = convex_hull(points)
#     print(solution)
    arc = MBR(solution)
    binNp = np.array(binaryL)
    xMin = int(arc[0])
    xMax = int(arc[1] + 1)
    yMin = int(arc[2])
    yMax = int(arc[3]+1)
    #print(str(xMin)+ " ",str(xMax)+" ",str(yMin),' '+str(yMax))
    #print(str(im.size[0]),str(im.size[1]))
    im = im.crop((xMin,yMin,xMax,yMax))
    im = im.resize((20,20))
    return im
#     angel = 180 * arc / math.pi
#     print('the arc is ' + str(arc))
#     print('Start rotate, the angel of rotate is ' + str(angel))
#     rot = im2.rotate(angel,expand = 1)
#     fff = Image.new('RGBA', rot.size, (255,)*4)
#     out = Image.composite(rot, fff, rot)
#     out = out.convert(im.mode)
#     im.close()
#     im2.close()
#     print('transfer finished')
#     return out
        #plt.plot([i[0] for i in solution],[i[1] for i in solution],'b')
#         plt.show()
#         wid = getWidth(binaryL,out)
#         if wid < minVal:
#             minImg = out
#             minVal = wid
#     minImg.save('transed/'+path + '.png')

   # minImg.close()
# main function
def imgToBinList(im):
    img = transImg(im)
    pix = img.load()
    binLists = []
    for i in range(img.size[1]):
        temp = []
        for j in range(img.size[0]):#binary transfer
            if pix[j,i]>200:
                temp.append('0')
            else:
                temp.append('1')
        binLists.append(temp)
    return np.array(binLists)
    #print('convertToBin finished')
if __name__ == '__main__':
    path = 'image_codeSharpedsub3'
    test = imgToBinList(path)
    print(test)


# In[ ]:





# In[ ]:




