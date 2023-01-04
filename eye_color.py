# face color analysis given eye center position

import sys
import os
import numpy as np
import cv2
import argparse
import time
from mtcnn.mtcnn import MTCNN
import detect
import predict
detector = MTCNN()

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', default="download.jpg",
                    help="it can be image or video or webcan id")
parser.add_argument('--input_type', default='image',
                    help="either image or video (for video file and webcam id)")
opt = parser.parse_args()

# define HSV color ranges for eyes colors
class_name = ("black", "white", "red1", "red2",
              "green", "blue", "yellow", "brown", "gray")
EyeColor = {
    class_name[0]: [[180, 255, 30], [0, 0, 0]],
    class_name[1]: [[180, 18, 255], [0, 0, 231]],
    class_name[2]: [[180, 255, 255], [159, 50, 70]],
    class_name[3]: [[9, 255, 255], [0, 50, 70]],
    class_name[4]: [[89, 255, 255], [36, 50, 70]],
    class_name[5]: [[128, 255, 255], [90, 50, 70]],
    class_name[6]: [[35, 255, 255], [25, 50, 70]],
    class_name[7]: [[24, 255, 255], [10, 50, 70]],
    class_name[8]: [[180, 18, 230], [0, 0, 40]]


}


def check_color(hsv, color):
    if (hsv[0] >= color[0][0]) and (hsv[0] <= color[1][0]) and (hsv[1] >= color[0][1]) and \
            hsv[1] <= color[1][1] and (hsv[2] >= color[0][2]) and (hsv[2] <= color[1][2]):
        return True
    else:
        return False

# define eye color category rules in HSV space


def find_class(hsv):
    color_id = 7
    for i in range(len(class_name)-1):
        if check_color(hsv, EyeColor[class_name[i]]) == True:
            color_id = i

    return color_id
    print(color_id)


def eye_color(x):
    image = cv2.imread(x)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, w = image.shape[0:2]
    imgMask = np.zeros((image.shape[0], image.shape[1], 1))

    result = detector.detect_faces(image)
    if result == []:
        print('Warning: Can not detect any face in the input image!')
        return

    bounding_box = result[0]['box']
    left_eye = result[0]['keypoints']['left_eye']
    right_eye = result[0]['keypoints']['right_eye']

    eye_distance = np.linalg.norm(np.array(left_eye)-np.array(right_eye))
    eye_radius = eye_distance/15  # approximate

    cv2.circle(imgMask, left_eye, int(eye_radius), (255, 255, 255), -1)
    cv2.circle(imgMask, right_eye, int(eye_radius), (255, 255, 255), -1)

    cv2.rectangle(image,
                  (bounding_box[0], bounding_box[1]),
                  (bounding_box[0]+bounding_box[2],
                   bounding_box[1] + bounding_box[3]),
                  (255, 155, 255),
                  2)

    cv2.circle(image, left_eye, int(eye_radius), (0, 155, 255), 1)
    cv2.circle(image, right_eye, int(eye_radius), (0, 155, 255), 1)

    eye_class = np.zeros(len(class_name), np.float)

    for y in range(0, h):
        for x in range(0, w):
            if imgMask[y, x] != 0:
                eye_class[find_class(imgHSV[y, x])] += 1

    main_color_index = np.argmax(eye_class[:len(eye_class)-1])
    total_vote = eye_class.sum()

    # print("\n\nDominant Eye Color: ", class_name[main_color_index])
    return class_name[main_color_index]
    print("\n **Eyes Color Percentage **")
    for i in range(len(class_name)):
        print(class_name[i], ": ", round(eye_class[i]/total_vote*100, 2), "%")

    label = 'Dominant Eye Color: %s' % class_name[main_color_index]
    cv2.putText(image, label, (left_eye[0]-10, left_eye[1]-40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155, 255, 0))
    cv2.imshow('EYE-COLOR-DETECTION', image)
    print(detect.age(image))
    print(predict.bald(image))


if __name__ == '__main__':

    # image
    # if opt.input_type == 'image':
    image = cv2.imread(opt.input_path, cv2.IMREAD_COLOR)
    # detect color percentage
    eye_color(image)
    cv2.imwrite('sample/result.jpg', image)
    cv2.waitKey(0)

    # video or webcam
    # else:
    #     cap = cv2.VideoCapture(opt.input_path)
    #     while(True):
    #         ret, frame = cap.read()
    #         if ret == -1:
    #             break

    #         eye_color(frame)
    #         if cv2.waitKey(0) & 0xFF == 27:
    #             break
