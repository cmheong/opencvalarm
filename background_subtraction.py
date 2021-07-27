# Author: Addison Sears-Collins
# Description: This algorithm detects objects in a video stream
#   using the Gaussian Mixture Model background subtraction method. 
 
# import the necessary packages
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np # Import NumPy library
# import subprocess # capture images via curl
import datetime

# Create the background subtractor object
# Feel free to modify the history as you see fit.
back_sub = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)
 
# Create kernel for morphological operation. You can tweak
# the dimensions of the kernel.
# e.g. instead of 20, 20, you can try 30, 30
kernel = np.ones((20,20),np.uint8)
# cmd = "curl -s -u admin:password -o 341front.jpg -k http://192.168.10.30/cgi/jpg/image.cgi"

key = 0
trigger = 0 # count consecutive triggers
avg_image = None

# subprocess.check_output(cmd, shell=True)
cam = cv2.VideoCapture('http://admin:password@192.168.10.30/cgi/mjpg/mjpg.cgi')

# Capture frames continuously from the trendnet ip camera
while key != ord("q"):
    # Grab the raw NumPy array representing the image
    # subprocess.check_output(cmd, shell=True)
    # original_image = cv2.imread('341front.jpg')
    ret, original_image = cam.read()
    image = original_image
    #cv2.imshow('image', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # crop image 2021-07-16
    #image = image[120:480, 0:640]
    image = image[120:480, 0:600]
    clr_image = image
    # use weighted average
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (21, 21), 0)
    if avg_image is None:
      avg_image = image.copy().astype(float)
    cv2.accumulateWeighted(image, avg_image, 0.125)

    # Convert to foreground mask
    #fg_mask = back_sub.apply(image)
    fg_mask = back_sub.apply(avg_image)

    # Close gaps using closing
    fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
    # closegaps = fg_mask

    # Remove salt and pepper noise with a median filter
    fg_mask = cv2.medianBlur(fg_mask,5)

    # saltnpepper = fg_mask

    # If a pixel is less than ##, it is considered black (background).
    # Otherwise, it is white (foreground). 255 is upper limit.
    # Modify the number after absolute_difference as you see fit.
    _, fg_mask = cv2.threshold(fg_mask, 112, 255, cv2.THRESH_BINARY)
    threshholded = fg_mask

    # Find the contours of the object inside the binary image
    contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]
    # If there are no countours
    if len(areas) < 1:
      trigger = 0 # 2021-07-18 reset consecutive trigger count

      #print("!There are no countours!")
      # Display the resulting frame
      cv2.imshow('Frame',clr_image)

      # Wait for keyPress for 1 millisecond
      key = cv2.waitKey(1) & 0xFF

      # If "q" is pressed on the keyboard,
      # exit this loop
      if key == ord("q"):
        break

      # Go to the top of the for loop
      continue

    else:
      #print("Found countours!!!! area is ", areas)

      # Find the largest moving object in the image
      # 2021-07-21 scroll through all objects
      # max_index = np.argmax(areas)
      for i in range(0, len(areas)):

        # Draw the bounding box
        # cnt = contours[max_index]
        cnt = contours[i]
        x,y,w,h = cv2.boundingRect(cnt)

        if w*h > 3000 and w*h<33000 :
          break
      if w*h > 3000 and w*h<33000 :
        trigger += 1
        if trigger > 5 :
          print("TRIGGER!!! trigger #", trigger, "areas size is ", len(areas), "object size is ", w*h, "at (", x, ",", y, ") on", datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          cv2.rectangle(clr_image,(x,y),(x+w,y+h),(0,255,0),3)

          # Draw circle in the center of the bounding box
          x2 = x + int(w/2)
          y2 = y + int(h/2)
          cv2.circle(clr_image,(x2,y2),4,(0,255,0),-1)

          # Print the centroid coordinates (we'll use the center of the
          # bounding box) on the image
          text = "x: " + str(x2) + ", y: " + str(y2)
          cv2.putText(image, text, (x2 - 10, y2 - 10),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

          # Display the resulting frame
          cv2.imshow("Frame",clr_image)
          #cv2.imshow("fg_mask",fg_mask)

          # save to file 2021-07-15
          filename = './alarms/341front_{}_size_{}.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), w*h)
          cv2.imwrite(filename,clr_image)
          filename = './alarms/341front_{}_original.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          cv2.imwrite(filename, original_image)
          # filename = './alarms/341front_{}_fg_mask.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          # cv2.imwrite(filename,fg_mask)

          # filename = './alarms/341front_{}_closegaps.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          # cv2.imwrite(filename,closegaps)
          # filename = './alarms/341front_{}_saltnpepper.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          # cv2.imwrite(filename,saltnpepper)
          filename = './alarms/341front_{}_threshholded.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
          cv2.imwrite(filename,threshholded)

          # Wait for keyPress for 1 millisecond
          key = cv2.waitKey(1) & 0xFF

          # If "q" is pressed on the keyboard,
          # exit this loop
          if key == ord("q"):
            break

          # a genuine trigger might set off a chain3of false ones
          trigger = 0
        else:
          print("index", i, "trig_cnt",  trigger, "areas size is ", len(areas), "object size is ", w*h, "at (", x, ",", y, ") on", datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

# Close down windows
cv2.destroyAllWindows()

