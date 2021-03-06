'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/6/24 8:48
@Software: PyCharm
@File    : 624.py
'''
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def dis(title,num,files):
    cv.namedWindow(title, 0)
    cv.resizeWindow(title, num * H, W)
    cv.imshow(title, np.hstack(files))
    cv.waitKey(0)
    cv.destroyAllWindows()

def display(num,files):
    for i in range(num):
        plt.figure("hist")
        arr = files[i].flatten()
        plt.subplot(1,2,i+1)
        n, bins, patches = plt.hist(arr, bins=256, density=1,edgecolor='None',
                                    facecolor='red')
    plt.show()

def displays(r,c,titles,files):
    for i in range(len(files)):
        plt.subplot(r,c,i+1)
        plt.imshow(files[i], cmap='gray')
        plt.xticks([]), plt.yticks([])
        plt.title(titles[i])
    plt.show()

def grey(img):
    # 获取当前图片的信息
    imgInfo = img.shape
    heigh = imgInfo[0]
    width = imgInfo[1]
    # dst 一般是新建值，目标图片
    dst = np.zeros((heigh, width), np.uint8)
    for i in range(0, heigh):
        for j in range(0, width):
            gray = 0.114 * img[i, j, 0] + 0.587 * img[i, j, 1] + 0.299 * img[i, j, 2]
            dst[i, j] = np.uint8(gray)
    return dst

#灰度上移
def huidushangyi(img1):
    img2 = np.zeros((H,W),np.uint8)
    for i in range(H):
        for j in range(W):
            if int(img1[i,j]+50)>255:
                gray = 255
            else:
                gray = int(img1[i,j]+50)
            img2[i,j]=gray
    flies = [img1,img2]
    dis("huidushangyi",2,files=flies)

#灰度对比度
def huiduduibidu(img1):
    img3 = np.zeros((H,W),np.uint8)
    for i in range(H):
        for j in range(W):
            if img1[i,j] > 160:
                gray = img1[i,j]*1.2
                if gray > 255:
                    gray = 255
            elif img1[i,j] < 127:
                gray = img1[i,j]*0.5
            else:
                gray = img1[i,j]
            img3[i,j]=gray
    flies = [img1,img3]
    dis("huiduduibidu",2,files=flies)

#灰度反转
def huidufanzhuan(img1):
    img4 = np.zeros((H,W),np.uint8)
    for i in range(H):
        for j in range(W):
            gray = 255 - img1[i,j]
            img4[i,j]=gray
    flies = [img1,img4]
    dis("huidufanzhuan",2,files=flies)
    return img4

#伽马
def gama(img1):
    img5 = np.zeros((H,W),np.uint8)
    for i in range(H):
        for j in range(W):
            gray = 3 * pow(img1[i,j],0.8)
            img5[i,j]=gray
    flies = [img1,img5]
    dis("gama",2,files=flies)

#二值化
def erzhihua(img1):
    img6 = np.zeros((H,W),np.uint8)
    for i in range(H):
        for j in range(W):
            if img1[i,j]>127:
                gray = 255
            else:
                gray = 0
            img6[i,j]=gray
    flies = [img1,img6]
    dis("erzhihua",2,files=flies)

#直方图均衡
def Hist(img):
    Newimg = np.zeros((H, W), np.uint8)  # 二维数组
    Hist = np.zeros(256, np.int)  # Pixel sum一维均衡化前
    EqHist = np.zeros(256, np.int)  # Equal Pixel均衡化后
    HistP = np.zeros(256, np.float)  # 像素概率
    HistPSUM = np.zeros(256, np.float)  # 像素概率和
    Pixelsum = H * W
    for i in range(H):
        for j in range(W):
            # Every Gray Pixel sum
            Hist[img[i,j]]+=1#像素点出现的次数

    for i in range(256):
        HistP[i] =Hist[i]/Pixelsum#像素点出现的概率

    for i in range(1,256):
        HistPSUM[i] =HistP[i]+HistPSUM[i-1]#归一化

    for i in range(256):
        EqHist[i] =HistPSUM[i]*255#均衡化后灰度值

    for i in range(H):
        for j in range(W):
            # Set New pixels Gray
            Newimg[i,j]= EqHist[img[i,j]]

    files = [img,Newimg]
    dis("7",2,files)
    display(2,files)
    return Newimg

#3x3中值滤波
def cross3x3(img):
    curimg = np.zeros((H,W),np.uint8)
    newimg = np.zeros((H,W),np.uint8)
    for i in range(1,H-1):
        for j in range(1,W-1):
            t00 = img[i-1, j - 1]
            t01 = img[i-1, j]
            t02 = img[i-1, j + 1]
            t10 = img[i, j-1]
            t11 = img[i, j]
            t12 = img[i, j+1]
            t20 = img[i + 1, j-1]
            t21 = img[i + 1, j]
            t22 = img[i + 1, j+1]
            templ =[t00,t01,t02,t10,t11,t12,t20,t21,t22]
            templ.sort()
            curimg[i,j]=templ[4]
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if curimg[i,j] != 0:
                newimg[i,j] = curimg[i,j]
            else:
                newimg[i,j] = img[i,j]
    files = [img,curimg,newimg]
    dis('3x3', 3, files)
    return newimg

def Robert(H,W,img):
    imgR = np.zeros((H,W),np.uint8)
    for i in range(0, H - 1):
        for j in range(0, W - 1):
            a00 = np.int16(img[i,j])
            a01 = np.int16(img[i,j+1])
            a10 = np.int16(img[i+1,j])
            a11 = np.int16(img[i+1,j+1])
            #u = np.sqrt((a00-a11)**2 + (a10-a01)**2)
            u = np.abs((a00-a11))+np.abs(a10-a01)
            if u>= 255:
                u = 255
            elif u<0:
                u = 0
            imgR[i,j] =np.uint8(u)
    return imgR

def Grad(H,W,img):
    imgG= np.zeros((H, W), np.uint8)
    for i in range(0, H - 1):
        for j in range(0, W - 1):
            a00 = np.int16(img[i, j])
            a01 = np.int16(img[i, j + 1])
            a10 = np.int16(img[i + 1, j])
            a11 = np.int16(img[i + 1, j + 1])
            u = np.abs(a00 - a10) + np.abs(a00 - a01)
            if u >= 255:
                u = 255
            elif u < 0:
                u = 0
            imgG[i, j] = np.uint8(u)
    return imgG

def Prewitt(H,W,img):
    imgpX = np.zeros((H, W), np.uint8)
    imgpY = np.zeros((H, W), np.uint8)
    imgpXY = np.zeros((H, W), np.uint8)
    imgpS = np.zeros((H, W), np.uint8)
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            a00 = img[i - 1, j - 1]
            a01 = img[i - 1, j]
            a02 = img[i - 1, j + 1]
            a10 = img[i, j - 1]
            a11 = img[i, j]
            a12 = img[i, j + 1]
            a20 = img[i + 1, j - 1]
            a21 = img[i + 1, j]
            a22 = img[i + 1, j + 1]
            ux = a20 * 1 + a10 * 1 + a00 * 1 + a02 * -1 + a12 * -1 + a22 * -1
            imgpX[i, j] = ux
            uy = a02 * 1 + a01 * 1 + a00 * 1 + a20 * -1 + a21 * -1 + a22 * -1
            imgpY[i, j] = uy
            imgpXY[i, j] = np.sqrt(ux * ux + uy * uy)
            imgpS[i, j] = np.abs(ux) + np.abs(uy)
    titles = ["imgpX","imgpY","imgpXY","imgpS"]
    files = [imgpX, imgpY, imgpXY, imgpS]
    displays(2,2,titles,files)
    return imgpX, imgpY, imgpXY, imgpS

def Sobel(H,W,img):
    imgX = np.zeros((H,W),np.uint8)
    imgY = np.zeros((H,W),np.uint8)
    imgXandY = np.zeros((H,W),np.uint8)
    imgabS = np.zeros((H,W),np.uint8)
    for i in range(1,H-1) :
        for j in range (1,W-1):
            a00 = img[i-1, j-1]
            a01 = img[i-1, j]
            a02 = img[i-1, j+1]
            a10 = img[i,j-1]
            a11 = img[i,j]
            a12 = img[i, j+1]
            a20 = img[i+1, j-1]
            a21 = img[i+1, j]
            a22 = img[i+1, j+1]
            ux = a20 * 1 + a10 * 2 + a00 * 1  + a02 * -1 + a12 * -2 + a22 *-1
            imgX[i,j] = ux
            uy = a02 * 1 + a01 * 2 + a00 * 1+ a20 * -1 + a21 * -2 + a22 * -1
            imgY[i,j] = uy
            imgXandY[i,j] = np.sqrt(ux* ux+uy *uy)
            imgabS[i,j]  = np.abs(ux) + np.abs(uy)
    titles = ["imgpX", "imgpY", "imgXandY", "imgabS"]
    files = [imgX,imgY,imgXandY,imgabS]
    displays(2,2,titles, files)
    return imgX,imgY,imgXandY,imgabS


if __name__ == '__main__':
    img = cv.imread("cell.jpg")
    # img11 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img1 = grey(img)
    H = img1.shape[0]
    W = img1.shape[1]
    print(img1.shape)
    cv.imshow("img1",img1)
    # cv.imshow("img11",img11)

    # huidushangyi(img1)
    # huiduduibidu(img1)
    # img4 = huidufanzhuan(img1)
    # gama(img1)
    # erzhihua(img1)
    # imgh = Hist(img1)
    # imgh = Hist(img4)
    # imgN = cross3x3(imgh)
    # imga = cv.medianBlur(img1,3)
    # imga1 = cv.medianBlur(img1,5)
    # imga2 = cv.medianBlur(img1,7)
    # imgb = cv.GaussianBlur(img1,(7,7),0)
    # imgc = cv.blur(img1,(5,5))
    # imgd = cv.bilateralFilter(img1,127,75,75)
    # cv.imshow("imga",imga)
    # cv.imshow("imga1",imga1)
    # cv.imshow("imga2",imga2)
    # cv.imshow("imgb",imgb)
    # cv.imshow("imgc",imgc)
    # cv.imshow("imgd",imgd)
    # cv.imshow("img",img)
    #
    # imgG = Grad(H, W, imgN)
    # imgR = Robert(H, W, imgN)
    # files = [imgN,imgG,imgR]
    # titles = ["Original","Grad image","Rebert image"]
    # # dis('R,G', 3, files)
    # displays(1,3,titles,files)
    # (imgpX, imgpY, imgpXY, imgpS) = Prewitt(H, W, imgN)
    # (imgX, imgY, imgXandY, imgabS) = Sobel(H, W, imgN)


    cv.waitKey(0)
    cv.destroyAllWindows()

