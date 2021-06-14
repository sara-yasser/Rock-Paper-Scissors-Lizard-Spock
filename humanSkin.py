import cv2
import numpy as np

#Shoelace formula
def getContourArea(contour):
    x=contour[:,0,0]
    y=contour[:,0,1]
    #np.roll(x, 1) rotate right (1)
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))




def getMaxContourArea(contours):
    maxArea=0
    maxContour=None
    box=None
    for contour in contours:
        Xmin = np.min(contour[:,:,0])
        Xmax = np.max(contour[:,:,0])
        Ymin = np.min(contour[:,:,1])
        Ymax = np.max(contour[:,:,1])
        contourArea=getContourArea(contour)
        if contourArea>maxArea:
            maxArea=contourArea
            maxContour=contour
            box=[Xmin, Xmax, Ymin, Ymax]
            
    return maxArea,maxContour,box




def getHand(frame):

    
    handBool=False
    humanSkin=getHumanSkin(frame)
    maxContour=None
    contours = cv2.findContours(humanSkin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    if   len(contours)>0 :
                maxContourArea,maxContour,[Xmin, Xmax, Ymin, Ymax] =getMaxContourArea(contours)
                if maxContourArea > 10000:
                    handBool=True
                    humanSkin = humanSkin[Ymin:Ymax, Xmin:Xmax]
        
    return humanSkin,handBool,maxContour



def getHumanSkin(frame):

    img=np.copy(frame)
    
    img = cv2.blur(img,(11,11)) #blur

    #converting from rgb to YCbCr color space
    img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    #skin color range for YCbCr color space 
    YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))

    
    return YCrCb_mask

