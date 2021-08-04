# https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv

import cv2

# Both rtsp and http works for trendnet tv-ip422wn
cap = cv2.VideoCapture('rtsp://admin:password@192.168.10.30/mpeg4')
#cap = cv2.VideoCapture('http://admin:password@192.168.10.30/cgi/mjpg/mjpg.cgi')

while True:

    #print('About to start the Read command')
    ret, frame = cap.read()
    #print('About to show frame of Video.')
    cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
