import easyocr
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_img_data(path):
    reader = easyocr.Reader(['en'])
    file = cv2.imread(path,cv2.CV_8UC1)
    print(file.dtype)
    print(file.shape)
    aimimg = file[334:375, 34:696]
    # gray = cv2.cvtColor()

    th2 = cv2.adaptiveThreshold(aimimg,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

    plt.imshow(th2)
    plt.show()
    result = reader.readtext(th2)

    for r in result:
        print(r)










if __name__ == '__main__':
    get_img_data(r"I:\python3proj\spider_filters\output\4860\cinegel_4860_jpg\cinegel_4860.jpg")


