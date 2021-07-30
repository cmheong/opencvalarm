#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
#
# adapted cmheong 2021-07-30 https://cmheong.blogspot.com
############################################


import cv2
import numpy as np

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
import os

# read object dictionary
classes = None
with open('./yolov3.txt', 'r') as f:
  classes = [line.strip() for line in f.readlines()]

net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')

# List all files in a directory using scandir()
basepath = '../alarms/'
entries = os.scandir(basepath)
for entry in entries:
  if entry.is_file():
    if entry.name.startswith('341front_') and  entry.name.endswith('original.png'):
      print("Processing alarm file", entry.name)

      image = cv2.imread(basepath+entry.name)
      Width = image.shape[1]
      Height = image.shape[0]
      scale = 0.00392

      COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
      blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
      net.setInput(blob)
      outs = net.forward(get_output_layers(net))
      class_ids = []
      confidences = []
      boxes = []
      conf_threshold = 0.5
      nms_threshold = 0.4
      indices = []

      for out in outs:
        for detection in out:
          scores = detection[5:]
          class_id = np.argmax(scores)
          confidence = scores[class_id]
          if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])

      indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
      # print("indices length", len(indices), "indices", indices)
      for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

      if len(indices) > 0:
        #cv2.imshow("object detection", image)
        #cv2.imwrite("object-detection.jpg", image)
        #cv2.waitKey(1000)
        ns = entry.name.rsplit("_")
        cv2.imwrite('../alarm/'+ns[0]+'_'+ns[1]+'_'+ns[2]+'.jpg', image)
    
cv2.destroyAllWindows()

