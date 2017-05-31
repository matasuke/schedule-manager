import cv2
import numpy as np
import sys
import time
import requests

def get_diff(im_before, im_now, th):
    
    imageGray_before = cv2.cvtColor(im_before, cv2.COLOR_BGR2GRAY)
    imageGray_now = cv2.cvtColor(im_now, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(im_before, im_now)
    print(np.sum(diff))
    return np.sum(diff) > th

def get_movement(th):

    cap = cv2.VideoCapture(0)
    ret, f_before = cap.read()
    

    while True:
        ret, frame = cap.read()
        
        if get_diff(f_before, frame, th):
            requests.post('https://testapps009.herokuapp.com/post')    
        f_before = frame
        time.sleep(3)


        

if __name__ == "__main__":
    get_movement(40000000);
