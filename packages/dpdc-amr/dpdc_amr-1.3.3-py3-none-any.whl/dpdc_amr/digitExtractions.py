from ultralytics import YOLO
import cv2
import base64
import numpy as np
from ultralytics.utils.plotting import Annotator
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'weights\\best.pt')



def getYoloModel():
    model = YOLO(model_path)
    return model


def extract_digits(test_model, bigfile, conf, imgflg = False):
    img = cv2.imread(bigfile)
    annotator = Annotator(img)

    y_adjustment = 20.0

    test_model.conf = conf
    result = test_model.predict(source=bigfile, show_conf=True, save=False,
                                save_crop=False, exist_ok=True, verbose=False,iou=.4,
                                agnostic_nms=True)

    digit = {}

    for r in result:

        boxes = r.boxes
        avg_y = np.mean([box.xywh.tolist()[0][1] for box in boxes])


        high_box =np.array( [[int(box.xywh.tolist()[0][0]), box.conf.item()] for box in boxes])
        high_conf_box = np.array([high_box[high_box[:, 0] == key].max(axis=0) for key in np.unique(high_box[:, 0])])
        lookup_dict = {int(key): value for key, value in high_conf_box}
        #print(lookup_dict)

        for box in boxes:
           # print(box.xywh.tolist()[0][0] , ':' , box.conf)
            y = box.xywh.tolist()[0][1]
            box_conf=lookup_dict.get(int(box.xywh.tolist()[0][0]),None)
            #print(box_conf)
            if box.conf >= box_conf and avg_y + y_adjustment >= y >= avg_y - y_adjustment:
                c = box.cls
                b = box.xyxy[0]
                digit.update({box.xywh.tolist()[0][0]: test_model.names[int(c)]})
                annotator.box_label(b, test_model.names[int(c)])

    digits_str = ''
    for x, y in sorted(digit.items()):
        digits_str += str(y)

    #print(imgflg)
    base64_image=''
    if imgflg:
        # Get the annotated image
        img = annotator.result()
        # Convert the image to base64
        _, buffer = cv2.imencode('.jpg', img)
        base64_image = base64.b64encode(buffer).decode()
    return digits_str,base64_image
