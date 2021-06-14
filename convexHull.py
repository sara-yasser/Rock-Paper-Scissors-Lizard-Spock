from random import randint # for sorting and creating data pts
from math import atan2 # for computing polar angle
import math
import numpy as np

def polar_angle(p0,p1=None):
    if p1==None: p1=anchor
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return atan2(y_span,x_span)



def distance(p0,p1=None):
    if p1==None: p1=anchor
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return y_span**2 + x_span**2



def det(p1,p2,p3):
    return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
            -(p2[1]-p1[1])*(p3[0]-p1[0])



def quicksort(a):
    if len(a)<=1: return a
    smaller,equal,larger=[],[],[]
    piv_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot
    for pt in a:
        pt_ang=polar_angle(pt) # calculate current point angle
        if   pt_ang<piv_ang:  smaller.append(pt)
        elif pt_ang==piv_ang: equal.append(pt)
        else:                   larger.append(pt)
    return   quicksort(smaller) \
            +sorted(equal,key=distance) \
            +quicksort(larger)



def graham_scan(points,show_progress=False):
    global anchor # to be set, (x,y) with smallest y value


    min_idx=None
    for i,(x,y) in enumerate(points):
        if min_idx==None or y<points[min_idx][1]:
            min_idx=i
        if y==points[min_idx][1] and x<points[min_idx][0]:
            min_idx=i


    anchor=points[min_idx]


    sorted_pts=quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]


    hull=[anchor,sorted_pts[0]]
    for s in sorted_pts[1:]: 
        if len(hull)>=2 :
            
            while det(hull[len(hull)-2],hull[len(hull)-1],s)<=0:
                
                
                del hull[len(hull)-1] # backtrack
                
                if len(hull)<2: break

            hull.append(s)

    return hull




#defects



def distanceCon(p0,p1):
    y_span=p0[0,1]-p1[0,1]
    x_span=p0[0,0]-p1[0,0]
    return (y_span**2 + x_span**2)**0.5

def getTriangleAreaAndAngle(far,start,end):

    a = math.sqrt((end[0,0] - start[0,0])**2 + (end[0,1] - start[0,1])**2)
    b = math.sqrt((far[0] - start[0,0])**2 + (far[1] - start[0,1])**2)
    c = math.sqrt((end[0,0] - far[0])**2 + (end[0,1] - far[1])**2)
    s = (a+b+c)/2
    if (s*(s-a)*(s-b)*(s-c))<0: return [0,0]
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    if b*c==0: return [0,0]
    Aang= round((b**2 + c**2 - a**2)/(2*b*c),5)
    if (Aang)<=-1.0 and (Aang)>=1.0: 
        return [0,0]
    
    angle = math.acos(Aang) *57
    return [area,angle]



def convexityDefects(contour, hull):
    defects=[]
    for i in range(hull.shape[0]-1):
        dst=distanceCon(contour[hull[i][0]],contour[hull[i+1][0]])
        if dst<50: 
            continue
        part=contour[hull[i][0]:hull[i+1][0],0,:]
        
        areaAndAngle=np.array([getTriangleAreaAndAngle(x,contour[hull[i][0]],contour[hull[i+1][0]]) for x in part])


        heights=(2*areaAndAngle[:,0]/(dst))
        if heights.size == 0:
            continue
        maxHeight=np.max(heights)
        index=np.where(np.logical_and( heights==maxHeight , areaAndAngle[:,1]<90))[0]
        if(index.size != 0 and maxHeight>60):
            defects.append(np.array([contour[hull[i][0]],contour[hull[i+1][0]],contour[index[0]+hull[i][0]]]))
            
    


    defects=np.array(defects)
    return defects