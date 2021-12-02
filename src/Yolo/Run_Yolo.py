import cv2
import numpy as np


def loadModel(weights, cfg):
    yolo = cv2.dnn.readNet(weights, cfg)
    yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
    return yolo


def getOutput(yolo, img):
    blob = cv2.dnn.blobFromImage(img, 1/255,(320,320), (0,0,0), swapRB=True, crop=False)
    yolo.setInput(blob)
    output_layers_names = yolo.getUnconnectedOutLayersNames()
    layerOutput = yolo.forward(output_layers_names)
    (H, W) = img.shape[:2]
    return layerOutput, W, H


def getBoxes(layerOutput, W, H):
    boxes = []
    confidences = []
    class_ids = []
    for output in layerOutput:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.4:

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids


def getImagewithLabel(boxes, confidences, class_ids, image):
    classes = ['Head', 'Arms', 'Hand', 'Spine', 'Legs', 'Feet']
    indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.4,0.4)
    font = cv2.FONT_HERSHEY_COMPLEX
    colors = np.random.uniform(0,255,size = (len(boxes),3))
    print(len(indexes))

    if len(indexes) != 0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str (classes[class_ids[i]])
            confi = str(round(confidences[i],2))
            color = colors[i]

            if (label == "Head"):
                color = [ 71.39511963, 201.96006481,  96.11926929]
            elif (label == "Spine"):
                color = [255,255,255]

            cv2.rectangle(image,(x,y), (x+w, y+h), color, 2)
            cv2.putText(image,label+" "+confi, (x,y), font, 1, (255,255,255),2)
    return image


def getLabelledImage(imagePath, yoloModel):
    img = cv2.imread(imagePath)
    output, W, H = getOutput(yoloModel, img)
    boxes, confidences, class_ids = getBoxes(output, W, H)
    labelledImage = getImagewithLabel(boxes, confidences, class_ids, img)
    bbExists = True
    if(len(boxes) == 0):
        bbExists = False
    return labelledImage, bbExists


def analyzeImage(imPath):
    # Load the yolo model
    weights = "./Yolo/Model/yolov4.weights"
    cfg = "./Yolo/Model/yolov4.cfg"
    yolo = loadModel(weights, cfg)

    # specify image path
    imagePath = imPath

    # get the labelled image
    finalImage, bbExists = getLabelledImage(imagePath, yolo)
    return finalImage, bbExists


