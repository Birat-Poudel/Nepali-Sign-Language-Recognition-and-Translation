import cv2
import numpy as np
import os
import string



if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/train"):
    os.makedirs("data/train")
if not os.path.exists("data/test"):
    os.makedirs("data/test")
   
   
for i in range(3):
    if not os.path.exists("data/train/" + str(i)):
        os.makedirs("data/train/"+str(i))
    if not os.path.exists("data/test/" + str(i)):
        os.makedirs("data/test/"+str(i))
         
    
j=0;


for i in string.ascii_uppercase:
    if not os.path.exists("data/train/" + i):
        os.makedirs("data/train/"+i)
    if not os.path.exists("data/test/" + i):
        os.makedirs("data/test/"+i)
    j=j+1
    if j==9:
        break;
    

mode = 'train'
directory = 'data/'+mode+'/'
mode2='test'
directory2='data/'+mode2+'/'


minValue = 70


cap = cv2.VideoCapture(0)


interrupt = -1 


flag=True


while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    
    
    count = {
             'zero': len(os.listdir(directory+"/0")),
             'one': len(os.listdir(directory+"/1")),
             'two': len(os.listdir(directory+"/2")),
             
             'a': len(os.listdir(directory+"/A"))+1,
             'b': len(os.listdir(directory+"/B"))+1,
             'c': len(os.listdir(directory+"/C"))+1,
             'd': len(os.listdir(directory+"/D"))+1,
             'e': len(os.listdir(directory+"/E"))+1,
             'f': len(os.listdir(directory+"/F"))+1,
             'g': len(os.listdir(directory+"/G"))+1,
             'h': len(os.listdir(directory+"/H"))+1,
             'i': len(os.listdir(directory+"/I"))+1,
            }
    
    count2 = {
             'zero': len(os.listdir(directory2+"/0")),
             'one': len(os.listdir(directory2+"/1")),
             'two': len(os.listdir(directory2+"/2")),
              
             'a': len(os.listdir(directory2+"/A"))+1,
             'b': len(os.listdir(directory2+"/B"))+1,
             'c': len(os.listdir(directory2+"/C"))+1,
             'd': len(os.listdir(directory2+"/D"))+1,
             'e': len(os.listdir(directory2+"/E"))+1,
             'f': len(os.listdir(directory2+"/F"))+1,
             'g': len(os.listdir(directory2+"/G"))+1,
             'h': len(os.listdir(directory2+"/H"))+1,
             'i': len(os.listdir(directory2+"/I"))+1,
            }
    
    cv2.rectangle(frame, (270-1, 9), (620+1, 355), (265,0,0) ,1)
    cv2.imshow("Frame", frame)
    
    roi = frame[50:350, 270:570]
    
    cv2.imshow("ROI", roi)
    
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    
    blur = cv2.GaussianBlur(gray,(5,5),2)
    
    blur = cv2.bilateralFilter(blur,3,75,75)
    
    
    th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    ret, roi = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    cv2.imshow("ROI", roi)
    
    # roi = cv2.resize(roi, (64, 64))
    
    interrupt = cv2.waitKey(10)
    
    if interrupt & 0xFF == 27: # esc key
        break  
    
    if interrupt & 0xFF == ord('0'):
        if count['zero']%3==0 and flag:
            cv2.imwrite(directory2+'0/'+str(count2['zero'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'0/'+str(count['zero'])+'.jpg', roi)
            flag=True
    
    if interrupt & 0xFF == ord('1'):
        if count['one']%3==0 and flag:
            cv2.imwrite(directory2+'1/'+str(count2['one'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'1/'+str(count['one'])+'.jpg', roi)
            flag=True
    
    if interrupt & 0xFF == ord('2'):
        if count['two']%3==0 and flag:
            cv2.imwrite(directory2+'2/'+str(count2['two'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'2/'+str(count['two'])+'.jpg', roi)
            flag=True
    
    
            
    if interrupt & 0xFF == ord('a'):
        if count['a']%3==0 and flag:
            cv2.imwrite(directory2+'A/'+str(count2['a'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'A/'+str(count['a'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('b'):
        if count['b']%3==0 and flag:
            cv2.imwrite(directory2+'B/'+str(count2['b'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'B/'+str(count['b'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('c'):
        if count['c']%3==0 and flag:
            cv2.imwrite(directory2+'C/'+str(count2['c'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'C/'+str(count['c'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('d'):
        if count['d']%3==0 and flag:
            cv2.imwrite(directory2+'D/'+str(count2['d'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'D/'+str(count['d'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('e'):
        if count['e']%3==0 and flag:
            cv2.imwrite(directory2+'E/'+str(count2['e'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'E/'+str(count['e'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('f'):
        if count['f']%3==0 and flag:
            cv2.imwrite(directory2+'F/'+str(count2['f'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'F/'+str(count['f'])+'.jpg', roi)
            flag=True
    
    if interrupt & 0xFF == ord('g'):
        if count['g']%3==0 and flag:
            cv2.imwrite(directory2+'G/'+str(count2['g'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'G/'+str(count['g'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('h'):
        if count['h']%3==0 and flag:
            cv2.imwrite(directory2+'H/'+str(count2['h'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'H/'+str(count['h'])+'.jpg', roi)
            flag=True
            
    if interrupt & 0xFF == ord('i'):
        if count['i']%3==0 and flag:
            cv2.imwrite(directory2+'I/'+str(count2['i'])+'.jpg', roi)
            flag=False
        else:
            cv2.imwrite(directory+'I/'+str(count['i'])+'.jpg', roi)
            flag=True
              
  
cap.release()
cv2.destroyAllWindows()


    
    