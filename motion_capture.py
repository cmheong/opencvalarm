import cv2
import cvui
username = "admin"
password = "password"
width = 640
height = 480
cam_no = 1
def create_camera (channel):
    rtsp = "http://" + username + ":" + password + "@192.168.10.30/cgi/mjpg/mjpg.cgi"
    cap = cv2.VideoCapture()
    cap.open(rtsp)
    cap.set(3, 640)  # ID number for width is 3
    cap.set(4, 480)  # ID number for height is 480
    cap.set(10, 100)  # ID number for brightness is 10qq
    return cap
cam = create_camera(str(cam_no))
cvui.init('screen')
while True:
    success, current_cam = cam.read()
    dim = (width, height)
    Full_frame = cv2.resize(current_cam, dim, interpolation=cv2.INTER_AREA)
    cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    if (cvui.button(Full_frame, width - 100, height - 40, "Next") and cvui.mouse(cvui.CLICK)):
        print("Next Button Pressed")
        cvui.init('screen')
        cam_no = cam_no+1
        if (cam_no>4):
            cam_no=1
        del cam
        cam = create_camera(str(cam_no))
    if (cvui.button(Full_frame, width - 200, height - 40, "Previous") and cvui.mouse(cvui.CLICK)):
        print("Previous Button Pressed")
        cvui.init('screen')
        cam_no = cam_no - 1
        if (cam_no<1):
            cam_no=4
        del cam
        cam = create_camera(str(cam_no))
    cv2.imshow('screen', Full_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
